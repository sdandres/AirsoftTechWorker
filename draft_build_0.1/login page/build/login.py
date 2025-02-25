from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, StringVar, Label
from tkinter import messagebox
import subprocess
import sys
import mainmenu

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\\Users\\hamza\\Documents\\homework\\draft_build_0.1\\login page\\build\\assets\\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def validate_login():
    password = entry_1.get().strip()
    username = entry_2.get().strip()
    print(f"Username entered: '{username}'")  # Debug statement
    print(f"Password entered: '{password}'")  # Debug statement
    if username == "admin" and password == "password":
        messagebox.showinfo("Login Successful", "Welcome!")
        window.destroy()
        open_mainmenu()
    else:
        messagebox.showerror("Invalid Credentials", "Incorrect username or password.")

def open_mainmenu():
    subprocess.Popen([sys.executable, "mainmenu.py"])  # Open mainmenu.py from the same folder

window = Tk()
window.geometry("1200x720")
window.configure(bg="#FFFFFF")
window.title("Login Page")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=720,
    width=1200,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
canvas.create_image(918.0, 483.0, image=entry_image_1)
entry_1 = Entry(
    bd=0,
    bg="#D0D0D0",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(x=768.0, y=458.0, width=300.0, height=48.0)

entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
canvas.create_image(918.0, 404.0, image=entry_image_2)
entry_2 = Entry(
    bd=0,
    bg="#D0D0D0",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(x=768.0, y=379.0, width=300.0, height=48.0)

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(918.0, 225.0, image=image_image_1)

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=validate_login,
    relief="flat"
)
button_1.place(x=843.0, y=547.0, width=150.0, height=50.0)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
canvas.create_image(309.0, 360.0, image=image_image_2)

canvas.create_text(768.0, 350.0, anchor="nw", text="Password", fill="#000000", font=("MergeOne Regular", 24 * -1))
canvas.create_text(768.0, 432.0, anchor="nw", text="Username", fill="#000000", font=("MergeOne Regular", 24 * -1))

window.resizable(False, False)
window.mainloop()
