import yaml
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth

try:
    with open("config.yml", "r") as f:
        config = yaml.load(f, yaml.FullLoader)

    client_id = config["client_id"]
    client_secret = config["client_secret"]

    if not client_id or not client_secret or client_id in ["", " "] or client_secret in ["", " "]:
        raise RuntimeError("Please provide a valid client_id and valid client_secret in the config.yml file")

except FileNotFoundError as e:
    raise FileNotFoundError("Please create a config.yml file with a client_id and client_secret") from e

except KeyError as e:
    raise KeyError("Please check your configuration file and set the client_id and client_secret variable") from e


tokenInfo = "token_info"
authorization = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:8888/callback",
        scope="playlist-read-collaborative playlist-read-private playlist-modify-private playlist-modify-public"
    )

user = spotipy.Spotify(auth_manager=authorization)

def shufflePlaylistsByURI(playlistURI: str) -> bool:
    playlistID = playlistURI.split(":")[2]

    try:
        user.playlist(playlistID)
    except Exception:
        return False
    
    tracks = []
    offset = 0

    while True:
        items = user.user_playlist_tracks(user=user, playlist_id=playlistID, limit=100, offset=offset)['items']
        tracks.extend(
            item['track']['uri']
            for item in items
            if item['track']['uri'].split(":")[1] in ["track", "episode"]
        )

        offset += 100

        if len(items) != 100:
            break
    
    user.playlist_remove_all_occurrences_of_items(playlistID, tracks)
    random.shuffle(tracks)
    offset = 0

    while True:
        to_add = tracks[offset:offset+100]
        user.user_playlist_add_tracks(user, playlistID, to_add)

        offset += 100

        if len(to_add) != 100:
            break

    return True


if __name__ == "__main__":
    sampleURI = "spotify:playlist:2UKqwpfrKKZrLFBncodK4L"
    playlistURI = input(f"The playlist URI to shuffle: (Sample URI: {sampleURI})\n")

    if len(playlistURI.split(":")) != 3 or playlistURI.split(":")[1] != "playlist":
        raise ValueError("PlaylistURI invalid")
    
    success = shufflePlaylistsByURI(playlistURI)

    if not success:
        raise RuntimeError("An error occoured while shuffling the playlist")
    
    print("The playlist has been shuffled successfully")