from typing import AsyncGenerator, Generator
from fastapi import Depends, FastAPI, Response, UploadFile, File, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from ntp_manager.pa import main as pa_main
import orjson
import time
import asyncio
import sqlite3
import aiomysql
from aiomysql import DictCursor
from dataclasses import dataclass


from ntp_manager.utils import geojson_default


def init_sqlite_db():
    conn = sqlite3.connect('requests.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS requests 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       ip TEXT, 
                       file_name TEXT,
                       duration INTEGER,
                       content_size INTEGER,
                       timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                       )''')
    
    conn.commit()
    conn.close()

init_sqlite_db()

class FastAPIWithDb(FastAPI):
    pool: aiomysql.Pool

app = FastAPIWithDb()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

lock = asyncio.Lock()

@app.on_event("startup")
async def startup():
    app.pool = await aiomysql.create_pool(
        host='localhost',
        user='myuan',
        password='room409',
        db='nhp',
        loop=asyncio.get_running_loop(),
    )

@app.on_event("shutdown")
async def shutdown():
    app.pool.close()


async def get_db() -> AsyncGenerator[DictCursor, None]:
    async with app.pool.acquire() as conn:
        async with conn.cursor(DictCursor) as cur:
            yield cur
        await conn.commit()

@app.post("/api/ntp")
async def upload_ntp(
    request: Request, 
    files: list[UploadFile] = File(...), 
    ignore_regions: list[str] = Form([]),
    um_per_pixel: int = Form(10000),
    transpose: bool = Form(False),
):
    res = {}
    t0 = time.time()

    for file in files:
        if file.filename is None:
            continue

        content = await file.read()
        write_path = Path('/tmp') / file.filename
        with open(write_path, 'wb') as f:
            f.write(content)
        res[file.filename] = pa_main(
            write_path, um_per_pixel=um_per_pixel, 
            ignore_regions=ignore_regions, transpose=transpose
        )
    res['delta'] = time.time() - t0
    content=orjson.dumps(res, default=geojson_default, option=orjson.OPT_SERIALIZE_NUMPY)

    async with lock:
        conn = sqlite3.connect('requests.db')
        cursor = conn.cursor()
        for file in files:
            cursor.execute('''
            INSERT INTO requests (ip, file_name, duration, content_size)
            VALUES (?, ?, ?, ?)
            ''', (
                request.headers.get('X-REAL-IP', ''), 
                file.filename,
                int(res['delta'] * 1000),
                len(content)
            ))
        conn.commit()
        conn.close()

    return Response(
        media_type="application/json", 
        content=orjson.dumps(res, default=geojson_default, option=orjson.OPT_SERIALIZE_NUMPY)
    )

@app.post("/api/check-region-names")
async def check_region_names(
    species: str, 
    names: list[str], 
    cur: DictCursor = Depends(get_db)
):
    sql_res = cur.mogrify('''
    SELECT 
        region_info.id, region_id, acronym, region_info.name, parent_id, insert_datetime,
        insert_person, species.name as species_name, species_id
    FROM nhp.region_info
    join nhp.species on species.id = region_info.species_id
    WHERE nhp.species.name = %s and BINARY acronym in %s
    ''', (species, (names)))
    print(sql_res)
    if not names:
        return []

    await cur.execute('''
    SELECT 
        region_info.id, region_id, acronym, region_info.name, parent_id, insert_datetime,
        insert_person, species.name as species_name, species_id
    FROM nhp.region_info
    join nhp.species on species.id = region_info.species_id
    WHERE nhp.species.name = %s and BINARY acronym in %s
    ''', (species, (names)))

    res = await cur.fetchall()
    return res

@app.get("/api/region-info")
async def get_region_names(
    species: str, 
    cur: DictCursor = Depends(get_db)
):
    await cur.execute('''
    SELECT
        r.id,
        r.region_id,
        r.acronym,
        r.name,
        r.parent_id,
        r.insert_datetime,
        r.insert_person,
        r.harmless,
        r.species_id,
        s.name as species_name, 
        GROUP_CONCAT(child.id) AS children
    FROM
        region_info AS r
        JOIN species AS s ON r.species_id = s.id
        LEFT JOIN region_info AS child ON r.id = child.parent_id
    WHERE
        s.name = %s
    GROUP BY
        r.id
    ORDER BY 
        r.acronym
    ;
    ''', (species,))


    res = await cur.fetchall()
    id_to_item = {i['id']: i for i in res}

    for item in res:
        item['_parent_id'] = item['parent_id']
        item['_id'] = item['id']
        # item['children'] = []

        if item['parent_id'] is None:
            parent_id = 0
            item['_parent_id'] = 0
        else:
            parent = id_to_item[item['parent_id']]
            parent_id = parent['region_id']
        item['parent_id'] = item['parent'] = parent_id
        if item['children']:
            children = [
                id_to_item[int(i)]
                for i in item['children'].split(',')
            ]
            children.sort(key=lambda x: x['name'])
            children = [i['region_id'] for i in children]
        else:
            children = []
        item['children'] = children
    return res

@dataclass
class RegionInfo:
    region_id: int
    acronym: str
    name: str
    parent_id: int | None
    species_name: str


@app.post("/api/region-info")
async def add_region_info(region: RegionInfo, cur: DictCursor = Depends(get_db)):
    # check if region_id exists
    await cur.execute('''
        SELECT * FROM region_info WHERE region_id = %s AND species_id = (SELECT id FROM species WHERE name = %s)
    ''', (region.region_id, region.species_name))
    res = await cur.fetchone()
    if res:
        return {'status': 'error', 'error': 'region_id exists'}

    await cur.execute('''
    INSERT INTO region_info (region_id, acronym, name, parent_id, species_id, insert_datetime, insert_person, harmless)
    VALUES (%s, %s, %s, %s, (SELECT id FROM species WHERE name = %s), NOW(), 'web', %s)
    ''', (region.region_id, region.acronym, region.name, region.parent_id, region.species_name, region.name))
    await cur.execute('''
    SELECT * FROM region_info WHERE region_id = %s AND species_id = (SELECT id FROM species WHERE name = %s)
    ''', (region.region_id, region.species_name))
    res = await cur.fetchone()

    return {'status': 'ok', 'region': res}

@app.put("/api/region-info/parent")
async def update_region_parent(
    id: int, 
    parent_id: int, 
    species_name: str,
    cur: DictCursor = Depends(get_db)
):
    await cur.execute('''
    UPDATE region_info SET parent_id = %s WHERE region_id = %s AND species_id = (SELECT id FROM species WHERE name = %s)
    ''', (parent_id, id, species_name))
    return {'status': 'ok'}


@app.get('/api/region-info-data-center')
async def get_region_info_data_center(species: str, cur: DictCursor = Depends(get_db)):
    await cur.execute('''
        SELECT ri.id AS _id, ri.parent_id AS _parent_id, 
            ri.region_id AS region_id, ri.acronym, ri.name, ri.insert_datetime, 
            p.region_id AS parent_id,
            ri.insert_person, ri.harmless, ri.species_id, 
            GROUP_CONCAT(DISTINCT c.region_id ORDER BY c.id ASC SEPARATOR '|') AS children_id_array
        FROM region_info AS ri
        LEFT JOIN region_info AS p ON ri.parent_id = p.id
        LEFT JOIN region_info AS c ON ri.id = c.parent_id
        LEFT JOIN species AS s ON ri.species_id = s.id
        WHERE s.name = %s
        GROUP BY region_id
    ''', (species,))
    res = await cur.fetchall()
    for item in res:
        item['children_id_array'] = item['children_id_array'].split('|') if item['children_id_array'] else []
        item['children_id_array'] = [int(i) for i in item['children_id_array']]
        item['file'] = f'{item["region_id"]}.stl'
        item['species'] = species

    return res
