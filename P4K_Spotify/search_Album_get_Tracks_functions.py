#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Credentials

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials  # To access authorised Spotify data
import json
import time
import numpy as np
import pandas as pd


client_id_input = 'XXX'
client_secret_input = 'XXX'

client_id = client_id_input
client_secret = client_secret_input
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)  # spotify object to access API

# In[2]:


# Get album names, artist names for search

# call the function wih these defined


# In[3]:


def Find_Albums(album_name_lst, artist_name_lst):
    """
    Takes album names, artist names and looks them up on spotify to return the album URI's.
    """
    Spotify_Albums = {}  # empty dictionary to store album info

    # iterate through the albums
    for n in range(len(album_name_lst)):
        album_name = album_name_lst[n]
        artist_name = artist_name_lst[n]

        if " EP" in album_name:
            album_name_q = album_name.replace(" EP", "")
        elif " LP" in album_name:
            album_name_q = album_name.replace(" LP", "")
        else:
            album_name_q = album_name
        # look up the album
        query = f'album:{album_name_q} artist:{artist_name}'

        # search(q, limit=10, offset=0, type='track', market=None)
        temp_album = sp.search(q=query, type='album', limit=1)
        #         print(json.dumps(temp_album, indent=4, ensure_ascii=False))  # reading back from JSON

        # check if the found album's name is 2x longer than our search
        if temp_album['albums']['total'] != 0:  # if we found an album
            album_name_temp = temp_album['albums']['items'][0]['name']
            if len(album_name_temp) >= 2*len(album_name_q):
                # This name is too long (2x length of our search), assume we matched the wrong album and try for an exact
                # match to the album name. It's okay if we don't find the album.
                query = f'album:"{album_name_q}" artist:{artist_name}'

                # search(q, limit=10, offset=0, type='track', market=None)
                temp_album = sp.search(q=query, type='album', limit=1)
                #         print(json.dumps(temp_album, indent=4, ensure_ascii=False))  # reading back from JSON
        else:
            # just try this search if we don't have a match at all
            query = f'album:"{album_name_q}" artist:{artist_name}'

            # search(q, limit=10, offset=0, type='track', market=None)
            temp_album = sp.search(q=query, type='album', limit=1)
            #         print(json.dumps(temp_album, indent=4, ensure_ascii=False))  # reading back from JSON

        if temp_album['albums']['total'] != 0:  # if we found an album
            artist_name_temp = temp_album['albums']['items'][0]['artists'][0]['name']
            if len(artist_name_temp) >= 2*len(artist_name):
                # This name is too long (2x length of our search), assume we matched the wrong album and try for an exact
                # match to the artist name. It's okay if we don't find the album look up the album
                query = f'album:"{album_name_q}" artist:"{artist_name}"'

                # search(q, limit=10, offset=0, type='track', market=None)
                temp_album = sp.search(q=query, type='album', limit=1)
                #         print(json.dumps(temp_album, indent=4, ensure_ascii=False))  # reading back from JSON
        else:
            # just try this search if we don't have a match at all
            query = f'album:"{album_name_q}" artist:"{artist_name}"'

            # search(q, limit=10, offset=0, type='track', market=None)
            temp_album = sp.search(q=query, type='album', limit=1)
            #         print(json.dumps(temp_album, indent=4, ensure_ascii=False))  # reading back from JSON

        # get the album's uri:
        if temp_album['albums']['total'] != 0:
            temp_album_uri = temp_album['albums']['items'][0]['uri']
            #             print(temp_album_uri)
            #     temp_album_returned = sp.album(temp_album_uri)
            #     print(json.dumps(temp_album_returned, indent=4, ensure_ascii=False))  # reading back from JSON

            Spotify_Albums[temp_album_uri] = {}
            Spotify_Albums[temp_album_uri]['album_name'] = album_name
            Spotify_Albums[temp_album_uri]['artist_name'] = artist_name
            Spotify_Albums[temp_album_uri]['album_uri'] = temp_album_uri
            Spotify_Albums[temp_album_uri]['album_release_date'] = temp_album['albums']['items'][0]['release_date']


        else:
            print(f'No album found: Name: {album_name}, Artist: {artist_name}')
    return Spotify_Albums


# ## Get the Album's URI and add it to a list of URI's found




# ## Get Tracks from Each Album
#
# Here we get the tracks from each album

# In[5]:


# Grab songs from each album

def albumSongs(uri, spotify_albums: dict):
    """
    Function to take an album URI and found_albums dictionary, and add tracks field to each album filled with track info.
    """

    album = uri  # assign album uri to a_name
    spotify_albums[album]['tracks'] = {}  # Creates dictionary for that specific album's tracks

    # Create keys-values of empty lists inside nested dictionary for album
    spotify_albums[album]['tracks']['album'] = []  # create empty list for album names for each track
    spotify_albums[album]['tracks']['album_uri'] = []  # create empty list for album uris for each track
    spotify_albums[album]['tracks']['album_artist'] = []  # create empty list for artist name ON THE ALBUM, NOT TRACK
    spotify_albums[album]['tracks']['track_number'] = []
    spotify_albums[album]['tracks']['id_track'] = []
    spotify_albums[album]['tracks']['name_track'] = []
    spotify_albums[album]['tracks']['uri_track'] = []

    tracks = sp.album_tracks(album)  # pull data on album tracks
    for n in range(len(tracks['items'])):  # for each song track
        spotify_albums[album]['tracks']['album'].append(spotify_albums[album]["album_name"])
        spotify_albums[album]['tracks']['album_uri'].append(album)
        spotify_albums[album]['tracks']['album_artist'].append(spotify_albums[album]["artist_name"])
        spotify_albums[album]['tracks']['track_number'].append(tracks['items'][n]['track_number'])
        spotify_albums[album]['tracks']['id_track'].append(tracks['items'][n]['id'])
        spotify_albums[album]['tracks']['name_track'].append(tracks['items'][n]['name'])
        spotify_albums[album]['tracks']['uri_track'].append(tracks['items'][n]['uri'])






