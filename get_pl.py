import json  # Importing library to work with json

import requests  # Importing library to make http requests


class ArtistObject:
    def __init__(self, **kwargs):
        """
        Initializing ArtistObject
        :param kwargs: data about artist
        """
        self.artist_id = kwargs.get('artist_id')
        self.artist_name = kwargs.get('name')


class TrackObject:
    def __init__(self, **kwargs):
        """
        Initializing TrackObject
        :param kwargs: data about track
        """
        self.album_id = kwargs.get('album_id')
        self.album_name = kwargs.get('album_name')
        self.artists_list = kwargs.get('artists')
        self.id = kwargs.get('track_id')
        self.name = kwargs.get('track_name')


class PlaylistObject:
    def __init__(self, **kwargs):
        """
        Initializing PlaylistObject
        :param kwargs: data about playlist
        """
        self.playlist_id = kwargs.get('playlist_id')
        self.tracks_list = kwargs.get('tracks')
        self.image_url = kwargs.get('image')
        self.name = kwargs.get('name')
        self.owner_id = kwargs.get('owner_id')

    def from_dict(self, playlist_dict):
        """
        Fills Object with data from dict
        :param playlist_dict: dict with data
        """
        self.image_url = playlist_dict['images'][0]['url']
        self.playlist_id = playlist_dict['id']
        self.owner_id = playlist_dict['owner']['id']
        self.name = playlist_dict['name']
        self.tracks_list = tracks_from_list(playlist_dict['tracks']['items'])

    def from_id(self, playlist_id):
        """
        Fills Object with retrieved data
        :param playlist_id: unique identifier for playlist
        """
        playlist = get_playlist_info(playlist_id)
        self.from_dict(playlist)


def get_OAuth(secrets):
    """
    Gets OAuth access token
    :param secrets: file with base64 encoded ClientID:ClientSecret
    :return: access token
    """
    return requests.post("https://accounts.spotify.com/api/token",
                         headers={"Authorization": f"Basic {json.load(secrets)['IdAndSecret']}"},
                         data={'grant_type': "client_credentials"}).json()['access_token']


def tracks_from_list(items: list):
    """
    Parsing all tracks info
    :param items: list with all tracks data
    :return: list with TrackObjects
    """
    tracks = []
    for track_about in (i['track'] for i in items):
        tracks.append(TrackObject(album_id=track_about['album']['id'],
                                  album_name=track_about['album']['name'],
                                  track_id=track_about['id'],
                                  track_name=track_about['name'],
                                  artists=[ArtistObject(artist_id=artist['id'], name=artist['name']) for artist in
                                           track_about['artists']]))
    return tracks


def get_playlist_info(playlist_id):
    """
    Parsing data about playlist from spotify api
    :param playlist_id: unique playlist identifier
    :return: parsed dict
    """
    response = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}",
                            headers={'Authorization': f'Bearer {OAuth_token}'})
    return response.json()


with open('secrets.json') as file:
    OAuth_token = get_OAuth(secrets=file)  # Getting access token from IdAndEmail in secrets.json

if __name__ == "__main__":
    playlist_obj = PlaylistObject()  # Declaring instance
    playlist_obj.from_id(playlist_id='187a3FDc6isgauO5dG6Ivn')  # Filling object with data
    print(vars(playlist_obj))  # Showing object in readable format
