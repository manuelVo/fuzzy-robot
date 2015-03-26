# Fuzzy Robot
A tool for synchronizing saves for games via synchronization services like Dropbox or OwnCloud

## Requirements
- python3
- python3-tkinter
- python3-pil (python image library or pillow)
- python3-imaging-tk (python image support for tkinter (might be included in python3-pil))

Installation of requirements for Ubuntuusers:

<pre>sudo apt-get install python3 python3-tk python3-pil python3-imaging-tk</pre>

## How to use
To run either double click *main.py* or execute

<pre>python3 main.py</pre>

On the first run the gamesync will ask for a folder. This will be the folder the save files will be stored in. Select a folder thats within a synchronized directory (for example your DropBox folder).

Afterwards the program will display a list of found games (it will only find those games which have already created save files though). Check the boxes next to the games you want synchronized and click on "Synchronize selected".

The games are now set up for synchronization. Synchronized games will be greyed-out. The games will now automatically synchronize without the need of having the tool opened.

## Adding more games
Currently the database of games is quite small. However adding games is simple. Just edit *games.json*

Add an entry for your game which looks like this:
<pre>{
	"id": "example_game",
	"name": "Example Game",
	"files": [
		{
			"directory": true,
			"name": "Savefiles",
			"locations": {
				"Linux": "~/.examplegame/Savefiles",
				"Windows": "%APPDATA%\\examplegame\\Savefiles"
			}
		}
  ]
},</pre>

- **id** is the uniqe indentifier for this game. It should be the same as the full game name in only lowercase letters with an underscore ( _ ) to seperate words
- **name** is the name of the game players will normally see (for example in the main menu or on the box)
- **directory** indicates wheter the given location is a directory or a file (*true* for directory, *false* for file)
- **name** is the name under which the file/directory will be synchronized. Ideally this is the same name as the local file/directory. However each name is only allowed once per game.
- **locations** lists the locations at which the file/directory is stored in different operating systems. The name the operating system ist the one returned by the pyhton call *system.platform()*

To add an image for the game save it as *game_id.png* into the *images/* folder.

## TODO
### General
- Build release packages

### Backend
- Add support for old games which put their save files into their installation folder instead of the user folder
- Add support for games using the steam cloud
- Add an option to revert games back from synchronized state to local saving

### Frontend
- Get rid of tkinter
- Make list of found games scrollable
- Gui for linux which looks less crappy
- Add an option to change the synchronization folder
- Better conflict resolution dialog
