from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox

import utils.login_page_utils as lp

def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()
    for attr in dir(window):
        if isinstance(getattr(window, attr), PhotoImage):
            setattr(window, attr, None)

def open_login_page():
    window = Tk()
    window.geometry("1200x720")
    window.configure(bg = "#FFFFFF")
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\hallo\OneDrive\Desktop\SP2025 DOCS\MIS161\GUI\draft_build_1.1\login_page\build\assets\frame0")
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)
    window.canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 720,
        width = 1200,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    window.canvas.place(x = 0, y = 0)
    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    window.entry_bg_1 = window.canvas.create_image(
        918.0,
        483.0,
        image=entry_image_1
    )
    window.entry_1 = Entry(
        bd=0,
        bg="#D0D0D0",
        fg="#000716",
        highlightthickness=0
    )
    window.entry_1.place(
        x=768.0,
        y=458.0,
        width=300.0,
        height=48.0
    )

    window.entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    window.entry_bg_2 = window.canvas.create_image(
        918.0,
        404.0,
        image=window.entry_image_2
    )
    window.entry_2 = Entry(
        bd=0,
        bg="#D0D0D0",
        fg="#000716",
        highlightthickness=0
    )
    window.entry_2.place(
        x=768.0,
        y=379.0,
        width=300.0,
        height=48.0
    )

    window.image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    window.image_1 = window.canvas.create_image(
        918.0,
        225.0,
        image=window.image_image_1
    )

    window.button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    window.button_1 = Button(
        image=window.button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: lp. validate_login(window),
        relief="flat"
    )
    window.button_1.place(
        x=843.0,
        y=547.0,
        width=150.0,
        height=50.0
    )

    window.image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    window.image_2 = window.canvas.create_image(
        309.0,
        360.0,
        image=window.image_image_2
    )

    window.canvas.create_text(
        768.0,
        350.0,
        anchor="nw",
        text="Username",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        768.0,
        432.0,
        anchor="nw",
        text="Password",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )
    window.resizable(False, False)
    window.mainloop()

