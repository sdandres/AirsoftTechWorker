from tkinter import END, messagebox
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

        # SQL Insert Query
        query = """
        INSERT INTO Guns (DropOffDate, CustomerID, Employee, GunBrand, GunModel, SerialNum, PurchaseLocation, PurchaseDate, PastInfo, WorkDescription, AdditionalParts, AdditionalComments)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        # Execute query
        cursor.execute(query, (
            window.drop_off_date_entry.get(),
            window.customer_combobox.get(),
            window.received_by_entry.get(),
            window.gun_brand_combobox.get(),
            window.gun_model_entry.get(),
            window.gun_serial_entry.get(),
            window.purchase_location_entry.get(),
            window.purchase_date_entry.get(),
            window.past_entry.get(),
            window.work_entry.get(),
            window.add_parts_entry.get(),
            window.add_comment_entry.get()
        ))
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