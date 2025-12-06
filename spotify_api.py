import spotipy
from spotipy.oauth2 import SpotifyOAuth


client_id = "VOTRE_CLIENT_ID"
client_secret = "VOTRE_CLIENT_SECRET"
redirect_uri = "http://localhost:8080/"
SCOPE = "user-read-playback-state user-modify-playback-state user-library-modify"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id='CLIENT_ID',
    client_secret="CLIENT_SECRET",
    redirect_uri="REDIRECT_URI",
    scope=SCOPE
))

def get_current_track():
    try:
        track = sp.current_playback()
    except Exception as e:
        print("Erreur Spotify API :", e)
        return {
            "name": None,
            "artist": None,
            "image": None,
            "is_playing": None,
            "raw_progress": 0,
            "raw_duration": 0
        }

    if not track or not track.get("item"):
        return {
            "name": None,
            "artist": None,
            "image": None,
            "is_playing": None,
            "raw_progress": 0,
            "raw_duration": 0
        }

    item = track["item"]

    return {
        "name": item["name"],
        "artist": ", ".join([a["name"] for a in item["artists"]]),
        "image": item["album"]["images"][0]["url"] if item["album"]["images"] else None,
        "is_playing": track.get('is_playing', False),
        "raw_progress": track.get("progress_ms", 0),
        "raw_duration": item.get("duration_ms", 0)
    }