def open_main_menu(window):
    window.geometry("1200x720")
    window.configure(bg = "#FFFFFF")
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\hallo\OneDrive\Desktop\SP2025 DOCS\MIS161\GUI\draft_build_1.1\main_menu\build\assets\frame0")
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)
    window.canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 720,
        width = 1200,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    window.canvas.place(x = 0, y = 0)
    window.button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    window.button_1 = Button(
        image=window.button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_1 clicked"),
        relief="flat"
    )
    window.button_1.place(
        x=0.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    window.button_2 = Button(
        image=window.button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: (clear_window(window), open_onboarding(window)),
        relief="flat"
    )
    window.button_2.place(
        x=200.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    window.button_3 = Button(
        image=window.button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: (clear_window(window), open_new_ticket(window)),
        relief="flat"
    )
    window.button_3.place(
        x=400.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    window.button_4 = Button(
        image=window.button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_4 clicked"),
        relief="flat"
    )
    window.button_4.place(
        x=600.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.button_image_5 = PhotoImage(
        file=relative_to_assets("button_5.png"))
    window.button_5 = Button(
        image=window.button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_5 clicked"),
        relief="flat"
    )
    window.button_5.place(
        x=800.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.button_image_6 = PhotoImage(
        file=relative_to_assets("button_6.png"))
    window.button_6 = Button(
        image=window.button_image_6,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_6 clicked"),
        relief="flat"
    )
    window.button_6.place(
        x=1000.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.button_image_7 = PhotoImage(
        file=relative_to_assets("button_7.png"))
    window.button_7 = Button(
        image=window.button_image_7,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_7 clicked"),
        relief="flat"
    )
    window.button_7.place(
        x=90.0,
        y=532.0,
        width=420.0,
        height=111.0
    )

    window.button_image_8 = PhotoImage(
        file=relative_to_assets("button_8.png"))
    window.button_8 = Button(
        image=window.button_image_8,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_8 clicked"),
        relief="flat"
    )
    window.button_8.place(
        x=90.0,
        y=351.0,
        width=420.0,
        height=111.0
    )

    window.button_image_9 = PhotoImage(
        file=relative_to_assets("button_9.png"))
    window.button_9 = Button(
        image=window.button_image_9,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_9 clicked"),
        relief="flat"
    )
    window.button_9.place(
        x=90.0,
        y=170.0,
        width=420.0,
        height=111.0
    )

    window.entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    window.entry_bg_1 = window.canvas.create_image(
        872.5,
        449.0,
        image=window.entry_image_1
    )
    window.entry_1 = Text(
        bd=0,
        bg="#D0D0D0",
        fg="#000716",
        highlightthickness=0
    )
    window.entry_1.place(
        x=593.0,
        y=255.0,
        width=559.0,
        height=386.0
    )

    window.image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    window.image_1 = window.canvas.create_image(
        616.0,
        194.0,
        image=window.image_image_1
    )

    window.entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    window.entry_bg_2 = window.canvas.create_image(
        902.0,
        195.0,
        image=window.entry_image_2
    )
    window.entry_2 = Entry(
        bd=0,
        bg="#D0D0D0",
        fg="#000716",
        highlightthickness=0
    )
    window.entry_2.place(
        x=652.0,
        y=170.0,
        width=500.0,
        height=48.0
    )
    window.resizable(False, False)
    window.mainloop()

def open_onboarding(window):
    window.geometry("1200x720")
    window.configure(bg = "#FFFFFF")
    window.resizable(False, False)
    window.mainloop()

def open_new_ticket(window):
    window.geometry("1200x720")
    window.configure(bg = "#FFFFFF")
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\hallo\OneDrive\Desktop\SP2025 DOCS\MIS161\GUI\draft_build_1.1\new_ticket\build\assets\frame0")
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)
    window.canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 720,
        width = 1200,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    window.canvas.place(x = 0, y = 0)
    window.button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    window.button_1 = Button(
        image=window.button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: (clear_window(window), open_main_menu(window)),
        relief="flat"
    )
    window.button_1.place(
        x=0.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    window.button_2 = Button(
        image=window.button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_2 clicked"),
        relief="flat"
    )
    window.button_2.place(
        x=200.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    window.button_3 = Button(
        image=window.button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_3 clicked"),
        relief="flat"
    )
    window.button_3.place(
        x=400.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    window.button_4 = Button(
        image=window.button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_4 clicked"),
        relief="flat"
    )
    window.button_4.place(
        x=600.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.button_image_5 = PhotoImage(
        file=relative_to_assets("button_5.png"))
    window.button_5 = Button(
        image=window.button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_5 clicked"),
        relief="flat"
    )
    window.button_5.place(
        x=800.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.button_image_6 = PhotoImage(
        file=relative_to_assets("button_6.png"))
    window.button_6 = Button(
        image=window.button_image_6,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_6 clicked"),
        relief="flat"
    )
    window.button_6.place(
        x=1000.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.button_image_7 = PhotoImage(
        file=relative_to_assets("button_7.png"))
    window.button_7 = Button(
        image=window.button_image_7,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_7 clicked"),
        relief="flat"
    )
    window.button_7.place(
        x=1074.0,
        y=916.0,
        width=78.0,
        height=49.0
    )

    window.button_image_8 = PhotoImage(
        file=relative_to_assets("button_8.png"))
    window.button_8 = Button(
        image=window.button_image_8,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_8 clicked"),
        relief="flat"
    )
    window.button_8.place(
        x=963.0,
        y=916.0,
        width=78.0,
        height=49.0
    )

    window.canvas.create_text(
        952.0,
        877.0,
        anchor="nw",
        text="*Required Fields",
        fill="#E00000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    window.entry_bg_1 = window.canvas.create_image(
        132.0,
        178.5,
        image=window.entry_image_1
    )
    window.entry_1 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.entry_1.place(
        x=36.0,
        y=155.0,
        width=192.0,
        height=45.0
    )

    window.entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    window.entry_bg_2 = window.canvas.create_image(
        168.0,
        414.5,
        image=window.entry_image_2
    )
    window.entry_2 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.entry_2.place(
        x=36.0,
        y=391.0,
        width=264.0,
        height=45.0
    )

    window.entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    window.entry_bg_3 = window.canvas.create_image(
        283.0,
        565.0,
        image=window.entry_image_3
    )
    window.entry_3 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.entry_3.place(
        x=36.0,
        y=493.0,
        width=494.0,
        height=142.0
    )

    window.entry_image_4 = PhotoImage(
        file=relative_to_assets("entry_4.png"))
    window.entry_bg_4 = window.canvas.create_image(
        283.0,
        824.5,
        image=window.entry_image_4
    )
    window.entry_4 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.entry_4.place(
        x=36.0,
        y=692.0,
        width=494.0,
        height=263.0
    )

    window.entry_image_5 = PhotoImage(
        file=relative_to_assets("entry_5.png"))
    window.entry_bg_5 = window.canvas.create_image(
        850.0,
        565.0,
        image=window.entry_image_5
    )
    window.entry_5 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.entry_5.place(
        x=600.0,
        y=493.0,
        width=500.0,
        height=142.0
    )

    window.entry_image_6 = PhotoImage(
        file=relative_to_assets("entry_6.png"))
    window.entry_bg_6 = window.canvas.create_image(
        850.0,
        764.0,
        image=window.entry_image_6
    )
    window.entry_6 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.entry_6.place(
        x=600.0,
        y=692.0,
        width=500.0,
        height=142.0
    )

    window.entry_image_7 = PhotoImage(
        file=relative_to_assets("entry_7.png"))
    window.entry_bg_7 = window.canvas.create_image(
        480.0,
        414.5,
        image=window.entry_image_7
    )
    window.entry_7 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.entry_7.place(
        x=400.0,
        y=391.0,
        width=160.0,
        height=45.0
    )

    window.entry_image_8 = PhotoImage(
        file=relative_to_assets("entry_8.png"))
    window.entry_bg_8 = window.canvas.create_image(
        950.0,
        312.5,
        image=window.entry_image_8
    )
    window.entry_8 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.entry_8.place(
        x=800.0,
        y=289.0,
        width=300.0,
        height=45.0
    )

    window.entry_image_9 = PhotoImage(
        file=relative_to_assets("entry_9.png"))
    window.entry_bg_9 = window.canvas.create_image(
        132.0,
        312.5,
        image=window.entry_image_9
    )
    window.entry_9 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.entry_9.place(
        x=36.0,
        y=289.0,
        width=192.0,
        height=45.0
    )

    window.entry_image_10 = PhotoImage(
        file=relative_to_assets("entry_10.png"))
    window.entry_bg_10 = window.canvas.create_image(
        515.0,
        312.5,
        image=window.entry_image_10
    )
    window.entry_10 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.entry_10.place(
        x=300.0,
        y=289.0,
        width=430.0,
        height=45.0
    )

    window.entry_image_11 = PhotoImage(
        file=relative_to_assets("entry_11.png"))
    window.entry_bg_11 = window.canvas.create_image(
        513.0,
        178.5,
        image=window.entry_image_11
    )
    window.entry_11 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.entry_11.place(
        x=300.0,
        y=155.0,
        width=426.0,
        height=45.0
    )

    window.entry_image_12 = PhotoImage(
        file=relative_to_assets("entry_12.png"))
    window.entry_bg_12 = window.canvas.create_image(
        972.5,
        178.5,
        image=window.entry_image_12
    )
    window.entry_12 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.entry_12.place(
        x=845.0,
        y=155.0,
        width=255.0,
        height=45.0
    )

    window.canvas.create_text(
        36.0,
        258.0,
        anchor="nw",
        text="Gun Brand",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        36.0,
        124.0,
        anchor="nw",
        text="Drop Off Date",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        300.0,
        124.0,
        anchor="nw",
        text="Customer",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        845.0,
        124.0,
        anchor="nw",
        text="Received By",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        300.0,
        258.0,
        anchor="nw",
        text="Gun Model",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        36.0,
        357.0,
        anchor="nw",
        text="Purchase Location",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        401.0,
        357.0,
        anchor="nw",
        text="Purchase Date",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        800.0,
        258.0,
        anchor="nw",
        text="Gun Serial Number",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        36.0,
        661.0,
        anchor="nw",
        text="Work Description",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        36.0,
        459.0,
        anchor="nw",
        text="List Previous Upgrades and/or Repairs",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        600.0,
        459.0,
        anchor="nw",
        text="Additional Parts and Extras",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        602.0,
        661.0,
        anchor="nw",
        text="Additional Comments",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )
    window.resizable(False, False)
    window.mainloop()