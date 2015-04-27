from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import os.path
import platform

from PIL import Image, ImageTk

import savesync
import configuration as config


root = Tk()
root.title("Fuzzy Robot")
mainframe = Frame(root)
mainframe.grid(row=1, column=1, columnspan=2, sticky=(N, W, E, S))

if platform.system() == "Linux":
    ttk.Style().theme_use("alt")


def browse_cloudfolder():
    newdir = filedialog.askdirectory()
    if newdir != "":
        global cfolder
        cfolder.set(newdir)


def apply_cloudfolder():
    global cfolder
    folder = cfolder.get()
    if os.path.isdir(folder):
        config.cloudfolder = folder
        config.save()
        update()
        folderpicker.withdraw()
        root.deiconify()
    else:
        messagebox.showerror("Invalid folder", "The selected folder doesn't exist")


def draw_main_window():
    global mainframe
    global games
    mainframe.grid_forget()
    mainframe = Frame(root)
    mainframe.grid(row=1, column=1, columnspan=2, sticky=(N, W, E, S))
    if "games" not in globals():
        games = savesync.detect_games()
    for game in games:
        if savesync.is_synchronized(game):
            state = 'disabled'
        else:
            state = 'normal'
        if not hasattr(game, "selected"):
            game.selected = IntVar()
            game.selected.set(1)
        try:
            image = ImageTk.PhotoImage(Image.open(os.path.join(config.game_images_folder, game.id + ".png")).resize((32, 32), Image.ANTIALIAS))
        except FileNotFoundError:
            image = None
        checkbutton = ttk.Checkbutton(mainframe, variable=game.selected, image=image, text=game.name, compound=LEFT, takefocus=False, state=state)
        checkbutton.image = image
        checkbutton.grid(sticky=(W, E))
    pass


def synchronize():
    global games
    syncgames = [game for game in games if game.selected.get() == 1 and not savesync.is_synchronized(game)]
    for game in syncgames:
        if savesync.has_conflicts(game):
            if messagebox.askyesno("Savegame conflict", "Game '" + game.name + "' has local saves as well as synchronized saves. Do you want to overwrite the local saves with the synchronized saves?\n\n(No cancels synchronization for this game)"):
                savesync.remove_local_savegame(game)
            else:
                continue
        savesync.move_save_to_cloud(game)
    messagebox.showinfo("Synchronization done", "The selected games are now set up for synchronization and will store their saves in the specified folder.")
    draw_main_window()


def update():
    global games
    config.update_games()
    games = savesync.detect_games()
    draw_main_window()


Button(root, text="Synchronize selected", command=synchronize).grid(row=2, column=1, sticky=W)
Button(root, text="Update supported game list", command=update).grid(row=2, column=2, sticky=E)

cfolder = StringVar()
folderpicker = Toplevel()
folderpicker.title("Setup sync folder")
ttk.Label(folderpicker, text="Please select the folder to which you want your saves synchronized").grid(row=1, column=1, columnspan=2, sticky=(W, E))
ttk.Entry(folderpicker, exportselection=0, textvariable=cfolder).grid(row=2, column=1, sticky=(E, W))
ttk.Button(folderpicker, text="Browse...", command=browse_cloudfolder).grid(row=2, column=2, sticky=W)
ttk.Button(folderpicker, text="Ok", command=apply_cloudfolder).grid(row=3, column=2, sticky=E)

if config.exists():
    folderpicker.withdraw()
    config.load()
    draw_main_window()
else:
    root.withdraw()

root.mainloop()
