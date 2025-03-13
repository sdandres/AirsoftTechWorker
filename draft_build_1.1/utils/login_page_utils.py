from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
import gui.gui as gui

def validate_login(window, username, password):
    print(f"Username entered: '{username}'")
    print(f"Password entered: '{password}'")
    if username == "" and password == "":
        gui.clear_window(window)
        gui.open_main_menu(window)
        
    else:
        messagebox.showerror("Invalid Credentials", "Incorrect username or password.")

