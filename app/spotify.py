import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Spotify client
spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
    )
)

def search_tracks(query: str, limit: int = 5):
    """Search for tracks on Spotify"""
    results = spotify.search(q=query, type='track', limit=limit)
    
    tracks = []
    for track in results['tracks']['items']:
        # Get the album image (medium size)
        album_image = track['album']['images'][1]['url'] if track['album']['images'] else None
        
        tracks.append({
            'id': track['id'],
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'album': track['album']['name'],
            'albumImage': album_image,
            'previewUrl': track['preview_url']
        })
    
    return tracks

def get_track_features(track_id: str):
    """Get audio features for a track"""
    features = spotify.audio_features(track_id)[0]
    return {
        'danceability': features['danceability'],
        'energy': features['energy'],
        'valence': features['valence'],
        'tempo': features['tempo'],
        'instrumentalness': features['instrumentalness']
    } 