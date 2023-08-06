# %%
from dataclasses import dataclass
from datetime import datetime
from typing import Literal

import geojson
from numpy import ndarray
from serde import deserialize, field
from shapely.geometry import LineString, Polygon, shape


def with_geojson(initer):
    return lambda x: initer(shape(geojson.loads(x)))

LineStringWGJ = with_geojson(LineString)
PolygonWGJ = with_geojson(Polygon)


@deserialize
@dataclass
class NTPLine:
    linetype: int
    closed: bool # 闭合是 region, 开放是 mark
    line: LineString = field(deserializer=LineStringWGJ)

@deserialize
@dataclass
class NTPLabel:
    name: str
    position: tuple[float, float]

@deserialize
@dataclass
class NTPRegion:
    label: NTPLabel
    polygon: Polygon = field(deserializer=PolygonWGJ)
    area: float = 0

@deserialize
@dataclass
class NTPRegionWarnings:
    单标无区: list[NTPLabel]

    悬线: list[LineString] = field(deserializer=lambda x: [LineStringWGJ(i) for i in x])
    切线: list[LineString] = field(deserializer=lambda x: [LineStringWGJ(i) for i in x])
    劣线: list[LineString] = field(deserializer=lambda x: [LineStringWGJ(i) for i in x])
    单区多标: list[tuple[Polygon, list[NTPLabel]]] = field(
        deserializer=lambda x: [
            (PolygonWGJ(i[0]), [NTPLabel(*j.values()) for j in i[1]]) 
            for i in x
        ]
    )
    单区无标: list[Polygon] = field(deserializer=lambda x: [PolygonWGJ(i) for i in x])


T_SIZE_SOURCE = Literal['ntp', 'background', 'manual']
T_COLOR_SOURCE = Literal['green', 'red', 'blue', 'yellow']

@deserialize
@dataclass
class SliceMeta:
    date: datetime
    ntp_path: str
    bin_size: int
    um_per_pixel: float
    background_path: str
    w: int
    h: int
    size_source: T_SIZE_SOURCE
    ignore_regions: list[str]
    transpose: bool
    warnings: NTPRegionWarnings

    regions: list[NTPRegion]

    raw_labels: list[tuple[str, tuple[float, float]]]
    raw_lines: list[NTPLine]

    cells: dict[T_COLOR_SOURCE, ndarray] = field(default_factory=lambda: {
        'green': [], 'red': [], 'blue': [], 'yellow': []
    })
    ntp_version: str = 'none'
