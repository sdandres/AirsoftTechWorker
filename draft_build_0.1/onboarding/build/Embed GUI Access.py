import tkinter as tk
from tkinter import Canvas, Button, PhotoImage, messagebox
from tkinter import ttk  # for Combobox and Entry
from tkinter import messagebox,simpledialog
import pandas as pd
import re
from pathlib import Path
from customer import CustomerObject
import pyodbc

# ================
# DESIGNER SECTION
# ================


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\madlynedodds\Desktop\GUI\github\AirsoftTechWorker-main\AirsoftTechWorker-main\draft_build_0.1\onboarding\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = tk.Tk()
window.geometry("1200x720")
window.configure(bg="#FFFFFF")

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

# Buttons from Designer
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    window,
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(x=0, y=0, width=200, height=100)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=3,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(x=200.0, y=0.0, width=200.0, height=100.0)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=3,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(x=400.0, y=0.0, width=200.0, height=100.0)

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=3,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(x=600.0, y=0.0, width=200.0, height=100.0)

button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=3,
    command=lambda: print("button_5 clicked"),
    relief="flat"
)
button_5.place(x=800.0, y=0.0, width=200.0, height=100.0)

button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=3,
    command=lambda: print("button_6 clicked"),
    relief="flat"
)
button_6.place(x=1000.0, y=0.0, width=200.0, height=100.0)

# Texts that label each entry field:
canvas.create_text(99.0, 169.0, anchor="nw", text="First Name*", fill="#000000", font=20)
canvas.create_text(613.0, 169.0, anchor="nw", text="Last Name*", fill="#000000", font=20)
canvas.create_text(96.0, 276.0, anchor="nw", text="Email*", fill="#000000", font=20)
canvas.create_text(613.0, 276.0, anchor="nw", text="Mobile*", fill="#000000", font=20)
canvas.create_text(96.0, 386.0, anchor="nw", text="Address", fill="#000000", font=20)
canvas.create_text(613.0, 386.0, anchor="nw", text="Address 2", fill="#000000", font=20)
canvas.create_text(97.0, 500.0, anchor="nw", text="City", fill="#000000", font=20)
canvas.create_text(613.0, 500.0, anchor="nw", text="State", fill="#000000", font=20)
canvas.create_text(767.0, 500.0, anchor="nw", text="Zipcode", fill="#000000", font=20)

# Create a custom style for ttk.Entry to add internal padding
style = ttk.Style(window)
style.configure(
    "Custom.TEntry",
    padding=(10, 5, 10, 5),         # (left, top, right, bottom)
    foreground="#000716",
    fieldbackground="#D9D9D9",
    font=("Arial", 20)
)

# -- Create Entry widgets using ttk.Entry with the custom style --

# 1) First Name
entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(310.0, 227.5, image=entry_image_1)
entry_1 = ttk.Entry(window, style="Custom.TEntry", font=20)
entry_1.place(x=97.0, y=204.0, width=426.0, height=45.0)

# 2) Last Name
entry_image_8 = PhotoImage(file=relative_to_assets("entry_8.png"))
entry_bg_8 = canvas.create_image(826.0, 227.5, image=entry_image_8)
entry_8 = ttk.Entry(window, style="Custom.TEntry", font=20)
entry_8.place(x=613.0, y=204.0, width=426.0, height=45.0)

# 3) Email
entry_image_9 = PhotoImage(file=relative_to_assets("entry_9.png"))
entry_bg_9 = canvas.create_image(309.0, 333.5, image=entry_image_9)
entry_9 = ttk.Entry(window, style="Custom.TEntry", font=20)
entry_9.place(x=96.0, y=310.0, width=426.0, height=45.0)

# 4) Mobile
entry_image_7 = PhotoImage(file=relative_to_assets("entry_7.png"))
entry_bg_7 = canvas.create_image(826.0, 333.5, image=entry_image_7)
entry_7 = ttk.Entry(window, style="Custom.TEntry", font=20)
entry_7.place(x=613.0, y=310.0, width=426.0, height=45.0)

