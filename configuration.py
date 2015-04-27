import json
import os.path
import platform
import urllib.request
from urllib.error import HTTPError

from game import Game


CONFIG_FILE_NAME = "config.json"
GAMES_FILE_NAME = "games.json"
INSTALLED_GAMES_FILE_NAME = "installed_games.json"
cloudfolder = ""
games = []


def expand_path(path):
    return os.path.expandvars(os.path.expanduser(path))


if platform.system() == "Windows":
    data_directory = "%LOCALAPPDATA%\\fuzzy-robot"
else:
    data_directory = "~/.fuzzy-robot"

data_directory = expand_path(data_directory)
game_images_folder = os.path.join(data_directory, "images")


def exists():
    return os.path.exists(expand_path(os.path.join(data_directory, CONFIG_FILE_NAME)))


def load():
    global games
    global cloudfolder
    filepath = expand_path(os.path.join(data_directory, CONFIG_FILE_NAME))
    with open(filepath) as configuration_file:
        config = json.load(configuration_file)
    cloudfolder = expand_path(config["cloudfolder"])
    games_file_path = os.path.join(data_directory, GAMES_FILE_NAME)
    if os.path.exists(games_file_path):
        with open(games_file_path) as games_file:
            games = [Game.create_from_json(game) for game in json.load(games_file)]
    else:
        update_games()


def save():
    try:
        os.makedirs(data_directory)
    except FileExistsError:
        pass
    data = {"cloudfolder": cloudfolder}
    filepath = expand_path(os.path.join(data_directory, CONFIG_FILE_NAME))
    with open(filepath, 'w') as configuration_file:
        json.dump(data, configuration_file)


def update_games():
    global games
    try:
        os.makedirs(game_images_folder)
    except FileExistsError:
        pass
    jsonstr = urllib.request.urlopen("https://raw.githubusercontent.com/manuelVo/fuzzy-robot/master/games.json").read().decode("utf-8")
    with open(os.path.join(data_directory, GAMES_FILE_NAME), "w") as games_file:
        games_file.write(jsonstr)
    games = [Game.create_from_json(game) for game in json.loads(jsonstr)]
    for game in games:
        image_file_name = os.path.join(game_images_folder, game.id + ".png")
        if not os.path.exists(image_file_name):
            try:
                image = urllib.request.urlopen("https://raw.githubusercontent.com/manuelVo/fuzzy-robot/master/images/" + game.id + ".png").read()
                with open(image_file_name, "wb") as image_file:
                    image_file.write(image)
            except HTTPError:
                pass