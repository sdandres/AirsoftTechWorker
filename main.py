import gui.gui as gui
from tkinter import Tk

if __name__ == "__main__":
    window = Tk()

    window.geometry("1200x720")
    window.configure(bg = "#FFFFFF")
    gui.open_login_page(window)