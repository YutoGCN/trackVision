#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import numpy as np
from datetime import datetime
from geopy.distance import geodesic

def parse_gpx(file_path):
    # GPX namespace
    ns = {'gpx': 'http://www.topografix.com/GPX/1/1'}
    
    # Parse the GPX file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Initialize lists to store data
    timestamps = []
    latitudes = []
    longitudes = []
    elevations = []
    speeds = []

    # Iterate through track points
    for trkpt in root.findall('.//gpx:trkpt', namespaces=ns):
        # Extract latitude and longitude
        latitude = float(trkpt.get('lat'))
        longitude = float(trkpt.get('lon'))

        # Extract elevation
        elevation = float(trkpt.find('gpx:ele', namespaces=ns).text)

        # Extract timestamp
        timestamp_str = trkpt.find('gpx:time', namespaces=ns).text
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%SZ')

        # Calculate speed
        if len(latitudes) > 0 and len(longitudes) > 0:
            distance = geodesic((latitudes[-1], longitudes[-1]), (latitude, longitude)).meters
            time_difference = (timestamp - timestamps[-1]).total_seconds()
            speed = distance / time_difference if time_difference > 0 else 0
            speeds.append(speed)
        else:
            speeds.append(0)

        # Append data to lists
        timestamps.append(timestamp)
        latitudes.append(latitude)
        longitudes.append(longitude)
        elevations.append(elevation)

    # Convert lists to NumPy arrays
    timestamps = np.array(timestamps)
    latitudes = np.array(latitudes)
    longitudes = np.array(longitudes)
    elevations = np.array(elevations)
    speeds = np.array(speeds)

    return timestamps, latitudes, longitudes, elevations, speeds

# Example usage:
file_path = 'yamap_2022-07-29_08_17.gpx'
timestamps, latitudes, longitudes, elevations, speeds = parse_gpx(file_path)

import csv

def save_to_csv(file_path, timestamps, latitudes, longitudes, elevations, speeds):
    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write header
        csv_writer.writerow(['Timestamp', 'Latitude', 'Longitude', 'Elevation', 'Speed'])

        # Write data
        for i in range(len(timestamps)):
            csv_writer.writerow([timestamps[i], latitudes[i], longitudes[i], elevations[i], speeds[i]])

# Example usage:
csv_file_path = 'output.csv'
save_to_csv(csv_file_path, timestamps, latitudes, longitudes, elevations, speeds)