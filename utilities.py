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
    img = mpimg.imread('MDRS-Map.png')
    plt.imshow(img)

    points = path # [[50, 100],[100, 150],[150,200]] - Example points

    x_points = [point[0] for point in points]
    y_points = [point[1] for point in points]
    #Z value is ignored

    # Plot the points on top of the image
    plt.scatter(x_points, y_points, color='red', s=20, marker='o')  # Red points with size 20

    plt.show()
