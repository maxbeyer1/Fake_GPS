"""
Main script to create GPX file
"""
import datetime
import random
import os
import requests
import gpxpy
import gpxpy.gpx
import polyline
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Maps API key
API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')


def get_coordinates(address):
    """Get latitude and longitude of an address using Google Geocoding API."""
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        raise Exception(f"Error fetching coordinates: {data['status']}")


def get_route(origin, destination):
    """Get route between two coordinates using Google Directions API."""
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&departure_time=now&key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'OK':
        return data['routes'][0]['legs'][0]['steps']
    else:
        raise Exception(f"Error fetching route: {data['status']}")


def decode_polyline(polyline_str):
    """Decode a polyline that is encoded using Google's algorithm."""
    return polyline.decode(polyline_str)


def create_gpx(steps, destination_coords, pause):
    """Create a GPX file from the route steps using waypoints (wpt) with timestamps.
    pause parameter is in minutes."""
    gpx = gpxpy.gpx.GPX()
    current_time = datetime.datetime.now()

    for step in steps:
        # Decode the polyline for the step to get intermediate points
        polyline_points = decode_polyline(step['polyline']['points'])
        # Get the duration of the step
        step_duration = step['duration']['value']  # duration in seconds

        for point in polyline_points:
            gpx.waypoints.append(gpxpy.gpx.GPXWaypoint(
                point[0], point[1], time=current_time))
            # Increment the current time by the appropriate duration divided by the number of points
            current_time += datetime.timedelta(
                seconds=step_duration / len(polyline_points))

    # Add the final destination as the last waypoint
    gpx.waypoints.append(gpxpy.gpx.GPXWaypoint(
        destination_coords[0], destination_coords[1], time=current_time))

    # Add additional waypoints at the destination to simulate a pause
    pause_duration = pause * 60
    num_pause_points = pause

    for _ in range(num_pause_points):
        current_time += datetime.timedelta(
            seconds=pause_duration / num_pause_points)
        altered_coords = destination_coords[0] + 0.00000001 * random.random(
        ), destination_coords[1] + 0.00000001 * random.random()
        gpx.waypoints.append(gpxpy.gpx.GPXWaypoint(
            altered_coords[0], altered_coords[1], time=current_time))
    return gpx


def main():
    """
    Run this file
    """
    origin_address = input("Enter the origin address: ")
    destination_address = input("Enter the destination address: ")
    pause = int(
        input("Enter the number of minutes to pause at the destination: "))
    # Get coordinates for origin and destination
    origin_coords = get_coordinates(origin_address)
    destination_coords = get_coordinates(destination_address)
    # Get route steps
    steps = get_route(f"{origin_coords[0]},{origin_coords[1]}",
                      f"{destination_coords[0]},{destination_coords[1]}")
    # Create GPX file
    gpx = create_gpx(steps, destination_coords, pause)
    # Save GPX file
    with open("route.gpx", "w", encoding="utf-8") as f:
        f.write(gpx.to_xml())
    print("GPX file created successfully: route.gpx")


if __name__ == "__main__":
    main()
