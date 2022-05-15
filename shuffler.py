import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth

tokenInfo = "token_info"
authorization = SpotifyOAuth(
        client_id="", # Your Client ID here
        client_secret="", # Your Client Secret here
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
    print(tracks)
    random.shuffle(tracks)
    print(tracks)
    offset = 0

    while True:
        to_add = tracks[offset:offset+100]
        user.user_playlist_add_tracks(user, playlistID, to_add)

        offset += 100

        if len(to_add) != 100:
            break

    return True


if __name__ == "__main__":
    sampleURI = "spotify:playlist:2UKjwdfbKRZrYSOncodK4L"
    playlistURI = input(f"The playlist URI to shuffle: (Sample URI: {sampleURI})\n")

    if len(playlistURI.split(":")) != 3 or playlistURI.split(":")[1] != "playlist" or playlistURI == sampleURI:
        raise ValueError("PlaylistURI invalid")
    
    success = shufflePlaylistsByURI(playlistURI)

    if not success:
        raise RuntimeError("An error occoured while shuffling the playlist")
    
    print("The playlist has been shuffled successfully")