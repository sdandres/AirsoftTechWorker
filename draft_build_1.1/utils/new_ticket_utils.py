from tkinter import END, messagebox
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
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=C:\Users\Sean\Documents\VSCODEPROJECTS\AirsoftTechWorker-ATW-v.0.2.0\AirsoftTechWorker-ATW-v.0.2.0\draft_build_1.1\database\AmericaAirsoftDatabase.accdb;'
    )
    
    if not validate_data(window):  # Call validate_data()
        return  # Stop if validation fails
    
    try:
        conn = pyodbc.connect(conn_str)
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
    

def read_customer_name_data_from_access():
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=C:\Users\Sean\Documents\VSCODEPROJECTS\AirsoftTechWorker-ATW-v.0.2.0\AirsoftTechWorker-ATW-v.0.2.0\draft_build_1.1\database\AmericaAirsoftDatabase.accdb;'
    )

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # SQL Select Query (fetch FirstName and LastName separately)
        query = "SELECT CustomerID, FirstName, LastName FROM Customer"
        cursor.execute(query)

        # Fetch all rows
        rows = cursor.fetchall()

        # Convert rows to a list of dictionaries with full name (handling None values)
        customer_data = [
            {
                "CustomerID": row[0], 
                "FullName": f"{row[1] or ''} {row[2] or ''}".strip()
            }
            for row in rows
        ]

        cursor.close()
        conn.close()

        return customer_data

    except pyodbc.Error as e:
        messagebox.showerror("Database Error", f"Error reading from database: {e}")
        return []  # Return an empty list if there's an error

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