import laspy, os
import numpy as np
import pandas as pd
from pyproj import Transformer

GPS_CRS="EPSG:4326"
POINT_CRS="EPSG:32612"

"""
This function converts the given points to GPS coordinates.
param points: The points to convert.
param source_crs: The source coordinate reference system (CRS).

return: np.ndarray: The GPS coordinates.
"""
def to_gps(points: np.ndarray, source_crs=POINT_CRS) -> np.ndarray:
    transformer = Transformer.from_crs(source_crs, GPS_CRS, always_xy=True)
    result = np.array([transformer.transform(x, y, z) for x, y, z in points])
    result[:, [0, 1]] = result[:, [1, 0]]
    return result


"""
This function converts the laz file to the dataframe of gps coordinates
and saves it in csv

Args:
    box_file: path to the box file which must be laz file
"""
def box_to_gps(box_file: str, result_name=None) -> np.ndarray:
    if not result_name:
        result_name = box_file + ".csv"
        
    with laspy.open(box_file) as f:
        las = f.read()

    points = np.vstack((las.x, las.y, las.z)).transpose()
    crs = las.header.parse_crs()
    if crs:
        print("Coordinate Reference System (CRS):", crs)
    else:
        crs = POINT_CRS

    transformer = Transformer.from_crs(crs, GPS_CRS, always_xy=True)
    gps_cords = np.array([transformer.transform(x, y, z) for x, y, z in points])
    gps_cords[:, [0, 1]] = gps_cords[:, [1, 0]]

    df = pd.DataFrame(gps_cords, columns=["Latitude", "Longtitude", "Altitude"])
    df.to_csv(result_name, index=False)
    print(f"GPS coordinates saved to {result_name}")
