import numpy as np
from enum import Enum


def _to_b36(num: float):
    return np.base_repr(num, 36)


def _from_b36(value):
    return int(value, 36)


def encode_hash(
    lat: float,
    lng: float,
    heading: float,
    pitch: float,
    panzoom: float,
    mapzoom: float,
    splitpos: str,
):
    lat_36 = _to_b36(round(lat * 1000000))
    lng_36 = _to_b36(round(lng * 1000000))

    heading_36 = _to_b36(round(heading))
    pitch_36 = _to_b36(round(pitch))

    panzoom_36 = _to_b36(round(panzoom * 10))
    mapzoom_36 = _to_b36(round(mapzoom))

    return (
        f"{lat_36}_{lng_36}_{heading_36}.{panzoom_36}_{pitch_36}{mapzoom_36}{splitpos}"
    )


def decode_hash(hash_str: str):
    # Split the hash into parts
    parts = hash_str.split("_")
    lat_str, lng_str = parts[0], parts[1]
    heading_pan_str = parts[2].split(".")
    heading_str, panzoom_str = heading_pan_str[0], heading_pan_str[1]
    pitch_mapzoom_split_str = parts[3]

    # Extract pitch, mapzoom, and splitpos
    pitch_str = pitch_mapzoom_split_str[:-2]
    mapzoom_str = pitch_mapzoom_split_str[-2]
    splitpos = pitch_mapzoom_split_str[-1]

    # Convert from base 36 to decimal
    lat = _from_b36(lat_str) / 1000000
    lng = _from_b36(lng_str) / 1000000
    heading = _from_b36(heading_str)
    pitch = _from_b36(pitch_str)
    panzoom = _from_b36(panzoom_str) / 10
    mapzoom = _from_b36(mapzoom_str)

    return lat, lng, heading, pitch, panzoom, mapzoom, splitpos


# NOTE: maybe we can add some randomness to the coordinates
def generate_global_grid(start_lat, start_lng, lat_divisions, lng_divisions):
    lat_range = (-90, 90)
    lng_range = (-180, 180)

    lat_step = (lat_range[1] - lat_range[0]) / lat_divisions
    lng_step = (lng_range[1] - lng_range[0]) / lng_divisions

    coordinates = []
    for i in range(lat_divisions):
        for j in range(lng_divisions):
            lat = start_lat + i * lat_step
            lng = start_lng + j * lng_step

            if lat > lat_range[1]:
                lat = lat_range[1]
            if lng > lng_range[1]:
                lng = lng_range[1]

            coordinates.append((lat, lng))

    return coordinates


print(decode_hash("i3keo_1qm2iu_43.7_b506"))
