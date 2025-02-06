from flask import Flask, render_template, jsonify, request
import folium
import webview
import threading

app = Flask(__name__)

# Robot and goal locations
robot_location = {"lat": 38.3753855364, "lon": -110.8302205892}

# takes a 2d array in the form lat lon
def set_goals(x):
    global goal_locations
    goal_locations = []
    for i in x:
        goal_locations.append({"lat": i[0], "lon": i[1], "name": "Goal " + str(x.index(i) + 1)})

# goal_locations = [
#     {"lat": 38.376, "lon": -110.832, "name": "Goal 1"},
#     {"lat": 38.374, "lon": -110.828, "name": "Goal 2"},
# ]

@app.route("/")
def home():
    return render_template("map.html")

@app.route("/get_location")
def get_location():
    """Returns the current robot location as JSON."""
    return jsonify(robot_location)

@app.route("/update_location", methods=["POST"])
def update_location():
    """Updates the robot's location via a POST request."""
    global robot_location
    data = request.json
    robot_location["lat"] = data.get("lat", robot_location["lat"])
    robot_location["lon"] = data.get("lon", robot_location["lon"])
    return jsonify({"message": "Location updated!"})

@app.route("/get_goals")
def get_goals():
    """Returns goal locations."""
    return jsonify(goal_locations)


# Function to generate the map.html file
def generate_map():
    m = folium.Map(location=[robot_location["lat"], robot_location["lon"]], zoom_start=12)

    # Add robot marker (this will be updated dynamically)
    folium.Marker(
        location=[robot_location["lat"], robot_location["lon"]],
        popup="Robot",
        icon=folium.Icon(color="blue")
    ).add_to(m)

    # Add goal markers
    for goal in goal_locations:
        folium.Marker(
            location=[goal["lat"], goal["lon"]],
            popup=goal["name"],
            icon=folium.Icon(color="red")
        ).add_to(m)

    m.save("templates/map.html")

# Run Flask in a separate thread so it doesn't block Tkinter
def run_flask():
    #IMPORTANT  generate_map() - must manually generate the map on the fist run then change map.html - DO THIS
    app.run(debug=True, port=5000, use_reloader=False)

# Run the GUI
def run_gui():
    webview.create_window("Robot Tracker", "http://127.0.0.1:5000/")
    webview.start()

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    run_gui()

