"""Converts point read from csv file to coordinate system specified by 'crs' variable

Args:
    point: point with coordinates (x, y, z)
    crs: coordinate system to convert to

Returns:
    new point with coordinates translated to crs system
"""
def convert_coordinates(point: list, crs) -> list:
    raise NotImplementedError

"""Plot the path on the map of Mars Desert Research Station. 
   Account for differences in geographical coordinate systems.    
   
Args:
    path: list of points on the path from some point A to point B. Each element of the list is 
          a point with coordinates (x, y, z) 
"""
def map_points(path: list[list]):
    raise NotImplementedError
