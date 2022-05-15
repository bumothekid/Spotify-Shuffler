# Spotify playlist shuffler

Spotify playlist shuffler written in Python that gets all ID's of the tracks in the playlist, deletes all of them from the playlist then shuffles the array of ID's and adds them back in

## Usage

First, create a [Spotify application](https://developer.spotify.com/dashboard/applications).

Now set this environment variables in a `config.yml` file:

```yaml
client_id: "<Spotify application client ID>"
client_secret: "<Spotify application client secret>"
```

After the setup just run `python3 shuffle.py` and you should be ready to go.