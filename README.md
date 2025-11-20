# iPhone GPS Spoofer

**DISCLAIMER:** This project is intended strictly for educational, research, and development purposes. The techniques and code provided are designed to help developers simulate GPS locations in controlled environments for legitimate testing, debugging, or demonstration purposes. Misuse of this technology — such as employing it to deceive, commit fraud, or violate any local, state, or federal laws — is strictly prohibited. Always ensure that you comply with all applicable terms of service and legal regulations when using this tool.

## Overview

Spoof your iPhone's GPS location and simulate movement along routes using Xcode and Python. The project consists of an Xcode app that runs on your iPhone and a Python script that generates GPX files using the Google Maps API.

## Requirements

- Mac with Xcode
- iPhone with Developer Mode enabled
- Google Maps API key (free tier sufficient)
- Python 3 with `gpxpy` and `polyline` libraries

## Setup

### 1. Xcode Project

1. Create a new iOS App project in Xcode (SwiftUI), keep all the default code
2. Connect your iPhone via cable
3. Enable Developer Mode on iPhone: Settings → Privacy & Security → Developer Mode → Enable → Restart
4. Trust developer certificate: Settings → General → VPN & Device Management → Developer App
5. Run the empty app on your device to verify setup

### 2. Python Environment

Install required libraries:

```bash
pip3 install gpxpy polyline
```

### 3. Google Maps API

1. Get an API key from [Google Maps Platform](https://console.cloud.google.com/google/maps-apis)
2. Copy the .env.example to .env and add your API key:

```
GOOGLE_MAPS_API_KEY=YOUR_API_KEY_HERE
```

## Usage

1. Run the Python script and enter route details:

   ```
   Enter the origin address: CN Tower, Toronto, Ontario
   Enter the destination address: CF Toronto Eaton Centre
   Enter the number of hours to pause at the destination: 1
   ```

2. The script generates `route.gpx` at your specified path

3. In Xcode, with your app running on the device:

   - Go to Debug → Simulate Location → Add GPX File to Project
   - Select your generated `route.gpx` file
   - Choose the custom route from the dropdown

4. Your iPhone will now follow the simulated route

## Python Script Structure

The script includes functions to:

- `get_coordinates(address)` - Geocode addresses to lat/lng
- `get_route(origin, destination)` - Fetch driving directions
- `create_gpx(steps, destination_coords, pause)` - Generate GPX file with timestamps
- Simulate realistic movement speed and optional pause at destination

## Notes

- The iPhone must remain connected to Xcode and running the app for location spoofing to work
- You can use Apple's preset locations via Debug → Simulate Location without custom GPX files
- Update the `path` variable in the Python script to specify GPX output location

---

_This project was inspired by an article: [INSERT LINK HERE]_
