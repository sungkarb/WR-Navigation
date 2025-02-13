import folium 
import pandas as pd
from rrt import RRT

df = pd.read_csv("csv/box8.csv")


start = (38.420426831190305, -110.77523436806995)
end = (38.42708847868464, -110.79555161312287)
map = folium.Map(location=start, zoom_start=13)


df = pd.read_csv("csv/box8.csv")
algorithm = RRT(data=df)
path = algorithm.find_path(start, end, show_path=True)

for i in range(0, len(path), 100):
    lat, lon = path[i]
    folium.Marker([lat, lon], popup=f"{lat}, {lon}").add_to(map)


map.save("map.html")
