from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, StringVar, Label, Text
from tkinter import messagebox

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH_LOGIN = OUTPUT_PATH / Path(r"C:\\Users\\hamza\\Documents\\homework\\draft_build_0.1\\login page\\build\\assets\\frame0")
ASSETS_PATH_MAINMENU = OUTPUT_PATH / Path(r"C:\Users\hamza\Documents\homework\draft_build_0.1\main_menu\build\assets\frame0")

def relative_to_assets(path: str, menu: str = "login") -> Path:
    return (ASSETS_PATH_MAINMENU if menu == "mainmenu" else ASSETS_PATH_LOGIN) / Path(path)

def validate_login():
    username = entry_2.get().strip()
    password = entry_1.get().strip()
    print(f"Username entered: '{username}'")
    print(f"Password entered: '{password}'")
    if username == "admin" and password == "password":
        messagebox.showinfo("Login Successful", "Welcome!")
        window.destroy()
        open_mainmenu()
    else:
        messagebox.showerror("Invalid Credentials", "Incorrect username or password.")

def open_mainmenu():
    mainmenu_window = Tk()
    mainmenu_window.geometry("1200x720")
    mainmenu_window.configure(bg="#FFFFFF")
    mainmenu_window.title("Main Menu")

    canvas = Canvas(
        mainmenu_window,
        bg="#FFFFFF",
        height=720,
        width=1200,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    for i in range(1, 10):
        button_image = PhotoImage(file=relative_to_assets(f"button_{i}.png", "mainmenu"))
        button = Button(
            image=button_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda i=i: print(f"button_{i} clicked"),
            relief="flat"
        )
        button.image = button_image
        if i <= 6:
            button.place(x=(i - 1) * 200.0, y=0.0, width=200.0, height=100.0)
        else:
            button.place(x=90.0, y=170.0 + (i - 7) * 181.0, width=420.0, height=111.0)

    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png", "mainmenu"))
    canvas.create_image(872.5, 449.0, image=entry_image_1)
    entry_1 = Text(
        bd=0,
        bg="#D0D0D0",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(x=593.0, y=255.0, width=559.0, height=386.0)

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png", "mainmenu"))
    canvas.create_image(616.0, 194.0, image=image_image_1)

    entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png", "mainmenu"))
    canvas.create_image(902.0, 195.0, image=entry_image_2)
    entry_2 = Entry(
        bd=0,
        bg="#D0D0D0",
        fg="#000716",
        highlightthickness=0
    )
    entry_2.place(x=652.0, y=170.0, width=500.0, height=48.0)

    mainmenu_window.resizable(False, False)
    mainmenu_window.mainloop()

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
