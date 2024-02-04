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
            [latitude   longitude   elevation   time]
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
            [latitude   longitude   elevation   time    time_diff   rest]
        threshold : int [m]
        """

        nodelist = pd.read_csv('nodelist.csv')
        track_df['reach'] = None

        rough_threshold = 0.00001098901 * threshold # 1m = 0.00001098901

        for track_index, track_row in track_df.iterrows():
            for _, node_row in nodelist.iterrows():
                # Iterate over each row in the nodelist
                if (track_row['latitude'] - rough_threshold < node_row['latitude'] < track_row['latitude'] + rough_threshold):
                    if(track_row['longitude'] - rough_threshold < node_row['longitude'] < track_row['longitude'] + rough_threshold):
                        distance = geodesic((track_row['latitude'], track_row['longitude']), (node_row['latitude'], node_row['longitude'])).meters
                        if distance < threshold:
                            df.at[track_index, 'reach'] = node_row['name']
                            break

    class sequence_generator:
        def calc_time(df):
            if len(df) == 0:
                return pd.DataFrame(columns=['node_name', 'arrival_time', 'departure_time'])

            sequence_list = []

            current_node = df.iloc[0]['reach']
            arrival_time = None
            departure_time = df.iloc[0]['time']

            for _, row in df.iterrows():
                if row['reach'] is not None:
                    if row['reach'] != current_node or row['reach'] is None:
                        sequence_list.append([current_node, arrival_time, departure_time])
                        current_node = row['reach']
                        arrival_time = row['time']
                    else:
                        departure_time = row['time']

            # Add the last track segment
            sequence_list.append([current_node, arrival_time, None])

            return pd.DataFrame(sequence_list, columns=['node_name', 'arrival_time', 'departure_time'])
    
    
        def calc_sequence(sequence_df,track_df):
            sequence_time_list = []
            sequence_time_list.append([0, 0, 0])
            for index_sequence_df, row in sequence_df.iterrows():
                if index_sequence_df == 0:
                    continue
                if row['node_name'] is None:
                    continue

                if row['departure_time'] is None:
                    rest_time_inside_node = 0
                else:
                    rest_time_inside_node = (row['departure_time'] - row['arrival_time']).total_seconds()

                rest_time_outside_node = 0
                walk_start_time = sequence_df.iloc[index_sequence_df-1]['departure_time']
                walk_end_time = row['arrival_time']
                walk_start_time_index = track_df[track_df['time'] == walk_start_time].index[0]
                walk_end_time_index = track_df[track_df['time'] == walk_end_time].index[0]
                for index_track_df in range(walk_start_time_index+1, walk_end_time_index):
                    if track_df.iloc[index_track_df]['rest']:
                        rest_time_outside_node += track_df.iloc[index_track_df]['time_diff']

                
                walk_time = (walk_end_time - walk_start_time).total_seconds() - rest_time_outside_node

                sequence_time_list.append([rest_time_outside_node/60, rest_time_inside_node/60, walk_time/60])
            return pd.merge(sequence_df, pd.DataFrame(sequence_time_list, columns=['rest_time_outside_node', 'rest_time_inside_node', 'walk_time']), left_index=True, right_index=True)
        
        def gen(df):
            """
            Generate track sequence dataframe from track points

            Parameters
            ----------
            df : pandas.DataFrame
                [latitude   longitude   elevation   time    time_diff   rest    reach]

            Returns
            -------
            df : pandas.DataFrame
                [node_name  arrival_time    departure_time  rest_time_outside_node  rest_time_inside_node   walk_time]
            """
            sequence_df = processor.sequence_generator.calc_time(df)
            return processor.sequence_generator.calc_sequence(sequence_df, df)
        

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
    data_read = open(file_path, 'r', encoding="utf-8")
    data_read_str = data_read.read()

    calc_gpx_driver = gpx_driver.GPXDriver()
    gpx_file = calc_gpx_driver.open_string(data_read_str)
    df = calc_gpx_driver.get_track_points()

    rest_threshold = 239 # [s]
    reach_node_threshold = 50 # [m]
    processor.rest_detection(df, rest_threshold)
    processor.calc_reach_node(df, reach_node_threshold)
    # pd.set_option('display.max_rows', None)
    # print(df)
    sequence_df = processor.sequence_generator.gen(df)
    print(sequence_df)