# ## Grab audio features for each song
#
# Here we add additional key-values to store the audio features of each album track and append the data into lists
# representing all the music tracks for that album.

# In[8]:


def audio_features(album_uri, spotify_albums: dict):
    """
    Takes in found_albums dictionary, adds audio features to each album's tracks under 'tracks' as a list.
    """
    album = album_uri
    # Add new key-values to store audio features
    spotify_albums[album]['tracks']['acousticness'] = []
    spotify_albums[album]['tracks']['danceability'] = []
    spotify_albums[album]['tracks']['energy'] = []
    spotify_albums[album]['tracks']['instrumentalness'] = []
    spotify_albums[album]['tracks']['liveness'] = []
    spotify_albums[album]['tracks']['loudness'] = []
    spotify_albums[album]['tracks']['speechiness'] = []
    spotify_albums[album]['tracks']['tempo'] = []
    spotify_albums[album]['tracks']['valence'] = []
    spotify_albums[album]['tracks']['popularity'] = []
    spotify_albums[album]['tracks']['duration_ms'] = []
    spotify_albums[album]['tracks']['is_explicit'] = []
    # create a track counter
    track_count = 0
    for track in spotify_albums[album]['tracks']['uri_track']:
        # pull audio features per track
        features = sp.audio_features(track)

        # Append to relevant key-value
        spotify_albums[album]['tracks']['acousticness'].append(features[0]['acousticness'])
        spotify_albums[album]['tracks']['danceability'].append(features[0]['danceability'])
        spotify_albums[album]['tracks']['energy'].append(features[0]['energy'])
        spotify_albums[album]['tracks']['instrumentalness'].append(features[0]['instrumentalness'])
        spotify_albums[album]['tracks']['liveness'].append(features[0]['liveness'])
        spotify_albums[album]['tracks']['loudness'].append(features[0]['loudness'])
        spotify_albums[album]['tracks']['speechiness'].append(features[0]['speechiness'])
        spotify_albums[album]['tracks']['tempo'].append(features[0]['tempo'])
        spotify_albums[album]['tracks']['valence'].append(features[0]['valence'])
        # popularity is stored elsewhere
        pop = sp.track(track)
        spotify_albums[album]['tracks']['popularity'].append(pop['popularity'])
        spotify_albums[album]['tracks']['duration_ms'].append(pop['duration_ms'])
        spotify_albums[album]['tracks']['is_explicit'].append(pop['explicit'])
        track_count += 1


# ## Loop through albums extracting the audio features
#
# We will need to add a random delay every few albums to avoid sending too many requests at Spotify’s API. We will
# also set up print statements to track which album we are on incase we encounter errors and want to know where in
# the data it happened.

# In[9]:





def Add_Track_AudioFeatures(spotify_albums: dict):
    """
    Pass in Found_Albums dict with tracks added to them. Adds audio features to each track looping through.
    """
    sleep_min = 2
    sleep_max = 5
    start_time = time.time()
    request_count = 0
    for i in spotify_albums:
        audio_features(i, spotify_albums)
        request_count += 1
        if request_count % 5 == 0:
            print(str(request_count) + " playlists completed")
            time.sleep(np.random.uniform(sleep_min, sleep_max))
            print('Loop #: {}'.format(request_count))
            print('Elapsed Time: {} seconds'.format(time.time() - start_time))





# ## Add data to a new dataframe
# We will organise our data into a dictionary which can more easily be turned into a dataframe.

# In[11]:


def create_df_dict(spotify_albums: dict):
    dic_df = {}

    for feature_key in spotify_albums[list(spotify_albums.keys())[0]]['tracks']:
        dic_df[feature_key] = []
    for album in spotify_albums:
        for feature in spotify_albums[album]['tracks']:
            dic_df[feature].extend(spotify_albums[album]['tracks'][feature])

    len(dic_df['album'])
    return dic_df




# ## Collapse the dataframe to album rows
#
# 1) Each album's tracks should have the features averaged or summed as appropriate
#
# 2) Each row will correspond to 1 album and the average features for its tracks
#
# 3) Each row will correspond to an album that Pitchfork reviewed
#
#



# In[17]:


def combine_albums(final_df: pd.DataFrame):
    """
    Combine albums by album_uri,
    """
    # Define the aggregation procedure outside of the groupby operation
    aggregations = {
        'album': 'first',
        'album_artist': 'first',
        'acousticness': 'mean',
        'danceability': 'mean',
        'energy': 'mean',
        'instrumentalness': 'mean',
        'liveness': 'mean',
        'loudness': 'mean',
        'speechiness': 'mean',
        'tempo': 'mean',
        'valence': 'mean',
        'popularity': 'mean',
        'duration_ms': 'sum',
        'is_explicit': 'sum'
    }
    combined_albums_df = final_df.groupby('album_uri', as_index=False).agg(aggregations)
    return combined_albums_df




