import json
import os.path
import platform

CONFIG_FILE_NAME = "config.json"
INSTALLED_GAMES_FILE_NAME = "installed_games.json"
cloudfolder = ""

def expand_path(path):
	return os.path.expandvars(os.path.expanduser(path))

if platform.system() == "Windows":
	data_directory = "%LOCALAPPDATA%\\fuzzy-robot"
else:
	data_directory = "~/.fuzzy-robot"

data_directory = expand_path(data_directory)
	
def exists ():
	return os.path.exists(expand_path(os.path.join(data_directory, CONFIG_FILE_NAME)))
	
def load ():
	global filepath
	global cloudfolder
	filepath = expand_path(os.path.join(data_directory, CONFIG_FILE_NAME))
	with open(filepath) as configuration_file:
		config = json.load(configuration_file)
	cloudfolder = expand_path(config["cloudfolder"])

def save ():
	try:
		os.makedirs(data_directory)
	except FileExistsError:
		pass
	data = {"cloudfolder":cloudfolder}
	filepath = expand_path(os.path.join(data_directory, CONFIG_FILE_NAME))
	with open(filepath, 'w') as configuration_file:
		json.dump(data, configuration_file)
