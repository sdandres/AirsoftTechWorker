import pyodbc
import tkinter as tk
from tkinter import messagebox

DB_PATH = r"C:\Users\Sean\Documents\VSCODEPROJECTS\AirsoftTechWorker-ATW-v.0.2.0\AirsoftTechWorker-ATW-v.0.2.0\draft_build_1.1\database\AmericaAirsoftDatabase.accdb"

def read_ticket_data_from_access():
    """Reads all data from Customer and Guns tables and merges them."""
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        fr'DBQ={DB_PATH};'  # Ensure correct path
    )

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Query to select all columns from Guns (Tickets) and Customer
        query = """
        SELECT 
            g.[OrderID] AS TicketID, 
            g.[DropOffDate], 
            g.[CustomerID], 
            g.[Employee], 
            g.[GunBrand], 
            g.[GunModel], 
            g.[SerialNum], 
            g.[PurchaseLocation], 
            g.[PurchaseDate], 
            g.[PastInfo], 
            g.[WorkDescription], 
            g.[AdditionalParts], 
            g.[AdditionalComments], 
            c.[CustomerID] AS CustID, 
            c.[FirstName], 
            c.[LastName], 
            c.[Email], 
            c.[Mobile] AS PhoneNumber, 
            c.[Address], 
            c.[Address2], 
            c.[City], 
            c.[State], 
            c.[Zipcode]
        FROM Guns AS g
        LEFT JOIN Customer AS c ON g.[CustomerID] = c.[CustomerID];
        """
        
        cursor.execute(query)

        # Get column names
        columns = [column[0] for column in cursor.description]

        # Fetch all records and create dictionaries
        tickets = [dict(zip(columns, row)) for row in cursor.fetchall()]

        cursor.close()
        conn.close()

        print(f"📋 Retrieved {len(tickets)} tickets.")  # Debugging output
        return tickets

    except Exception as e:
        messagebox.showerror("Database Error", f"Error retrieving tickets: {e}")
        return []


def edit_ticket_window(ticket):
    """Opens a window to edit ticket details with full customer & gun info."""
    edit_window = tk.Toplevel()
    edit_window.title(f"Edit Ticket ID {ticket['TicketID']}")

    fields = {
        "First Name": ticket["FirstName"],
        "Last Name": ticket["LastName"],
        "Phone Number": ticket["PhoneNumber"],
        "Email": ticket["Email"],
        "Gun Brand": ticket["GunBrand"],
        "Gun Model": ticket["GunModel"],
        "Serial Number": ticket["SerialNum"],
        "Drop-Off Date": ticket["DropOffDate"],
        "Employee": ticket["Employee"],
        "Purchase Location": ticket["PurchaseLocation"],
        "Purchase Date": ticket["PurchaseDate"],
        "Past Info": ticket["PastInfo"],
        "Work Description": ticket["WorkDescription"],
        "Additional Parts": ticket["AdditionalParts"],
        "Additional Comments": ticket["AdditionalComments"]
    }

    entry_widgets = {}

    for idx, (label, value) in enumerate(fields.items()):
        tk.Label(edit_window, text=label).grid(row=idx, column=0, padx=5, pady=5)
        entry = tk.Entry(edit_window, width=50)
        entry.insert(0, str(value))  # Pre-fill with existing data
        entry.grid(row=idx, column=1, padx=5, pady=5)
        entry_widgets[label] = entry

    def save_changes():
        """Saves the edited gun data back to the database."""
        updated_data = {label: entry_widgets[label].get() for label in fields}

        conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            fr'DBQ={DB_PATH};'
        )

        try:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()

            # SQL Update Query for Guns table only (Customer details remain unchanged)
            
            query = """
                UPDATE Guns 
                SET 
                    [GunBrand] = ?, 
                    [GunModel] = ?, 
                    [SerialNum] = ?, 
                    [DropOffDate] = ?, 
                    [Employee] = ?, 
                    [PurchaseLocation] = ?, 
                    [PurchaseDate] = ?, 
                    [PastInfo] = ?, 
                    [WorkDescription] = ?, 
                    [AdditionalParts] = ?, 
                    [AdditionalComments] = ? 
                WHERE [OrderID] = ?
            """

            cursor.execute(query, (
                updated_data["Gun Brand"],
                updated_data["Gun Model"],
                updated_data["Serial Number"],
                updated_data["Drop-Off Date"],
                updated_data["Employee"],
                updated_data["Purchase Location"],
                updated_data["Purchase Date"],
                updated_data["Past Info"],
                updated_data["Work Description"],
                updated_data["Additional Parts"],  # Matches exact column name in database
                updated_data["Additional Comments"],  # Matches exact column name in database
                ticket["TicketID"]  # OrderID is used for lookup
            ))
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Ticket updated successfully!")

        except Exception as e:
            messagebox.showerror("Database Error", f"Error updating ticket: {e}")

    # Save button
    tk.Button(edit_window, text="Save Changes", command=save_changes).grid(row=len(fields), column=0, columnspan=2, pady=10)