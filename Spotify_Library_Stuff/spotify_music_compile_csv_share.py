import pandas as pd
import numpy as np
import csv
import os

def read_files(files, username):
    '''create a function that loops through each file and creates a dataframe for each author, song, tracking csv of individual user 
       after creating the dataframe add the username column with name of user 
    '''
    # call files
    filenames = files
    
    # create an empty list to store each csv as a dataframe
    dataframes = []
    
    # loop through each of the csvs and append to the list
    for filename in filenames:
        dataframes.append(pd.read_csv(filename))
        
    # join the dataframes    
    df = pd.concat([dataframes[0], dataframes[1], dataframes[2]], axis=1, join='inner')
    
    # append username
    df['username'] = username
    
    return df

def union_data(frames):
    '''create a function that compiles (i.e. unions) everyone's clean dataframes into multiple csvs by topics'''
    frames_list = frames
    df = pd.concat(frames_list)
    return df

# call functions
lina = read_files(['Authors_lina400.csv', 
                  'song_features_lina400.csv',
                  'Tracking_data_lina400.csv'], 'Lina')

anand = read_files(['Authors_anand400.csv',
                    'song_features_anand400.csv',
                    'Tracking_data_anand400.csv'], 'Anand')

andres = read_files(['Authors.csv',
                     'song_features.csv',
                     'Tracking_data.csv'], 'Andres')

df = union_data([lina, anand, andres])

# save df as csv for team members
# export_csv = df.to_csv('our_tracks.csv', index=None,header=True)