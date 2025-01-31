"""
This function converts the given points to GPS coordinates.
param points: The points to convert.
param source_crs: The source coordinate reference system (CRS).

return: np.ndarray: The GPS coordinates.
"""
def to_gps(points: np.ndarray, source_crs="EPSG32612") -> np.ndarray:
    transformer = Transformer.from_crs(source_crs, "EPSG:4326", always_xy=True)
    return np.array([transformer.transform(x, y, z) for x, y, z in points])
