from tkinter import messagebox
import gui.gui as gui

def validate_login(window, username, password):
    print(f"Username entered: '{username}'")
    print(f"Password entered: '{password}'")
    if username == "testaccount" and password == "checkeredflag":
        gui.clear_window(window)
        gui.open_main_menu(window)
        
    else:
        messagebox.showerror("Invalid Credentials", "Incorrect username or password.")

