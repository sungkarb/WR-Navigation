import requests
import time
import random
import rospy
from sensor_msgs.msg import NavSatFix  # Standard ROS GPS message type

server_url = "http://127.0.0.1:5000/update_location"

# Starting position near the original marker
latitude = 38.3753855364
longitude = -110.8302205892

# ------------------------------------------test code -------------------------------------------

# def get_new_position():
#     """Generate a small random movement from the current position."""
#     global latitude, longitude
#     latitude += random.uniform(-0.005, 0.005)  # Small latitude shift
#     longitude += random.uniform(-0.005, 0.005)  # Small longitude shift
#     return {"lat": latitude, "lon": longitude}

# while True:
#     location = get_new_position()
#     response = requests.post(server_url, json=location)
    
#     if response.status_code == 200:
#         print(f"Updated location: {location}")
#     else:
#         print("Error updating location:", response.text)

#     time.sleep(1)  # Send an update every 2 seconds

# ---------------------------------------- ros code ----------------------------------------------

def gps_callback(msg):
    """Callback function that sends GPS data to the server whenever a new message arrives."""
    location = {"lat": msg.latitude, "lon": msg.longitude}

    try:
        response = requests.post(server_url, json=location)
        if response.status_code == 200:
            rospy.loginfo(f"Updated location: {location}")
        else:
            rospy.logwarn(f"Error updating location: {response.text}")
    except requests.exceptions.RequestException as e:
        rospy.logerr(f"Failed to send data: {e}")

def listener():
    """Initialize the ROS node and subscribe to the GPS topic."""
    rospy.init_node('gps_uploader', anonymous=True)
    
    # Subscribe to a GPS topic (Change '/gps/fix' to match your actual topic)
    rospy.Subscriber('/gps/fix', NavSatFix, gps_callback)

    # Keep the node running
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass



