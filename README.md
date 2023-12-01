# spotify-image-downloader

This is a simple command-line utility written in Python for downloading most Spotify images accessible through the Spotify Web API. API access requires a Spotify application, which in turn requires a user account. Follow the [Setup](#setup) instructions below.

## Setup

This tool requires Python 3 (3.8+ is preferable). Download the code with `git clone` or with `Download ZIP` (accessible with the green `Code` button).

1. Create a virtual environment (optional).

2. Run the command:

```
pip install -r requirements.txt
```

3. Package the script with [PyInstaller](https://pyinstaller.org/en/stable/) (optional).

### Spotify Application Setup

1. Register a Spotify account. If you are seeking to use this tool, then chances are, you already have one.

2. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard), and create a new application.

3. Populate the `App name`, `App description`, and `Redirect URI` fields. The `Redirect URI` field may be set to `http://localhost:3000`, for example.

4. Select the `Web API` to be used.

5. Read and agree to the Developer Terms of Service. Save the application.

6. Go to the application settings. You need the information here for the initial use of the script.

## First Use

Copy the `Client ID` and paste it in place of `CLIENT_ID` in the command below. Copy the `Client secret` and paste it in place of `CLIENT_SECRET` in the command below. Then go to Spotify and copy the URL of an artist, an album, a playlist, a user, or a track. Paste it in place of `URL` in the command below.

```commandLine
python spotify-image-downloader.py URL --client-id CLIENT_ID --client-secret CLIENT_SECRET
```

After the command completes successfully, `--client-id` and `--client-secret` need not be passed in subsequent runs, unless a change is desired or necessary.

## General Usage

```commandLine
usage: Simple command-line utility to download images for Spotify artists, albums, playlists, users, and tracks.

positional arguments:
  id                    URL or URI of the Spotify resource.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file.

authorization:
  --client-id CLIENT_ID
                        Spotify client ID. Only required on first run.
  --client-secret CLIENT_SECRET
                        Spotify client secret. Only required on first run.
  --one-time            Use the provided authorization without overwriting the saved configuration.
  --clear               Removes the current saved Spotify client configuration.
```

Pass `--one-time` along with the Spotify application information to use the provided information without overwriting the configuration saved in the 'config' file.

Pass `--clear` to delete the saved configuration from the 'config' file and then exit.

### Examples

**Downloading an image from a Spotify URL:**

```commandLine
python spotify-image-downloader.py "https://open.spotify.com/artist/0CGpNBihXlpMsjwHjVKNIO"
```

**Downloading an image from a Spotify URI:**

```commandLine
python spotify-image-downloader.py "spotify:artist:0CGpNBihXlpMsjwHjVKNIO"
```

**Specifying a custom output file:**

```commandLine
python spotify-image-downloader.py "spotify:artist:0CGpNBihXlpMsjwHjVKNIO" --output "./images/artist.jpg"
```