# 5) Address
entry_image_6 = PhotoImage(file=relative_to_assets("entry_6.png"))
entry_bg_6 = canvas.create_image(310.0, 447.5, image=entry_image_6)
entry_6 = ttk.Entry(window, style="Custom.TEntry", font = 20)
entry_6.place(x=97.0, y=424.0, width=426.0, height=45.0)

# 6) Address 2
entry_image_5 = PhotoImage(file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(826.0, 447.5, image=entry_image_5)
entry_5 = ttk.Entry(window, style="Custom.TEntry", font=20)
entry_5.place(x=613.0, y=424.0, width=426.0, height=45.0)

# 7) City
entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(310.0, 561.5, image=entry_image_4)
entry_4 = ttk.Entry(window, style="Custom.TEntry", font=20)
entry_4.place(x=97.0, y=538.0, width=426.0, height=45.0)

# 8) State (we'll replace this Entry with a Combobox below)
entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(666.5, 561.5, image=entry_image_3)
entry_3 = ttk.Entry(window, style="Custom.TEntry", font = 20)
entry_3.place(x=613.0, y=538.0, width=107.0, height=45.0)

# 9) Zipcode
entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(903.0, 561.5, image=entry_image_2)
entry_2 = ttk.Entry(window, style="Custom.TEntry", font=20)
entry_2.place(x=767.0, y=538.0, width=272.0, height=45.0)

# =======================
# BACKEND / LOGIC SECTION
# =======================

# Replace the "State" Entry with a Combobox
entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))  # for placement
entry_bg_3 = canvas.create_image(666.5, 561.5, image=entry_image_3)  # for placement
entry_3.destroy()  # Remove the old State entry

states = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID",
    "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS",
    "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK",
    "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV",
    "WI", "WY"
]
state_combobox = ttk.Combobox(window, values=states, font=("Arial", 15))
state_combobox.place(x=613.0, y=538.0, width=107.0, height=45.0)

def autocomplete(event):
    entered_text = event.widget.get()
    if entered_text:
        matches = [state for state in states if state.lower().startswith(entered_text.lower())]
        state_combobox['values'] = matches
    else:
        state_combobox['values'] = states

state_combobox.bind('<KeyRelease>', autocomplete)

def generate_customer_id(last_name, mobile):
    last_name_part = last_name[:3].upper() if last_name else "XXX"
    mobile_part = mobile[-4:] if mobile else "0000"
    return f"{last_name_part}{mobile_part}"

def validate_data():
    # First Name
    if not entry_1.get().strip():
        messagebox.showerror("Invalid Input", "First Name cannot be empty.")
        return False

    # Last Name
    if not entry_8.get().strip():
        messagebox.showerror("Invalid Input", "Last Name cannot be empty.")
        return False

    # Email
    email = entry_9.get().strip()
    if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        messagebox.showerror("Invalid Input", "Please enter a valid email address.")
        return False

    # Check for duplicate email
    if check_duplicate_email(email):
        messagebox.showerror("Duplicate Email", "Email address already exists.")
        return False

    # Mobile
    phone_number = entry_7.get().strip()
    phone_digits = phone_number.replace('-', '')
    if not phone_digits.isdigit() or len(phone_digits) != 10:
        messagebox.showerror("Invalid Input", "Please enter a valid 10-digit phone number (dashes are allowed).")
        return False

    # Check for duplicate phone number
    if check_duplicate_phone(phone_number):
        messagebox.showerror("Duplicate Phone Number", "Phone number already exists.")
        return False

    # Address
    if not entry_6.get().strip():
        messagebox.showerror("Invalid Input", "Address cannot be empty.")
        return False

    # City
    if not entry_4.get().strip():
        messagebox.showerror("Invalid Input", "City cannot be empty.")
        return False

    # State (from combobox)
    state = state_combobox.get().strip()

    if not state:
        messagebox.showerror("Invalid Input", "Please select a state.")
        return False

    # Check if state is exactly two uppercase letters
    if len(state) != 2 or not state.isupper():
        messagebox.showerror("Invalid Input", "State must have two uppercase letters.")
        return False

    # Zipcode
    zipcode = entry_2.get().strip()
    if not zipcode.isdigit() or len(zipcode) != 5:
        messagebox.showerror("Invalid Input", "Please enter a valid 5-digit zipcode.")
        return False

    return True

