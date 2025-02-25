
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\hallo\OneDrive\Desktop\SP2025 DOCS\MIS161\GUI\draft_build_0.1\new_ticket\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1200x1000")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 1000,
    width = 1200,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=0.0,
    y=0.0,
    width=200.0,
    height=100.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=200.0,
    y=0.0,
    width=200.0,
    height=100.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=400.0,
    y=0.0,
    width=200.0,
    height=100.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=600.0,
    y=0.0,
    width=200.0,
    height=100.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat"
)
button_5.place(
    x=800.0,
    y=0.0,
    width=200.0,
    height=100.0
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_6 clicked"),
    relief="flat"
)
button_6.place(
    x=1000.0,
    y=0.0,
    width=200.0,
    height=100.0
)

button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_7 clicked"),
    relief="flat"
)
button_7.place(
    x=1074.0,
    y=916.0,
    width=78.0,
    height=49.0
)

button_image_8 = PhotoImage(
    file=relative_to_assets("button_8.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_8 clicked"),
    relief="flat"
)
button_8.place(
    x=963.0,
    y=916.0,
    width=78.0,
    height=49.0
)

canvas.create_text(
    952.0,
    877.0,
    anchor="nw",
    text="*Required Fields",
    fill="#E00000",
    font=("MergeOne Regular", 24 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    132.0,
    178.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=36.0,
    y=155.0,
    width=192.0,
    height=45.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    168.0,
    414.5,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=36.0,
    y=391.0,
    width=264.0,
    height=45.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    283.0,
    565.0,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=36.0,
    y=493.0,
    width=494.0,
    height=142.0
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    283.0,
    824.5,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_4.place(
    x=36.0,
    y=692.0,
    width=494.0,
    height=263.0
)

entry_image_5 = PhotoImage(
    file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(
    850.0,
    565.0,
    image=entry_image_5
)
entry_5 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_5.place(
    x=600.0,
    y=493.0,
    width=500.0,
    height=142.0
)

entry_image_6 = PhotoImage(
    file=relative_to_assets("entry_6.png"))
entry_bg_6 = canvas.create_image(
    850.0,
    764.0,
    image=entry_image_6
)
entry_6 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_6.place(
    x=600.0,
    y=692.0,
    width=500.0,
    height=142.0
)

entry_image_7 = PhotoImage(
    file=relative_to_assets("entry_7.png"))
entry_bg_7 = canvas.create_image(
    480.0,
    414.5,
    image=entry_image_7
)
entry_7 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_7.place(
    x=400.0,
    y=391.0,
    width=160.0,
    height=45.0
)

entry_image_8 = PhotoImage(
    file=relative_to_assets("entry_8.png"))
entry_bg_8 = canvas.create_image(
    950.0,
    312.5,
    image=entry_image_8
)
entry_8 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_8.place(
    x=800.0,
    y=289.0,
    width=300.0,
    height=45.0
)

entry_image_9 = PhotoImage(
    file=relative_to_assets("entry_9.png"))
entry_bg_9 = canvas.create_image(
    132.0,
    312.5,
    image=entry_image_9
)
entry_9 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_9.place(
    x=36.0,
    y=289.0,
    width=192.0,
    height=45.0
)

entry_image_10 = PhotoImage(
    file=relative_to_assets("entry_10.png"))
entry_bg_10 = canvas.create_image(
    515.0,
    312.5,
    image=entry_image_10
)
entry_10 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_10.place(
    x=300.0,
    y=289.0,
    width=430.0,
    height=45.0
)

entry_image_11 = PhotoImage(
    file=relative_to_assets("entry_11.png"))
entry_bg_11 = canvas.create_image(
    513.0,
    178.5,
    image=entry_image_11
)
entry_11 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_11.place(
    x=300.0,
    y=155.0,
    width=426.0,
    height=45.0
)

entry_image_12 = PhotoImage(
    file=relative_to_assets("entry_12.png"))
entry_bg_12 = canvas.create_image(
    972.5,
    178.5,
    image=entry_image_12
)
entry_12 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_12.place(
    x=845.0,
    y=155.0,
    width=255.0,
    height=45.0
)

canvas.create_text(
    36.0,
    258.0,
    anchor="nw",
    text="Gun Brand",
    fill="#000000",
    font=("MergeOne Regular", 24 * -1)
)

canvas.create_text(
    36.0,
    124.0,
    anchor="nw",
    text="Drop Off Date",
    fill="#000000",
    font=("MergeOne Regular", 24 * -1)
)

canvas.create_text(
    300.0,
    124.0,
    anchor="nw",
    text="Customer",
    fill="#000000",
    font=("MergeOne Regular", 24 * -1)
)

canvas.create_text(
    845.0,
    124.0,
    anchor="nw",
    text="Received By",
    fill="#000000",
    font=("MergeOne Regular", 24 * -1)
)

canvas.create_text(
    300.0,
    258.0,
    anchor="nw",
    text="Gun Model",
    fill="#000000",
    font=("MergeOne Regular", 24 * -1)
)

canvas.create_text(
    36.0,
    357.0,
    anchor="nw",
    text="Purchase Location",
    fill="#000000",
    font=("MergeOne Regular", 24 * -1)
)

canvas.create_text(
    401.0,
    357.0,
    anchor="nw",
    text="Purchase Date",
    fill="#000000",
    font=("MergeOne Regular", 24 * -1)
)

canvas.create_text(
    800.0,
    258.0,
    anchor="nw",
    text="Gun Serial Number",
    fill="#000000",
    font=("MergeOne Regular", 24 * -1)
)

canvas.create_text(
    36.0,
    661.0,
    anchor="nw",
    text="Work Description",
    fill="#000000",
    font=("MergeOne Regular", 24 * -1)
)

canvas.create_text(
    36.0,
    459.0,
    anchor="nw",
    text="List Previous Upgrades and/or Repairs",
    fill="#000000",
    font=("MergeOne Regular", 24 * -1)
)

canvas.create_text(
    600.0,
    459.0,
    anchor="nw",
    text="Additional Parts and Extras",
    fill="#000000",
    font=("MergeOne Regular", 24 * -1)
)

canvas.create_text(
    602.0,
    661.0,
    anchor="nw",
    text="Additional Comments",
    fill="#000000",
    font=("MergeOne Regular", 24 * -1)
)
window.resizable(False, False)
window.mainloop()
