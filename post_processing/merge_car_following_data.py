#!/usr/bin/env python
from __future__ import print_function

# Import libraries
import pandas as pd
import numpy as np
import geopy.distance
import os

def merge_dataframes(dict_cars):
    
    dict_cars_new = dict_cars.copy()
    n_cars = len(dict_cars_new)

    # Prepare the merging
    for car in dict_cars_new:
        dict_cars_new[car]['timestamp'] = pd.to_datetime(dict_cars[car]['timestamp'],
                                                         format = '%Y-%m-%d %H:%M:%S.%f')
        dict_cars_new[car].index = dict_cars_new[car]['timestamp']
        dict_cars_new[car] = dict_cars_new[car].resample('s').mean()
        
        # Interpolate GPS coordinates to avoid NaNs
        dict_cars_new[car]['latitude_deg'] = dict_cars_new[car]['latitude_deg'].interpolate() 
        dict_cars_new[car]['longitude_deg'] = dict_cars_new[car]['longitude_deg'].interpolate() 
        
        
    # Start the merging process for all the vehicles in the platoon    
    if n_cars == 2:
        suffixes = ('_lead', '_following')
        merged_dataframe = pd.merge(dict_cars_new['car 1'], dict_cars_new['car 2'],
                                    how='inner',
                                    left_index=True, right_index=True,
                                    suffixes=suffixes)
        gps_dist = np.zeros([len(merged_dataframe), ])
        for i in range(len(merged_dataframe)):
            try:
                gps_dist[i] = geopy.distance.vincenty((merged_dataframe['latitude_deg_lead'].iloc[i],
                                                       merged_dataframe['longitude_deg_lead'].iloc[i]),
                                                      (merged_dataframe['latitude_deg_following'].iloc[i],
                                                       merged_dataframe['longitude_deg_following'].iloc[i])).m
            except ValueError:
                gps_dist[i] = 0
        merged_dataframe['gps_dist_car1_car2'] = gps_dist

    elif n_cars == 3:
        suffixes = ('_lead', '_middle', '_following')
        merged_dataframe = pd.merge(dict_cars_new['car 1'],
                                    dict_cars_new['car 2'],
                                    dict_cars_new['car 3'],
                                    how='inner',
                                    left_index=True, right_index=True,
                                    suffixes=suffixes)
        gps_dist_1 = np.zeros([len(merged_dataframe), ])
        gps_dist_2 = np.zeros([len(merged_dataframe), ])
        for i in range(len(merged_dataframe)):
            try:
                gps_dist_1[i] = geopy.distance.vincenty((merged_dataframe['latitude_deg_lead'].iloc[i],
                                                         merged_dataframe['longitude_deg_lead'].iloc[i]),
                                                        (merged_dataframe['latitude_deg_middle'].iloc[i],
                                                         merged_dataframe['longitude_deg_middle'].iloc[i])).m
            except ValueError:
                gps_dist_1[i] = 0
            try:
                gps_dist_2[i] = geopy.distance.vincenty((merged_dataframe['latitude_deg_middle'].iloc[i],
                                                         merged_dataframe['longitude_deg_middle'].iloc[i]),
                                                        (merged_dataframe['latitude_deg_following'].iloc[i],
                                                         merged_dataframe['longitude_deg_following'].iloc[i])).m
            except ValueError:
                gps_dist_2[i] = 0    
                
        merged_dataframe['gps_dist_car1_car2'] = gps_dist_1
        merged_dataframe['gps_dist_car2_car3'] = gps_dist_2
    else:
        raise ValueError("This function can only merge two or three vehicle platoon")
    
    return merged_dataframe



if __name__ == "__main__":
    
    # Number of cars that you want to merge
    df_cars = {}
    base_path = os.path.dirname(__file__)
 
    car1 = os.path.join(base_path, "example_raw_data/ford_f150_test_1.csv")
    car2 = os.path.join(base_path, "example_raw_data/mazda_cx9_test_1.csv")

    df_cars['car 1'] = pd.read_csv(car1)
    df_cars['car 2'] = pd.read_csv(car2)
    
    merged_dataframe = merge_dataframes(df_cars)
    merged_dataframe.to_csv('example_merged_data.csv')

    
    



