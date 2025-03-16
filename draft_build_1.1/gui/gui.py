from pathlib import Path
from tkinter import Tk, ttk, Canvas, Entry, Text, Button, PhotoImage, VERTICAL, Scrollbar, Label, Toplevel, END, StringVar

import utils.login_page_utils as lp
import utils.onboarding_utils as ob
import utils.new_ticket_utils as nt
import utils.customers_utils as cs

def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()
    for attr in dir(window):
        if isinstance(getattr(window, attr), PhotoImage):
            setattr(window, attr, None)

def open_inventory(window):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Sean\Documents\VSCODEPROJECTS\AirsoftTechWorker-ATW-v.0.2.0\AirsoftTechWorker-ATW-v.0.2.0\draft_build_1.1\assets")
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
        file=relative_to_assets("home_button.png"))
    window.selected_home_button = Button(
        image=window.selected_home_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: (clear_window(window), open_main_menu(window)),
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
        command=lambda: (clear_window(window), open_new_ticket(window)),
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
        command=lambda: (clear_window(window), open_customers(window)),
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
        command=lambda: (clear_window(window), open_tickets(window)),
        relief="flat"
    )
    window.tickets_button.place(
        x=800.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.inventory_button_image = PhotoImage(
        file=relative_to_assets("selected_inventory_button.png"))
    window.inventory_button = Button(
        image=window.inventory_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: (clear_window(window), open_inventory(window)),
        relief="flat"
    )
    window.inventory_button.place(
        x=1000.0,
        y=0.0,
        width=200.0,
        height=100.0
    )
    window.resizable(False, False)
    window.mainloop()

def open_tickets(window):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Sean\Documents\VSCODEPROJECTS\AirsoftTechWorker-ATW-v.0.2.0\AirsoftTechWorker-ATW-v.0.2.0\draft_build_1.1\assets")
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
        file=relative_to_assets("home_button.png"))
    window.selected_home_button = Button(
        image=window.selected_home_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: (clear_window(window), open_main_menu(window)),
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
        command=lambda: (clear_window(window),open_new_ticket(window)),
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
        command=lambda: (clear_window(window),open_customers(window)),
        relief="flat"
    )
    window.customers_button.place(
        x=600.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.tickets_button_image = PhotoImage(
        file=relative_to_assets("selected_tickets_button.png"))
    window.tickets_button = Button(
        image=window.tickets_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: (clear_window(window),open_tickets(window)),
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
        command=lambda: (clear_window(window),open_inventory(window)),
        relief="flat"
    )
    window.inventory_button.place(
        x=1000.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.canvas.create_text(
        90.0,
        140.0,
        anchor="nw",
        text="Search customers:",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    search_var = StringVar()

    window.search_bar_field = Entry(
        textvariable=search_var,
        bd=0,
        bg="#D0D0D0",
        fg="#000716",
        highlightthickness=0
    )
    window.search_bar_field.place(
        x=90.0,
        y=170.0,
        width=1000.0,
        height=48.0
    )

    # Scrollbar
    scrollbar = Scrollbar(window, orient=VERTICAL)

    # Treeview (Table) for displaying customers
    columns = ("FirstName", "LastName", "PhoneNumber", "Email")
    tree = ttk.Treeview(window, columns=columns, show="headings", height=10)

    # Define column headings with proper spacing
    tree.heading("FirstName", text="First Name")
    tree.heading("LastName", text="Last Name")
    tree.heading("PhoneNumber", text="Phone Number")
    tree.heading("Email", text="Email")

    tree.column("FirstName", width=150, anchor="center")
    tree.column("LastName", width=150, anchor="center")
    tree.column("PhoneNumber", width=150, anchor="center")
    tree.column("Email", width=250, anchor="center")

    # Place Treeview
    tree.place(x=90, y=240, width=1000, height=430)

    # Scrollbar (Placed next to the listbox)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.place(x=1090.0, y=240.0, height=430.0)


    # Fetch customer data from the database using cs
    customers = cs.read_customer_data_from_access()
    print(customers)

    def show_customer_details(customer):
        """Displays a new window with customer details."""
        details_window = Toplevel()
        details_window.title("Customer Details")

        Label(details_window, text=f"First Name: {customer['FirstName']}", font=("Arial", 12)).pack(pady=5)
        Label(details_window, text=f"Last Name: {customer['LastName']}", font=("Arial", 12)).pack(pady=5)
        Label(details_window, text=f"Phone Number: {customer['PhoneNumber']}", font=("Arial", 12)).pack(pady=5)
        Label(details_window, text=f"Email: {customer['Email']}", font=("Arial", 12)).pack(pady=5)

    def update_list():
        """Filters the customer list based on the search entry."""
        search_term = window.search_bar_field.get().lower()
        tree.delete(*tree.get_children())

        for customer in customers:
            if (search_term in customer["FirstName"].lower() or  # First name
                search_term in customer["LastName"].lower() or   # Last name
                search_term in customer["PhoneNumber"] or        # Phone number
                search_term in customer["Email"].lower()):       # Email
                tree.insert("", END, values=(
                    customer["FirstName"],
                    customer["LastName"],
                    customer["PhoneNumber"],
                    customer["Email"]
                ))
    
    def on_select(event):
        """Handles selection and shows customer details."""
        selected_item = tree.selection()
        print(f"Selected Item: {selected_item}")  # Debugging output

        if selected_item:
            item_values = tree.item(selected_item)["values"]
            print(f"Item Values: {item_values}")  # Debugging output

            if item_values:  # Ensure it's not empty
                customer = {
                    "FirstName": item_values[0],
                    "LastName": item_values[1],
                    "PhoneNumber": item_values[2],
                    "Email": item_values[3]
                }
                show_customer_details(customer)
            else:
                print("⚠️ No values found in selected item!")
        else:
            print("⚠️ No selection detected!")

    update_list()

    tree.bind("<<TreeviewSelect>>", on_select)
    search_var.trace_add("write", lambda *args: update_list())
    
    window.resizable(False, False)
    window.mainloop()
    
def open_customers(window):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Sean\Documents\VSCODEPROJECTS\AirsoftTechWorker-ATW-v.0.2.0\AirsoftTechWorker-ATW-v.0.2.0\draft_build_1.1\assets")
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
        file=relative_to_assets("home_button.png"))
    window.selected_home_button = Button(
        image=window.selected_home_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: (clear_window(window), open_main_menu(window)),
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
        command=lambda: (clear_window(window),open_new_ticket(window)),
        relief="flat"
    )
    window.new_ticket_button.place(
        x=400.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.customers_button_image = PhotoImage(
        file=relative_to_assets("selected_customers_button.png"))
    window.customers_button = Button(
        image=window.customers_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: (clear_window(window),open_customers(window)),
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
        command=lambda: (clear_window(window),open_tickets(window)),
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
        command=lambda: (clear_window(window),open_inventory(window)),
        relief="flat"
    )
    window.inventory_button.place(
        x=1000.0,
        y=0.0,
        width=200.0,
        height=100.0
    )

    window.canvas.create_text(
        90.0,
        140.0,
        anchor="nw",
        text="Search customers:",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    search_var = StringVar()

    window.search_bar_field = Entry(
        textvariable=search_var,
        bd=0,
        bg="#D0D0D0",
        fg="#000716",
        highlightthickness=0
    )
    window.search_bar_field.place(
        x=90.0,
        y=170.0,
        width=1000.0,
        height=48.0
    )

    # Scrollbar
    scrollbar = Scrollbar(window, orient=VERTICAL)

    # Treeview (Table) for displaying customers
    columns = ("FirstName", "LastName", "PhoneNumber", "Email")
    tree = ttk.Treeview(window, columns=columns, show="headings", height=10)

    # Define column headings with proper spacing
    tree.heading("FirstName", text="First Name")
    tree.heading("LastName", text="Last Name")
    tree.heading("PhoneNumber", text="Phone Number")
    tree.heading("Email", text="Email")

    tree.column("FirstName", width=150, anchor="center")
    tree.column("LastName", width=150, anchor="center")
    tree.column("PhoneNumber", width=150, anchor="center")
    tree.column("Email", width=250, anchor="center")

    # Place Treeview
    tree.place(x=90, y=240, width=1000, height=430)

    # Scrollbar (Placed next to the listbox)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.place(x=1090.0, y=240.0, height=430.0)


    # Fetch customer data from the database using cs
    customers = cs.read_customer_data_from_access()
    print(customers)

    def show_customer_details(customer):
        """Displays a new window with customer details."""
        details_window = Toplevel()
        details_window.title("Customer Details")

        Label(details_window, text=f"First Name: {customer['FirstName']}", font=("Arial", 12)).pack(pady=5)
        Label(details_window, text=f"Last Name: {customer['LastName']}", font=("Arial", 12)).pack(pady=5)
        Label(details_window, text=f"Phone Number: {customer['PhoneNumber']}", font=("Arial", 12)).pack(pady=5)
        Label(details_window, text=f"Email: {customer['Email']}", font=("Arial", 12)).pack(pady=5)

    def update_list():
        """Filters the customer list based on the search entry."""
        search_term = window.search_bar_field.get().lower()
        tree.delete(*tree.get_children())

        for customer in customers:
            if (search_term in customer["FirstName"].lower() or  # First name
                search_term in customer["LastName"].lower() or   # Last name
                search_term in customer["PhoneNumber"] or        # Phone number
                search_term in customer["Email"].lower()):       # Email
                tree.insert("", END, values=(
                    customer["FirstName"],
                    customer["LastName"],
                    customer["PhoneNumber"],
                    customer["Email"]
                ))
    
    def on_select(event):
        """Handles selection and shows customer details."""
        selected_item = tree.selection()
        print(f"Selected Item: {selected_item}")  # Debugging output

        if selected_item:
            item_values = tree.item(selected_item)["values"]
            print(f"Item Values: {item_values}")  # Debugging output

            if item_values:  # Ensure it's not empty
                customer = {
                    "FirstName": item_values[0],
                    "LastName": item_values[1],
                    "PhoneNumber": item_values[2],
                    "Email": item_values[3]
                }
                show_customer_details(customer)
            else:
                print("⚠️ No values found in selected item!")
        else:
            print("⚠️ No selection detected!")

    update_list()

    tree.bind("<<TreeviewSelect>>", on_select)
    search_var.trace_add("write", lambda *args: update_list())


    window.resizable(False, False)
    window.mainloop()

def open_new_ticket(window):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Sean\Documents\VSCODEPROJECTS\AirsoftTechWorker-ATW-v.0.2.0\AirsoftTechWorker-ATW-v.0.2.0\draft_build_1.1\assets")
    window.geometry("1200x800")
    window.configure(bg = "#FFFFFF")
    customers = nt.read_customer_name_data_from_access()

    customer_names = [customer["FullName"] for customer in customers]

    brands = [
        "A&K", "APS", "AGM", "Arcturus", "ARES", "Army Armament", "ASG",
        "Classic Army", "CYMA",
        "Dboys", "Double Bell",
        "Echo1", "Elite Force", "EMG",
        "G&G", "Golden Eagle",
        "ICS", 
        "JG",
        "KJ Works", "King Arms", "Krytac",
        "Lancer Tactical", "LCT Airsoft",
        "Maruzen", "Modify",
        "PTS", "RWA",
        "Sig Air", "Specna Arms", "SRC",
        "Tokyo Marui",
        "Umarex",
        "Valken", "VFC (Vega Force Company)",
        "WE", "Well", "WinGun",
        "OTHER"
    ]
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)
    window.canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 800,
        width = 1200,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    window.canvas.place(x = 0, y = 0)
    window.selected_home_button_image = PhotoImage(
        file=relative_to_assets("home_button.png"))
    window.selected_home_button = Button(
        image=window.selected_home_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: (clear_window(window), open_main_menu(window)),
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
        command=lambda: (clear_window(window),open_new_ticket(window)),
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
        command=lambda: (clear_window(window), open_customers(window)),
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
        command=lambda: (clear_window(window), open_tickets(window)),
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
        command=lambda: (clear_window(window), open_inventory(window)),
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
        x=1024.0,
        y=719.0,
        width=78.0,
        height=49.0
    )

    window.save_button_image = PhotoImage(
        file=relative_to_assets("save_button.png"))
    window.save_button = Button(
        image=window.save_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: nt.save_to_access(window),
        relief="flat"
    )
    window.save_button.place(
        x=913.0,
        y=719.0,
        width=78.0,
        height=49.0
    )

    window.canvas.create_text(
        902.0,
        680.0,
        anchor="nw",
        text="*Required Fields",
        fill="#E00000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.drop_off_date_entry = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.drop_off_date_entry.place(
        x=36.0,
        y=155.0,
        width=192.0,
        height=45.0
    )

    window.purchase_location_entry = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.purchase_location_entry.place(
        x=36.0,
        y=333.0,
        width=264.0,
        height=45.0
    )

    window.past_entry = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.past_entry.place(
        x=36.0,
        y=439.0,
        width=494.0,
        height=69.0
    )

    window.work_entry = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.work_entry.place(
        x=36.0,
        y=563.0,
        width=494.0,
        height=149.0
    )

    window.add_parts_entry = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.add_parts_entry.place(
        x=602.0,
        y=388.0,
        width=500.0,
        height=69.0
    )

    window.add_comment_entry = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.add_comment_entry.place(
        x=602.0,
        y=512.0,
        width=500.0,
        height=142.0
    )

    window.purchase_date_entry = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.purchase_date_entry.place(
        x=382.0,
        y=333.0,
        width=160.0,
        height=45.0
    )

    window.gun_serial_entry = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.gun_serial_entry.place(
        x=802.0,
        y=244.0,
        width=300.0,
        height=45.0
    )

    window.gun_brand_entry = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.gun_brand_entry.place(
        x=36.0,
        y=244.0,
        width=192.0,
        height=45.0
    )

    window.gun_brand_combobox = ttk.Combobox(
        window,
        values=brands
    )
    window.gun_brand_combobox.place(
        x=36.0,
        y=244.0,
        width=192.0,
        height=45.0
    )

    def autocomplete(event):
        entered_text = event.widget.get()
        if entered_text:
            matches = [state for state in brands if state.lower().startswith(entered_text.lower())]
            window.gun_brand_combobox['values'] = matches
        else:
            window.gun_brand_combobox['values'] = brands

    window.gun_brand_combobox.bind('<KeyRelease>', autocomplete)

    window.gun_model_entry = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.gun_model_entry.place(
        x=300.0,
        y=244.0,
        width=430.0,
        height=45.0
    )

    window.customer_entry = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.customer_entry.place(
        x=300.0,
        y=155.0,
        width=426.0,
        height=45.0
    )

    window.customer_combobox = ttk.Combobox(
        window,
        values=customer_names
    )
    window.customer_combobox.place(
        x=300.0,
        y=155.0,
        width=426.0,
        height=45.0
    )

    def on_name_selected(event):
        typed_name = window.customer_combobox.get()  # Get text from ComboBox

        # Find the matching customer in the dictionary
        for customer in customers:
            if customer["FullName"] == typed_name:
                window.customer_combobox.set(customer["CustomerID"])  # Replace name with ID
                break

    def autocomplete(event):
        entered_text = window.customer_combobox.get().strip()

        if entered_text:
            # Find matching names
            matches = [
                customer["FullName"] for customer in customers if customer["FullName"].lower().startswith(entered_text.lower())
            ]
            window.customer_combobox['values'] = matches # Update the drop-down options
        else:
            window.customer_combobox['values'] = customer_names  # Reset to all names

    window.customer_combobox.bind('<KeyRelease>', autocomplete)

    window.customer_combobox.bind("<<ComboboxSelected>>", on_name_selected)

    window.received_by_entry = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.received_by_entry.place(
        x=845.0,
        y=155.0,
        width=255.0,
        height=45.0
    )

    window.canvas.create_text(
        36.0,
        213.0,
        anchor="nw",
        text="Gun Brand*",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        36.0,
        124.0,
        anchor="nw",
        text="Drop Off Date*",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        300.0,
        124.0,
        anchor="nw",
        text="Customer*",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        845.0,
        124.0,
        anchor="nw",
        text="Received By*",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        300.0,
        213.0,
        anchor="nw",
        text="Gun Model*",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        36.0,
        302.0,
        anchor="nw",
        text="Purchase Location",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        382.0,
        302.0,
        anchor="nw",
        text="Purchase Date",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        802.0,
        213.0,
        anchor="nw",
        text="Gun Serial Number*",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        36.0,
        532.0,
        anchor="nw",
        text="Work Description*",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        36.0,
        408.0,
        anchor="nw",
        text="List Previous Upgrades and/or Repairs*",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        602.0,
        357.0,
        anchor="nw",
        text="Additional Parts and Extras",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )

    window.canvas.create_text(
        602.0,
        479.0,
        anchor="nw",
        text="Additional Comments",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )
    window.resizable(False, False)
    window.mainloop()

def open_onboarding(window):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Sean\Documents\VSCODEPROJECTS\AirsoftTechWorker-ATW-v.0.2.0\AirsoftTechWorker-ATW-v.0.2.0\draft_build_1.1\assets")
    window.geometry("1200x720")
    window.configure(bg = "#FFFFFF")
    states = [
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID",
        "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS",
        "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK",
        "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV",
        "WI", "WY"
    ]
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
        command=lambda: (clear_window(window), open_onboarding(window)),
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
        command=lambda: (clear_window(window), open_new_ticket(window)),
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
        command=lambda: (clear_window(window), open_customers(window)),
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
        command=lambda: (clear_window(window), open_tickets(window)),
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
        command=lambda: (clear_window(window), open_inventory(window)),
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
        command=lambda: ob.clear_form(window),
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
        command=lambda: (ob.save_to_access(window)),
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

    window.zipcode_entry = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.zipcode_entry.place(
        x=767.0,
        y=538.0,
        width=272.0,
        height=45.0
    )

    window.state_combobox = ttk.Combobox(
        window,
        values=states
    )
    window.state_combobox.place(
        x=613.0, 
        y=538.0, 
        width=107.0, 
        height=45.0
    )

    def autocomplete(event):
        entered_text = event.widget.get()
        if entered_text:
            matches = [state for state in states if state.lower().startswith(entered_text.lower())]
            window.state_combobox['values'] = matches
        else:
            window.state_combobox['values'] = states

    window.state_combobox.bind('<KeyRelease>', autocomplete)

    window.city_entry = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.city_entry.place(
        x=97.0,
        y=538.0,
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
        x=613.0,
        y=424.0,
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
        x=97.0,
        y=424.0,
        width=426.0,
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
        y=310.0,
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
        x=613.0,
        y=204.0,
        width=426.0,
        height=45.0
    )

    window.email_entry = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    window.email_entry.place(
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

def open_main_menu(window):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Sean\Documents\VSCODEPROJECTS\AirsoftTechWorker-ATW-v.0.2.0\AirsoftTechWorker-ATW-v.0.2.0\draft_build_1.1\assets")
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
        command=lambda: (clear_window(window), open_main_menu(window)),
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
        command=lambda: (clear_window(window), open_customers(window)),
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
        command=lambda: (clear_window(window), open_tickets(window)),
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
        command=lambda: (clear_window(window), open_inventory(window)),
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
        command=lambda: (clear_window(window),open_new_ticket(window)),
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
        command=lambda: (clear_window(window), open_onboarding(window)),
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

    window.canvas.create_text(
        593.0,
        140.0,
        anchor="nw",
        text="Search by name:",
        fill="#000000",
        font=("MergeOne Regular", 24 * -1)
    )


    window.search_bar_field = Entry(
        bd=0,
        bg="#D0D0D0",
        fg="#000716",
        highlightthickness=0
    )
    window.search_bar_field.place(
        x=593.0,
        y=170.0,
        width=559.0,
        height=48.0
    )
    window.resizable(False, False)
    window.mainloop()

def open_login_page():
    window = Tk()
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Sean\Documents\VSCODEPROJECTS\AirsoftTechWorker-ATW-v.0.2.0\AirsoftTechWorker-ATW-v.0.2.0\draft_build_1.1\assets")
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