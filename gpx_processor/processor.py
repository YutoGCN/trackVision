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
import pandas as pd

class processor:
    def rest_detection(df, threshold=239):
        """
        Detect rest points from track points
        
        Parameters
        ----------
        df : pandas.DataFrame
            DataFrame of track points
        threshold : int [s]
        """
        df['time_diff'] = df['time'].diff().dt.total_seconds()
        df['rest'] = df['time_diff'] > threshold

    def calc_reach_node(track_df,threshold=30):
        """
        Calculate the reach node of each track point

        Parameters
        ----------
        track_df : pandas.DataFrame
            DataFrame of track points
        threshold : int [m]
        """

        nodelist = pd.read_csv('nodelist.csv')
        track_df['reach'] = None

        for track_index, track_row in track_df.iterrows():
            for _, node_row in nodelist.iterrows():
                # Iterate over each row in the nodelist
                distance = geodesic((track_row['latitude'], track_row['longitude']), (node_row['latitude'], node_row['longitude'])).meters
                if distance < threshold:
                    df.at[track_index, 'reach'] = node_row['name']
                    break

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
    # file_path = 'gpx_files/yamap_2022-07-29_08_17.gpx'
    # file_path = 'gpx_files/yamap_2023-12-28_08_51.gpx'
    file_path = 'gpx_files/yamap_2023-07-29_05_24.gpx'
    gpx_file = gpx_driver.GPXDriver(file_path)
    df = gpx_file.get_track_points()

    rest_threshold = 100 # [s]
    reach_node_threshold = 30 # [m]
    processor.rest_detection(df, rest_threshold)
    processor.calc_reach_node(df, 30)
    pd.set_option('display.max_rows', None)
    print(df)