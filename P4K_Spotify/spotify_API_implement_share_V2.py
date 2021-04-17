import csv
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def Merge(dict1, dict2):
    return (dict2.update(dict1))


# https://stackoverflow.com/a/63759037
def get_all_saved_tracks(user: spotipy.client.Spotify, limit_step=50, track_limit=100):
    tracks = []
    for offset in range(0, track_limit, limit_step):
        response = user.current_user_saved_tracks(
            limit=limit_step,
            offset=offset,
        )
        # print(response)
        if len(response) == 0:
            break
        tracks.extend(response['items'])
    results_return = {'items': tracks}
    return results_return


# https://spotipy.readthedocs.io/en/2.17.1/#api-reference

# ENTER CREDS:
client_id_input = ''
client_secret_input = ''
redirect_uri_input = ''
scope_input = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id_input,
                                               client_secret=client_secret_input,
                                               redirect_uri=redirect_uri_input,
                                               scope=scope_input))

###Analyzing the last 100 songs that I saved on my spotify account
results = get_all_saved_tracks(sp, limit_step=50, track_limit=100)
print(results.keys())
print(type(results))



my_tracks = [['added_at_playlist', 'uri', 'name', 'popularity', 'duration_ms', 'is_explicit', 'album_name',
              'album_release_date']]

for songs in range(len(results['items'])):
    my_tracks.append([results['items'][songs]['added_at'],
                      results['items'][songs]['track']['uri'],  ##Identifier to find more information about the track
                      results['items'][songs]['track']['name'],
                      results['items'][songs]['track']['popularity'],
                      results['items'][songs]['track']['duration_ms'],
                      results['items'][songs]['track']['explicit'],
                      results['items'][songs]['track']['album']['name'],
                      results['items'][songs]['track']['album']['release_date']])

##Information about the artist- Some songs can have more than two artists
artists = [['artists', 'artists_id']]
for songs in range(len(results['items'])):
    artist_info = results['items'][songs]['track']['artists']
    if len(artist_info) == 1:
        artists.append([artist_info[0]['name'],
                        artist_info[0]['uri']])
    else:
        various_artists = []
        various_artist_names = []
        various_artist_uris = []
        for names in range(len(artist_info)):
            # various_artists.append([artist_info[names]['name'], artist_info[names]['uri']])
            various_artist_names.append(artist_info[names]['name'])
            various_artist_uris.append(artist_info[names]['uri'])
        various_artists = [various_artist_names, various_artist_uris]
        artists.append(various_artists)

###Information about the track
track_ids = []
for track_id in my_tracks:
    track_ids.append(track_id[1])

song_features = [
    ['uri', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness',
     'liveness', 'valence', 'tempo']]
for ids in track_ids[1:]:
    audio_features = sp.audio_features(tracks=[ids])  ##Search on the API
    song_features.append([
        ids,
        audio_features[0]['danceability'],
        audio_features[0]['energy'],
        audio_features[0]['key'],
        audio_features[0]['loudness'],
        audio_features[0]['mode'],
        audio_features[0]['speechiness'],
        audio_features[0]['acousticness'],
        audio_features[0]['instrumentalness'],
        audio_features[0]['liveness'],
        audio_features[0]['valence'],
        audio_features[0]['tempo']])

TrackFiles = open('Tracking_data.csv', 'wt', encoding="utf-8", newline='')
csvout = csv.writer(TrackFiles)
csvout.writerows(my_tracks)
TrackFiles.close()

authors = open('Authors.csv', 'wt', encoding="utf-8", newline='')
csvout = csv.writer(authors)
csvout.writerows(artists)
authors.close()

features = open('song_features.csv', 'wt', encoding="utf-8", newline='')
csvout = csv.writer(features)
csvout.writerows(song_features)
features.close()
