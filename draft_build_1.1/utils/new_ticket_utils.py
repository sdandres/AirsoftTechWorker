from tkinter import END, messagebox
from datetime import datetime
from utils.path_utils import get_database_conn_str
import pyodbc

def validate_data(window):
    if not window.drop_off_date_entry.get().strip():
        messagebox.showerror("Invalid Input", "Drop off date cannot be empty.")
        return False

    if not window.customer_combobox.get().strip():
        messagebox.showerror("Invalid Input", "Customer cannot be empty.")
        return False

    if not window.received_by_entry.get().strip():
        messagebox.showerror("Invalid Input", "Received by cannot be empty.")
        return False
    
    if not window.gun_brand_combobox.get().strip():
        messagebox.showerror("Invalid Input", "Gun brand cannot be empty.")
        return False
    
    if not window.past_entry.get().strip():
        messagebox.showerror("Invalid Input", "Past upgrades/repairs cannot be empty.")
        return False
    
    if not window.work_entry.get().strip():
        messagebox.showerror("Invalid Input", "Work description cannot be empty.")
        return False
    
    return True

def save_to_access(window):
    
    if not validate_data(window):  # Call validate_data()
        return  # Stop if validation fails
    
    try:
        conn = pyodbc.connect(get_database_conn_str())
        cursor = conn.cursor()

        # Insert into Guns table
        guns_insert_query = """
        INSERT INTO Guns (CustomerID, DropOffDate, GunBrand, GunModel, SerialNum, PurchaseLocation, PurchaseDate, PastInfo, PickUpDate)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        print("into guns")

        def parse_optional_date(date_str):
            date_str = date_str.strip()
            if date_str == "":
                return None
            return datetime.strptime(date_str, "%m/%d/%Y").date()
        guns_values = (
            window.hidden_customer_id.get(),
            datetime.strptime(window.drop_off_date_entry.get(), "%m/%d/%Y"),
            window.gun_brand_combobox.get(),
            window.gun_model_entry.get(),
            window.gun_serial_entry.get(),
            window.purchase_location_entry.get(),
            parse_optional_date(window.purchase_date_entry.get()),
            window.past_entry.get(),
            None
        )
        print(guns_values)

        print("guns q")
        cursor.execute(guns_insert_query, guns_values)

        print("guns c")
        # Retrieve generated GunID
        cursor.execute("SELECT @@IDENTITY")
        gun_id = cursor.fetchone()[0]

        # Insert into Labor table
        labor_insert_query = """
        INSERT INTO Labor (GunID, Employee, WorkDescription, AdditionalComments, AdditionalParts, Technician, LaborType, LaborPrice, LaborStatus, CompleteDate)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        print("into labor")
        labor_values = (
            gun_id,
            window.received_by_entry.get(),
            window.work_entry.get(),
            window.add_comment_entry.get(),
            window.add_parts_entry.get(),
            None,
            None,
            None,
            None,
            None,
        )
        print("labor q")
        cursor.execute(labor_insert_query, labor_values)

        print("labor c")

        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Success", "Gun record added successfully!")

    except Exception as e:
        messagebox.showerror("Database Error", f"Error saving to database: {e}")
    clear_form(window)

def format_customer_data(customers):
    """Takes a list of customer dictionaries and returns a list with CustomerID and FullName."""
    
    formatted_list = [
        {"CustomerID": customer["CustomerID"], "FullName": f"{customer['FirstName']} {customer['LastName']}"}
        for customer in customers if "CustomerID" in customer and "FirstName" in customer and "LastName" in customer
    ]

    return formatted_list

def clear_form(window):
    """Clears all input fields, including Comboboxes, in the gun submission form."""
    window.drop_off_date_entry.delete(0, END)
    window.customer_combobox.set('')  # Clear ComboBox selection
    window.received_by_entry.delete(0, END)
    window.gun_brand_combobox.set('')  # Clear ComboBox selection
    window.gun_model_entry.delete(0, END)
    window.gun_serial_entry.delete(0, END)
    window.purchase_location_entry.delete(0, END)
    window.purchase_date_entry.delete(0, END)
    window.past_entry.delete(0, END)
    window.work_entry.delete(0, END)
    window.add_parts_entry.delete(0, END)
    window.add_comment_entry.delete(0, END)