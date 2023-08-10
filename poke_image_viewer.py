"""
Description:
  Graphical user interface that displays the official artwork for a
  user-specified Pokemon, which can be set as the desktop background image.

Usage:
  python poke_image_viewer.py
"""
from tkinter import *
from tkinter import ttk
import os
import poke_api
import image_lib
import ctypes
import inspect

# Get the script and images directory
script_name = inspect.getframeinfo(inspect.currentframe()).filename
script_dir = os.path.dirname(os.path.abspath(script_name))
images_dir = os.path.join(script_dir, 'images')

# Create the images directory if it does not exist
if not os.path.isdir(images_dir):
    os.makedirs(images_dir)

# Create the main window
root = Tk()
root.title("Pokemon Viewer")
root.geometry('600x600')
root.minsize(500, 600)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Set the icon
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('COMP593.PokeImageViewer')
root.iconbitmap(os.path.join(script_dir, 'poke_ball.ico'))

# Create frames
frm = ttk.Frame(root)
frm.columnconfigure(0, weight=1)
frm.rowconfigure(0, weight=1)
frm.grid(sticky=NSEW)

# Label to display the Pokémon image
lbl_image = ttk.Label(frm)
lbl_image.grid(row=0, column=0, padx=10, pady=10)

# Create a PhotoImage object to be used for displaying the image
photo = PhotoImage()
lbl_image['image'] = photo

# Event handler for the dropdown selection
def handle_poke_sel(event):
    global image_path

    current_sel = cbox_poke_sel.get()
    image_path = poke_api.download_pokemon_artwork(current_sel, images_dir)

    if image_path:
        lbl_image['text'] = None
        updated_photo = PhotoImage(file=image_path)
        lbl_image['image'] = updated_photo
        lbl_image.image = updated_photo
        btn_set_desktop.state('!Disabled')
    else:
        lbl_image['text'] = "Error downloading artwork."
        lbl_image['image'] = None
        btn_set_desktop.state('Disabled')

# Create a button to set the desktop background
def handle_set_desktop():
    image_lib.set_desktop_background_image(image_path)

btn_set_desktop = ttk.Button(frm, text='Set as Desktop Image', command=handle_set_desktop)
btn_set_desktop['state']='Disabled'
btn_set_desktop.grid(row=2, column=0, padx=10, pady=(10, 20))

# Create a dropdown menu for Pokémon names
pokemon_list = poke_api.get_all_pokemon_names()

pokemon_list.sort()
cbox_poke_sel = ttk.Combobox(frm, values=pokemon_list, state='readonly')
cbox_poke_sel.set("Select a Pokemon")
cbox_poke_sel.grid(row=1, column=0, padx=10, pady=10)
cbox_poke_sel.bind('<<ComboboxSelected>>', handle_poke_sel)

root.mainloop()