def check_duplicate_email(email):
    """Checks if the email already exists in the Access database."""
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=C:\Users\madlynedodds\Documents\AmericaAirsoft.accdb;'
    )

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # SQL Query to check for duplicate email
        query = "SELECT COUNT(*) FROM Customer WHERE Email = ?"
        cursor.execute(query, (email,))
        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return count > 0  # True if duplicate exists, False otherwise

    except pyodbc.Error as e:
        messagebox.showerror("Database Error", f"Error checking duplicate email: {e}")
        return False  # Assume duplicate on error to prevent saving

def check_duplicate_phone(phone):
    """Checks if the phone number already exists in the Access database."""
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=C:\Users\madlynedodds\Documents\AmericaAirsoft.accdb;'
    )

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # SQL Query to check for duplicate phone number
        query = "SELECT COUNT(*) FROM Customer WHERE Mobile = ?"
        print(f"Checking for duplicate phone: '{phone}'") #Debuging print statement
        cursor.execute(query, (phone,))
        count = cursor.fetchone()[0]
        print(f"Count of matching phones: {count}") #Debuging print statement

        cursor.close()
        conn.close()

        return count > 0  # True if duplicate exists, False otherwise

    except pyodbc.Error as e:
        messagebox.showerror("Database Error", f"Error checking duplicate phone number: {e}")
        return False  # Assume duplicate on error to prevent saving

def save_to_access():
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=C:\Users\madlynedodds\Documents\AmericaAirsoft.accdb;'
    )
    
    if not validate_data():  # Call validate_data()
        return  # Stop if validation fails
    
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()


        # Collect data from form entries
        first_name = entry_1.get()
        last_name = entry_8.get()
        email = entry_9.get()
        mobile = entry_7.get()
        address = entry_6.get()
        address2 = entry_5.get()
        city = entry_4.get()
        state = state_combobox.get()  # Example for combobox state field
        zipcode = entry_2.get()

        # SQL Insert Query
        query = """
        INSERT INTO Customer (FirstName, LastName, Email, Mobile, Address, Address2, City, State, Zipcode)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        # Execute query
        cursor.execute(query, (first_name, last_name, email, mobile, address, address2, city, state, zipcode))
        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Success", "Customer saved to Access database.")
    except Exception as e:
        messagebox.showerror("Database Error", f"Error saving to database: {e}")

def read_customer_data_from_access():
    """Reads customer data from the Access database and returns it as a list of dictionaries."""
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=C:\Users\madlynedodds\Documents\AmericaAirsoft.accdb;'
    )

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # SQL Select Query
        query = "SELECT * FROM Customer"
        cursor.execute(query)

        # Fetch all rows
        rows = cursor.fetchall()

        # Get column names (descriptions)
        columns = [column[0] for column in cursor.description]

        # Convert rows to a list of dictionaries
        customer_data = [dict(zip(columns, row)) for row in rows]

        cursor.close()
        conn.close()

        return customer_data

    except pyodbc.Error as e:
        messagebox.showerror("Database Error", f"Error reading from database: {e}")
        return []  # Return an empty list if there's an error


def clear_form():
    entry_1.delete(0, tk.END)
    entry_8.delete(0, tk.END)
    entry_9.delete(0, tk.END)
    entry_7.delete(0, tk.END)
    entry_6.delete(0, tk.END)
    entry_5.delete(0, tk.END)
    entry_4.delete(0, tk.END)
    state_combobox.set('')
    entry_2.delete(0, tk.END)

# ===============================
# BUTTONS FOR BACKEND OPERATIONS
# ===============================

save_button = tk.Button(
    window,
    text="Save",
    font=("Arial", 14),
    bg="#5F74BD",
    command=save_to_access
)
save_button.place(x=1000, y=600, width=80, height=40)

clear_button = tk.Button(
    window,
    text="Clear",
    font=("Arial", 14),
    command=clear_form
)
clear_button.place(x=900, y=600, width=80, height=40)

window.resizable(False, False)
window.mainloop()
