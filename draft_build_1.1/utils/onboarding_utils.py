from tkinter import END, messagebox
import re
import pyodbc

states = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID",
    "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS",
    "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK",
    "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV",
    "WI", "WY"
]

def generate_customer_id(last_name, mobile):
    last_name_part = last_name[:3].upper() if last_name else "XXX"
    mobile_part = mobile[-4:] if mobile else "0000"
    return f"{last_name_part}{mobile_part}"

def validate_data(window):
    # First Name
    if not window.first_name_entry.get().strip():
        messagebox.showerror("Invalid Input", "First Name cannot be empty.")
        return False

    # Last Name
    if not window.last_name_entry.get().strip():
        messagebox.showerror("Invalid Input", "Last Name cannot be empty.")
        return False

    # Email
    email = window.email_entry.get().strip()
    if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        messagebox.showerror("Invalid Input", "Please enter a valid email address.")
        return False

    # Check for duplicate email
    if check_duplicate_email(email):
        messagebox.showerror("Duplicate Email", "Email address already exists.")
        return False

    # Mobile
    phone_number = window.phone_number_entry.get().strip()
    phone_digits = phone_number.replace('-', '')
    if not phone_digits.isdigit() or len(phone_digits) != 10:
        messagebox.showerror("Invalid Input", "Please enter a valid 10-digit phone number (dashes are allowed).")
        return False

    # Check for duplicate phone number
    if check_duplicate_phone(phone_number):
        messagebox.showerror("Duplicate Phone Number", "Phone number already exists.")
        return False

    # State (from combobox)
    state = window.state_combobox.get().strip()

    if not state:
        messagebox.showerror("Invalid Input", "Please select a state.")
        return False

    # Check if state is exactly two uppercase letters
    if len(state) != 2 or not state.isupper():
        messagebox.showerror("Invalid Input", "State must have two uppercase letters.")
        return False

    return True

def check_duplicate_email(email):
    """Checks if the email already exists in the Access database."""
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=C:\Users\Sean\Documents\VSCODEPROJECTS\AirsoftTechWorker-ATW-v.0.2.0\AirsoftTechWorker-ATW-v.0.2.0\draft_build_1.1\database\AmericaAirsoftDatabase.accdb;'
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
        r'DBQ=C:\Users\Sean\Documents\VSCODEPROJECTS\AirsoftTechWorker-ATW-v.0.2.0\AirsoftTechWorker-ATW-v.0.2.0\draft_build_1.1\database\AmericaAirsoftDatabase.accdb;'
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

def save_to_access(window):
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=C:\Users\Sean\Documents\VSCODEPROJECTS\AirsoftTechWorker-ATW-v.0.2.0\AirsoftTechWorker-ATW-v.0.2.0\draft_build_1.1\database\AmericaAirsoftDatabase.accdb;'
    )
    
    if not validate_data(window):  # Call validate_data()
        return  # Stop if validation fails
    
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()


        # Collect data from form entries
        first_name = window.first_name_entry.get()
        last_name = window.last_name_entry.get()
        email = window.email_entry.get()
        mobile = window.phone_number_entry.get()
        address = window.address1_entry.get()
        address2 = window.address2_entry.get()
        city = window.city_entry.get()
        state = window.state_combobox.get()  # Example for combobox state field
        zipcode = window.zipcode_entry.get()

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
    clear_form(window)
    

def read_customer_data_from_access():
    """Reads customer data from the Access database and returns it as a list of dictionaries."""
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=C:\Users\Sean\Documents\VSCODEPROJECTS\AirsoftTechWorker-ATW-v.0.2.0\AirsoftTechWorker-ATW-v.0.2.0\draft_build_1.1\database\AmericaAirsoftDatabase.accdb;'
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


def clear_form(window):
    window.first_name_entry.delete(0, END)
    window.last_name_entry.delete(0, END)
    window.email_entry.delete(0, END)
    window.phone_number_entry.delete(0, END)
    window.address1_entry.delete(0, END)
    window.address2_entry.delete(0, END)
    window.city_entry.delete(0, END)
    window.state_combobox.set('')
    window.zipcode_entry.delete(0, END)