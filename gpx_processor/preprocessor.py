#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
© 2023 Yuto Noguchi
https://github.com/YutoGCN
'''

from geopy.distance import geodesic
import gpx_driver

def calculate_speed(track_points_df):
    speeds = []
    speeds.append(0)

    for i in range(1, len(track_points_df)):
        # 2つのトラックポイント間の距離を計算
        coords1 = (track_points_df['latitude'].iloc[i - 1], track_points_df['longitude'].iloc[i - 1])
        coords2 = (track_points_df['latitude'].iloc[i], track_points_df['longitude'].iloc[i])
        distance = geodesic(coords1, coords2).meters

        # 2つのトラックポイント間の時間を計算
        time1 = track_points_df['time'].iloc[i - 1]
        time2 = track_points_df['time'].iloc[i]
        time_interval = (time2 - time1).total_seconds()

        # 速度を算出 (単位: km/h)
        speed = (distance / time_interval) * 3600 / 1000
        speeds.append(speed)

    return speeds

# Example usage:
file_path = 'yamap_2022-07-29_08_17.gpx'
gpx_file = gpx_driver.GPXDriver(file_path)
df = gpx_file.get_track_points()
df['speeds'] = calculate_speed(df)
print(df)