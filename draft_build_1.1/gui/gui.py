from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox, Scrollbar, Frame

import utils.login_page_utils as lp


def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()
    for attr in dir(window):
        if isinstance(getattr(window, attr), PhotoImage):
            setattr(window, attr, None)



def open_login_page():
    window = Tk()
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\hallo\OneDrive\Desktop\SP2025 DOCS\MIS161\GUI\draft_build_1.1\assets")
    window.geometry("1200x720")
    window.configure(bg = "#FFFFFF")
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
    window.username_entry = Entry(
        bd=0,
        bg="#D0D0D0",
        fg="#000716",
        highlightthickness=0
    )
    window.username_entry.place(
        x=768.0,
        y=458.0,
        width=300.0,
        height=48.0
    )

    
    window.password_entry = Entry(
        bd=0,
        bg="#D0D0D0",
        fg="#000716",
        highlightthickness=0
    )
    window.password_entry.place(
        x=768.0,
        y=379.0,
        width=300.0,
        height=48.0
    )

    window.aa_logo_image = PhotoImage(
        file=relative_to_assets("aalogo.png"))
    window.aa_logo = window.canvas.create_image(
        918.0,
        225.0,
        image=window.aa_logo_image
    )

    window.login_button_image = PhotoImage(
        file=relative_to_assets("login_button.png"))
    window.login_button = Button(
        image=window.login_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: lp.validate_login(window, window.username_entry.get().strip(), window.password_entry.get().strip()),
        relief="flat"
    )
    window.login_button.place(
        x=843.0,
        y=547.0,
        width=150.0,
        height=50.0
    )

    window.aa_store_image = PhotoImage(
        file=relative_to_assets("aastore.png"))
    window.aa_store = window.canvas.create_image(
        309.0,
        360.0,
        image=window.aa_store_image
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
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\hallo\OneDrive\Desktop\SP2025 DOCS\MIS161\GUI\draft_build_1.1\assets")
    window.geometry("1200x720")
    window.configure(bg = "#FFFFFF")
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
    window.selected_home_button_image = PhotoImage(
        file=relative_to_assets("selected_home_button.png"))
    window.selected_home_button = Button(
        image=window.selected_home_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_1 clicked"),
        relief="flat"
    )
    window.selected_home_button.place(
        x=0.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.onboarding_button_image = PhotoImage(
        file=relative_to_assets("onboarding_button.png"))
    window.onboarding_button = Button(
        image=window.onboarding_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: (clear_window(window), open_onboarding(window)),
        relief="flat"
    )
    window.onboarding_button.place(
        x=200.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.new_ticket_button_image = PhotoImage(
        file=relative_to_assets("new_ticket_button.png"))
    window.new_ticket_button = Button(
        image=window.new_ticket_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print(clear_window(window),open_new_ticket(window)),
        relief="flat"
    )
    window.new_ticket_button.place(
        x=400.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.customers_button_image = PhotoImage(
        file=relative_to_assets("customers_button.png"))
    window.customers_button = Button(
        image=window.customers_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_4 clicked"),
        relief="flat"
    )
    window.customers_button.place(
        x=600.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.tickets_button_image = PhotoImage(
        file=relative_to_assets("tickets_button.png"))
    window.tickets_button = Button(
        image=window.tickets_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_5 clicked"),
        relief="flat"
    )
    window.tickets_button.place(
        x=800.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.inventory_button_image = PhotoImage(
        file=relative_to_assets("inventory_button.png"))
    window.inventory_button = Button(
        image=window.inventory_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_6 clicked"),
        relief="flat"
    )
    window.inventory_button.place(
        x=1000.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.print_new_invoice_button_image = PhotoImage(
        file=relative_to_assets("print_new_invoice.png"))
    window.print_new_invoice_button = Button(
        image=window.print_new_invoice_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_7 clicked"),
        relief="flat"
    )
    window.print_new_invoice_button.place(
        x=90.0,
        y=532.0,
        width=420.0,
        height=111.0
    )

    window.create_new_ticket_button_image = PhotoImage(
        file=relative_to_assets("create_new_ticket.png"))
    window.create_new_ticket_button = Button(
        image=window.create_new_ticket_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_8 clicked"),
        relief="flat"
    )
    window.create_new_ticket_button.place(
        x=90.0,
        y=351.0,
        width=420.0,
        height=111.0
    )

    window.add_new_customer_button_image = PhotoImage(
        file=relative_to_assets("add_new_customer.png"))
    window.add_new_customer_button = Button(
        image=window.add_new_customer_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_9 clicked"),
        relief="flat"
    )
    window.add_new_customer_button.place(
        x=90.0,
        y=170.0,
        width=420.0,
        height=111.0
    )

    window.search_results_field = Text(
        bd=0,
        bg="#D0D0D0",
        fg="#000716",
        highlightthickness=0
    )
    window.search_results_field.place(
        x=593.0,
        y=255.0,
        width=559.0,
        height=386.0
    )

    window.search_bar_field = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    window.search_bar_field.place(
        x=652.0,
        y=170.0,
        width=500.0,
        height=48.0
    )
    window.resizable(False, False)
    window.mainloop()
    

def open_onboarding(window):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\hallo\OneDrive\Desktop\SP2025 DOCS\MIS161\GUI\draft_build_1.1\assets")
    window.geometry("1200x720")
    window.configure(bg = "#FFFFFF")
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
    window.home_button_image = PhotoImage(
        file=relative_to_assets("home_button.png"))
    window.home_button = Button(
        image=window.home_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: (clear_window(window),open_main_menu(window)),
        relief="flat"
    )
    window.home_button.place(
        x=0.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.selected_onboarding_button_image = PhotoImage(
        file=relative_to_assets("selected_onboarding_button.png"))
    window.selected_onboarding_button = Button(
        image=window.selected_onboarding_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print(clear_window(window),open_new_ticket(window)),
        relief="flat"
    )
    window.selected_onboarding_button.place(
        x=200.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.new_ticket_button_image = PhotoImage(
        file=relative_to_assets("new_ticket_button.png"))
    window.new_ticket_button = Button(
        image=window.new_ticket_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print(clear_window(window),open_new_ticket(window)),
        relief="flat"
    )
    window.new_ticket_button.place(
        x=400.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.customers_button_image = PhotoImage(
        file=relative_to_assets("customers_button.png"))
    window.customers_button = Button(
        image=window.customers_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_4 clicked"),
        relief="flat"
    )
    window.customers_button.place(
        x=600.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.tickets_button_image = PhotoImage(
        file=relative_to_assets("tickets_button.png"))
    window.tickets_button = Button(
        image=window.tickets_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_5 clicked"),
        relief="flat"
    )
    window.tickets_button.place(
        x=800.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.inventory_button_image = PhotoImage(
        file=relative_to_assets("inventory_button.png"))
    window.inventory_button = Button(
        image=window.inventory_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_6 clicked"),
        relief="flat"
    )
    window.inventory_button.place(
        x=1000.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.clear_button_image = PhotoImage(
        file=relative_to_assets("clear_button.png"))
    window.clear_button = Button(
        image=window.clear_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_7 clicked"),
        relief="flat"
    )
    window.clear_button.place(
        x=1073.0,
        y=647.0,
        width=78.0,
        height=49.0
    )

    window.save_button_image = PhotoImage(
        file=relative_to_assets("save_button.png"))
    window.save_button = Button(
        image=window.save_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_8 clicked"),
        relief="flat"
    )
    window.save_button.place(
        x=961.0,
        y=647.0,
        width=78.0,
        height=49.0
    )

    window.canvas.create_text(
        952.0,
        612.0,
        anchor="nw",
        text="*Required Fields",
        fill="#E00000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        96.0,
        169.0,
        anchor="nw",
        text="First Name*",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        613.0,
        169.0,
        anchor="nw",
        text="Last Name*",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.first_name_entry = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.first_name_entry.place(
        x=97.0,
        y=204.0,
        width=426.0,
        height=45.0
    )

    window.last_name_entry = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.last_name_entry.place(
        x=767.0,
        y=538.0,
        width=272.0,
        height=45.0
    )

    window.phone_number_entry = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.phone_number_entry.place(
        x=613.0,
        y=538.0,
        width=107.0,
        height=45.0
    )

    window.email_entry = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.email_entry.place(
        x=97.0,
        y=538.0,
        width=426.0,
        height=45.0
    )

    window.address1_entry = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.address1_entry.place(
        x=613.0,
        y=424.0,
        width=426.0,
        height=45.0
    )

    window.address2_entry = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.address2_entry.place(
        x=97.0,
        y=424.0,
        width=426.0,
        height=45.0
    )

    window.city_entry = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.city_entry.place(
        x=613.0,
        y=310.0,
        width=426.0,
        height=45.0
    )

    window.state_entry = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.state_entry.place(
        x=613.0,
        y=204.0,
        width=426.0,
        height=45.0
    )

    window.zipcode_entry = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.zipcode_entry.place(
        x=96.0,
        y=310.0,
        width=426.0,
        height=45.0
    )

    window.canvas.create_text(
        96.0,
        276.0,
        anchor="nw",
        text="Email*",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        96.0,
        386.0,
        anchor="nw",
        text="Address",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        97.0,
        500.0,
        anchor="nw",
        text="City",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        613.0,
        276.0,
        anchor="nw",
        text="Mobile*",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        613.0,
        386.0,
        anchor="nw",
        text="Address 2",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        613.0,
        500.0,
        anchor="nw",
        text="State",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        767.0,
        500.0,
        anchor="nw",
        text="Zipcode",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )
    window.resizable(False, False)
    window.mainloop()


def open_new_ticket(window):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\hallo\OneDrive\Desktop\SP2025 DOCS\MIS161\GUI\draft_build_1.1\assets")
    window.geometry("1200x800")
    window.configure(bg = "#FFFFFF")
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
    home_button_image = PhotoImage(
        file=relative_to_assets("home_button.png"))
    window.selected_home_button = Button(
        image=home_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_1 clicked"),
        relief="flat"
    )
    window.selected_home_button.place(
        x=0.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.onboarding_button_image = PhotoImage(
        file=relative_to_assets("onboarding_button.png"))
    window.onboarding_button = Button(
        image=window.onboarding_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: (clear_window(window), open_onboarding(window)),
        relief="flat"
    )
    window.onboarding_button.place(
        x=200.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.new_ticket_button_image = PhotoImage(
        file=relative_to_assets("selected_new_ticket_button.png"))
    window.new_ticket_button = Button(
        image=window.new_ticket_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button 3 clicked"),
        relief="flat"
    )
    window.new_ticket_button.place(
        x=400.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.customers_button_image = PhotoImage(
        file=relative_to_assets("customers_button.png"))
    window.customers_button = Button(
        image=window.customers_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_4 clicked"),
        relief="flat"
    )
    window.customers_button.place(
        x=600.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.tickets_button_image = PhotoImage(
        file=relative_to_assets("tickets_button.png"))
    window.tickets_button = Button(
        image=window.tickets_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_5 clicked"),
        relief="flat"
    )
    window.tickets_button.place(
        x=800.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.inventory_button_image = PhotoImage(
        file=relative_to_assets("inventory_button.png"))
    window.inventory_button = Button(
        image=window.inventory_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_6 clicked"),
        relief="flat"
    )
    window.inventory_button.place(
        x=1000.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    clear_button_image = PhotoImage(
        file=relative_to_assets("clear_button.png"))
    window.clear_button = Button(
        image=clear_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_7 clicked"),
        relief="flat"
    )
    window.clear_button.place(
        x=1074.0,
        y=816.0,
        width=78.0,
        height=49.0
    )

    save_button_image = PhotoImage(
        file=relative_to_assets("save_button.png"))
    window.save_button = Button(
        window,
        image=save_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_8 clicked"),
        relief="flat"
    )
    window.save_button.place(
        x=963.0,
        y=816.0,
        width=78.0,
        height=49.0
    )

    window.canvas.create_text(
        952.0,
        777.0,
        anchor="nw",
        text="*Required Fields",
        fill="#E00000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.entry_1 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.entry_1.place(
        x=36.0,
        y=055.0,
        width=192.0,
        height=45.0
    )

    window.entry_2 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.entry_2.place(
        x=36.0,
        y=291.0,
        width=264.0,
        height=45.0
    )

    window.entry_3 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.entry_3.place(
        x=36.0,
        y=393.0,
        width=494.0,
        height=142.0
    )

    window.entry_4 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.entry_4.place(
        x=36.0,
        y=592.0,
        width=494.0,
        height=263.0
    )

    window.entry_5 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.entry_5.place(
        x=600.0,
        y=393.0,
        width=500.0,
        height=142.0
    )

    window.entry_6 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.entry_6.place(
        x=600.0,
        y=592.0,
        width=500.0,
        height=142.0
    )

    window.entry_7 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.entry_7.place(
        x=400.0,
        y=291.0,
        width=160.0,
        height=45.0
    )

    window.entry_8 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.entry_8.place(
        x=800.0,
        y=189.0,
        width=300.0,
        height=45.0
    )

    window.entry_9 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.entry_9.place(
        x=36.0,
        y=189.0,
        width=192.0,
        height=45.0
    )

    window.entry_10 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.entry_10.place(
        x=300.0,
        y=189.0,
        width=430.0,
        height=45.0
    )

    window.entry_11 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.entry_11.place(
        x=300.0,
        y=055.0,
        width=426.0,
        height=45.0
    )

    window.entry_12 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.entry_12.place(
        x=845.0,
        y=055.0,
        width=255.0,
        height=45.0
    )

    window.canvas.create_text(
        36.0,
        158.0,
        anchor="nw",
        text="Gun Brand",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        36.0,
        024.0,
        anchor="nw",
        text="Drop Off Date",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        300.0,
        024.0,
        anchor="nw",
        text="Customer",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        845.0,
        024.0,
        anchor="nw",
        text="Received By",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        300.0,
        158.0,
        anchor="nw",
        text="Gun Model",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        36.0,
        257.0,
        anchor="nw",
        text="Purchase Location",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        401.0,
        157.0,
        anchor="nw",
        text="Purchase Date",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        800.0,
        158.0,
        anchor="nw",
        text="Gun Serial Number",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        36.0,
        561.0,
        anchor="nw",
        text="Work Description",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        36.0,
        359.0,
        anchor="nw",
        text="List Previous Upgrades and/or Repairs",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        600.0,
        259.0,
        anchor="nw",
        text="Additional Parts and Extras",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        602.0,
        561.0,
        anchor="nw",
        text="Additional Comments",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )
    window.resizable(False, False)
    window.mainloop()
