import spotipy
from spotipy.oauth2 import SpotifyOAuth 
import matplotlib.pyplot as plt


SPOTIPY_CLIENT_ID = 'CLIENT ID'
SPOTIPY_CLIENT_SECRET = 'CLIENT SECRET'
SPOTIPY_REDIRECT_URI = 'URI'
SCOPE = 'playlist-read-private'

def authenticate_spotify():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE,
        cache_path="cache/.cache"
    ))
    return sp

def get_user_playlists(sp):
    playlists = sp.current_user_playlists(limit=20)
    return playlists

def get_playlist_tracks(sp, playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']


    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    return tracks


def analyze_playlist_tracks(tracks):
    for item in tracks:
        track = item['track']
        print(f"Track: {track['name']}, Popularity: {track['popularity']}")


def plot_popularity(tracks):
    popularity = [track['track']['popularity'] for track in tracks]
    plt.hist(popularity, bins=10, color='skyblue')
    plt.title('Track Popularity Distribution')
    plt.xlabel('Popularity')
    plt.ylabel('Frequency')
    plt.show()

def plot_audio_features(sp, tracks):
    track_ids = [track['track']['id'] for track in tracks]
    features = sp.audio_features(track_ids)
    
    energy = [f['energy'] for f in features]
    danceability = [f['danceability'] for f in features]
    
    plt.scatter(danceability, energy, color='purple')
    plt.title('Danceability vs Energy')
    plt.xlabel('Danceability')
    plt.ylabel('Energy')
    plt.show()


def main():
    sp = authenticate_spotify()
    
    print("Fetching your playlists...")
    playlists = get_user_playlists(sp)
    
    for i, playlist in enumerate(playlists['items']):
        print(f"{i + 1}. {playlist['name']} - {playlist['tracks']['total']} tracks")
    
    choice = int(input("Select a playlist to analyze (enter number): ")) - 1
    selected_playlist = playlists['items'][choice]
    
    print(f"Analyzing '{selected_playlist['name']}'...")
    tracks = get_playlist_tracks(sp, selected_playlist['id'])
    analyze_playlist_tracks(tracks)
    plot_audio_features(sp,tracks)
    plot_popularity(tracks) 


if __name__ == "__main__":
    main()
