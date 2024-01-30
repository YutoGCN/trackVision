#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
© 2023 Yuto Noguchi
https://github.com/YutoGCN
'''

from geopy.distance import geodesic
import gpx_driver
import matplotlib as mpl
import matplotlib.pyplot as plt

class processor:
    def rest_detection(df, threshold=239):
        # if time_diff > threshold, rest = True
        df['time_diff'] = df['time'].diff().dt.total_seconds()
        df['rest'] = df['time_diff'] > threshold

class graph_visualization:
    def plot_track_with_rest(df):
        plt.scatter(df[~df['rest']]['longitude'], df[~df['rest']]['latitude'], color='blue', label='Rest False')
        plt.scatter(df[df['rest']]['longitude'], df[df['rest']]['latitude'], color='red', label='Rest True')
        for i, txt in enumerate(df[df['rest']]['time_diff']):
            plt.annotate(txt, (df[df['rest']]['longitude'].iloc[i], df[df['rest']]['latitude'].iloc[i]), textcoords="offset     points", xytext=(20,10), ha='center')

        # プロットの設定
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Track with Rest Plot')
        plt.legend()

        # csv out
        csv_data = df[df['rest']][['longitude', 'latitude', 'time_diff']].to_csv(index=False)
        print(csv_data)

        # プロットを表示
        plt.show()    

if __name__ == '__main__':
    # file_path = 'yamap_2022-07-29_08_17.gpx'
    # file_path = 'yamap_2023-12-28_08_51.gpx'
    file_path = 'yamap_2023-07-29_05_24.gpx'
    gpx_file = gpx_driver.GPXDriver(file_path)
    df = gpx_file.get_track_points()
    rest_threshold = 100
    processor.rest_detection(df, rest_threshold)
    print(df)

    df.to_csv('output.csv', index=False)

    graph_visualization.plot_track_with_rest(df)