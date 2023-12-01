import numpy as np


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
def generate_coordinates(
    start_lat, start_lng, end_lat, end_lng, lat_divisions, lng_divisions
):
    """
    Generates a coordinates as a list of tuples within the specified area.

    Parameters:
    start_lat (float): Starting latitude.
    start_lng (float): Starting longitude.
    end_lat (float): Ending latitude.
    end_lng (float): Ending longitude.
    lat_divisions (int): Number of subdivisions in latitude.
    lng_divisions (int): Number of subdivisions in longitude.

    Returns:
    list of tuples: A list of coordinates representing the grid.
    """
    # Calculate the step sizes
    lat_step = (end_lat - start_lat) / lat_divisions
    lng_step = (end_lng - start_lng) / lng_divisions

    # Generate ranges for latitudes and longitudes
    latitudes = np.arange(start_lat, end_lat, lat_step)
    longitudes = np.arange(start_lng, end_lng, lng_step)

    # Ensure that the end values are included
    latitudes = np.append(latitudes, end_lat)
    longitudes = np.append(longitudes, end_lng)

    # Create a meshgrid of coordinates
    lat_grid, lng_grid = np.meshgrid(latitudes, longitudes, indexing="ij")

    # Convert to list of tuples
    grid_tuples = [(lat, lng) for lat, lng in zip(lat_grid.ravel(), lng_grid.ravel())]

    return grid_tuples

import geopandas as gpd
import shapely.geometry as geom
import random

# Function to generate a random point on land
def generate_random_point_on_land(land_gdf):
    while True:
        # Generate random latitude and longitude
        latitude = random.uniform(-66, 90)
        longitude = random.uniform(-180, 180)

        # Create a point geometry
        point = geom.Point(longitude, latitude)

        # Check if the point is on land
        if land_gdf.geometry.intersects(point).any():
            return (latitude, longitude)

