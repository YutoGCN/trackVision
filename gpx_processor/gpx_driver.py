#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
© 2023 Yuto Noguchi
https://github.com/YutoGCN
'''

import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
import os

'''
purpose: gpx -> pandas.DataFrame
'''

class GPXDriver:
    ns ={'gpx': 'http://www.topografix.com/GPX/1/1'}

    def  __init__(self,file_path):
        tree = ET.parse(file_path)
        self.root = tree.getroot()
    
    def get_name(self):
        return self.root.find('.//gpx:name', namespaces=self.ns).text
    
    def get_track_points(self):
        data = []

        for track_point in self.root.findall('.//gpx:trkpt', namespaces=self.ns):
            latitude = float(track_point.attrib['lat'])
            longitude = float(track_point.attrib['lon'])
            elevation = float(track_point.find('.//gpx:ele', namespaces=self.ns).text)
            time = datetime.strptime(track_point.find('.//gpx:time', namespaces=self.ns).text,'%Y-%m-%dT%H:%M:%SZ')

            data.append({'latitude': latitude, 'longitude': longitude, 'elevation': elevation, 'time': time})

        df = pd.DataFrame(data)
        return df