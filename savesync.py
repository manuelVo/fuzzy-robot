import os
import os.path
import shutil
import platform

import configuration as config


def detect_games():
    games = config.games
    detected_games = []
    for game in games:
        game_found = False
        if os.path.exists(os.path.join(config.cloudfolder, game.id)):
            for file in game.files:
                if platform.system() in file.locations:
                    game_found = True
        else:
            for file in game.files:
                try:
                    path = config.expand_path(file.locations[platform.system()])
                except KeyError:
                    continue
                if os.path.exists(path):
                    game_found = True
                    break
        if game_found:
            game.is_synchronized = is_synchronized(game)
            detected_games.append(game)
    return detected_games


def move_save_to_cloud(game):
    path_in_cloud = config.expand_path(os.path.join(config.cloudfolder, game.id))
    if os.path.exists(path_in_cloud):
        for file in game.files:
            try:
                original_filepath = config.expand_path(file.locations[platform.system()])
                filepath_in_cloud = config.expand_path(os.path.join(path_in_cloud, file.name))

                try:
                    os.makedirs(os.path.dirname(original_filepath))
                except FileExistsError:
                    pass
                os.symlink(filepath_in_cloud, original_filepath, file.directory)
            except KeyError:
                pass
    else:
        for file in game.files:
            os.mkdir(path_in_cloud)
            try:
                original_filepath = config.expand_path(file.locations[platform.system()])
                filepath_in_cloud = config.expand_path(os.path.join(path_in_cloud, file.name))

                shutil.move(original_filepath, filepath_in_cloud)
                os.symlink(filepath_in_cloud, original_filepath, file.directory)
            except KeyError:
                pass


def unsync_save(game, keep_in_cloud):
    path_in_cloud = config.expand_path(os.path.join(config.cloudfolder, game.id))
    for file in game.files:
        original_filepath = original_filepath = config.expand_path(file.locations[platform.system()])
        filepath_in_cloud = config.expand_path(os.path.join(path_in_cloud, file.name))
        os.remove(original_filepath)
        if keep_in_cloud:
            shutil.copytree(filepath_in_cloud, original_filepath)
        else:
            shutil.move(filepath_in_cloud, original_filepath)
    if not keep_in_cloud:
        os.rmdir(path_in_cloud)


def is_synchronized(game):
    path_in_cloud = config.expand_path(os.path.join(config.cloudfolder, game.id))
    for file in game.files:
        try:
            original_filepath = config.expand_path(file.locations[platform.system()])
            filepath_in_cloud = config.expand_path(os.path.join(path_in_cloud, file.name))
            if not (os.path.exists(original_filepath) and os.path.exists(filepath_in_cloud) and os.path.islink(original_filepath) and os.path.abspath(os.readlink(original_filepath)) == os.path.abspath(filepath_in_cloud)):
                return False
        except KeyError:
            pass
    return True


def has_conflicts(game):
    path_in_cloud = config.expand_path(os.path.join(config.cloudfolder, game.id))
    if os.path.exists(path_in_cloud):
        for file in game.files:
            try:
                original_filepath = config.expand_path(file.locations[platform.system()])
                filepath_in_cloud = config.expand_path(os.path.join(path_in_cloud, file.name))

                if os.path.exists(original_filepath) and os.path.exists(filepath_in_cloud) and (not os.path.islink(original_filepath) or os.readlink(original_filepath) != filepath_in_cloud):
                    return True
            except KeyError:
                pass
    return False


def remove_local_savegame(game):
    for file in game.files:
        try:
            original_filepath = config.expand_path(file.locations[platform.system()])
            if os.path.isdir(original_filepath):
                shutil.rmtree(original_filepath)
            else:
                os.remove(original_filepath)
        except KeyError:
            pass


def remove_cloud_savegame(game):
    path_in_cloud = config.expand_path(os.path.join(config.cloudfolder, game.id))
    shutil.rmtree(path_in_cloud)


def move_game_to_other_cloud(game, new_cloud):
    new_path = os.path.join(new_cloud, game.id)
    shutil.move(os.path.join(config.cloudfolder, game.id), new_path)
    if game.is_synchronized:
        for file in game.files:
            link_location = config.expand_path(file.locations[platform.system()])
            os.remove(link_location)
            os.symlink(os.path.join(new_path, file.name), link_location, file.directory)
