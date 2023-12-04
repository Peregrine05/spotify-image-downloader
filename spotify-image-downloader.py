import argparse
import dotenv
import os

import requests
import spotipy


CLIENT_ID_ENV = "SPOTIPY_CLIENT_ID"
CLIENT_SECRET_ENV = "SPOTIPY_CLIENT_SECRET"

script_path = os.path.dirname(os.path.realpath(__file__))
if script_path.endswith("_internal"):
    script_path = script_path[:-9]
workdir = os.getcwd()
os.chdir(script_path)
config_file_path = "config"


def parse_id(resource):
    if "/" in resource:
        # Spotify URL

        if "spotify.com/" not in resource:
            raise ValueError("The provided URL is not a valid Spotify URL.")
        
        type_and_id = resource.partition("spotify.com/")[2].partition("/")

        resource_type = type_and_id[0]
        resource_id = type_and_id[2].partition("?")[0]

    elif ":" in resource:
        # Spotify URI

        if "spotify:" not in resource:
            raise ValueError("The provided URI is not a valid Spotify URI.")
        
        split = resource.split(":")

        resource_type = split[1]
        resource_id = split[2]

    else:
        raise ValueError("The provided input does not resolve to a valid "
                         "Spotify resource.")

    return resource_type, resource_id


def get_images(
        resource_type,
        resource_id,
        images,
        spotify_client_id,
        spotify_client_secret
):
    client = spotipy.Spotify(
        auth_manager=spotipy.oauth2.SpotifyClientCredentials(
            client_id=spotify_client_id,
            client_secret=spotify_client_secret
        )
    )

    if resource_type == "album":
        resource = client.album(resource_id)
    elif resource_type == "artist":
        resource = client.artist(resource_id)
    elif resource_type == "playlist":
        resource = client.playlist(resource_id)
    elif resource_type == "track":
        resource = client.track(resource_id)["album"]
    elif resource_type == "user":
        resource = client.user(resource_id)

    images.extend(
        sorted(
            resource["images"],
            key=(lambda x:
                int(x["width"]) if x["width"] is not None
                else 0 * int(x["height"]) if x["height"] is not None else 0),
            reverse=True
        )
    )


def main():
    dotenv.load_dotenv(dotenv_path=config_file_path)

    spotify_client_id = os.getenv(CLIENT_ID_ENV)
    spotify_client_secret = os.getenv(CLIENT_SECRET_ENV)

    parser = argparse.ArgumentParser(
        prog="spotify-image-downloader",
        description="Simple command-line utility to download images for "
                    "Spotify artists, albums, playlists, users, and tracks."
    )
    parser.add_argument(
        "id",
        type=str,
        help="URL or URI of the Spotify resource."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        required=False,
        help="Output file."
    )
    authorization = parser.add_argument_group("authorization")
    authorization.add_argument(
        "--client-id",
        required=spotify_client_id is None,
        help="Spotify client ID. Only required on first run."
    )
    authorization.add_argument(
        "--client-secret",
        required=spotify_client_secret is None,
        help="Spotify client secret. Only required on first run."
    )
    authorization.add_argument(
        "--one-time",
        action="store_true",
        help="Use the provided authorization without overwriting the saved "
        "configuration."
    )
    authorization.add_argument(
        "--clear",
        action="store_true",
        help="Removes the current saved Spotify client configuration."
    )

    args = parser.parse_args()

    if args.clear:
        with open(config_file_path, "wt") as config_file:
            config_file.write(f'{CLIENT_ID_ENV} = \n{CLIENT_SECRET_ENV}: \n')
        return None

    is_new_config = (args.client_id is not None
                     or args.client_secret is not None)
    if is_new_config:
        if args.client_id is not None:
            spotify_client_id = args.client_id
        if args.client_secret is not None:
            spotify_client_secret = args.client_secret

    resource_type, resource_id = parse_id(args.id)
    images = []

    try:
        get_images(resource_type,
                   resource_id,
                   images,
                   spotify_client_id,
                   spotify_client_secret)
    except spotipy.oauth2.SpotifyOauthError as e:
        return print(e)
    except spotipy.exceptions.SpotifyException:
        return print(f"The resource at URL / URI: \"{args.id}\" could not be "
                     f"retrieved. If the resource is a playlist, it must be "
                     f"public before its data can be retrieved.")

    largest_image = images[0]
    
    if args.output is not None:
        directory, file_name = os.path.split(args.output)
        if len(directory):
            try:
                os.makedirs(directory)
                os.chdir(directory)
            except FileExistsError:
                pass
    else:
        file_name = largest_image["url"].split("/")[-1] + ".jpg"

    image = requests.get(largest_image["url"])
    os.chdir(workdir)
    with open(file_name, "wb") as out_file:
        out_file.write(image.content)
    os.chdir(script_path)
    
    if is_new_config and not args.one_time:
        with open(config_file_path, "wt") as config_file:
            config_file.write(
                f"{CLIENT_ID_ENV} = {spotify_client_id}\n"
                f"{CLIENT_SECRET_ENV} = {spotify_client_secret}\n"
            )


if __name__ == "__main__":
    main()
