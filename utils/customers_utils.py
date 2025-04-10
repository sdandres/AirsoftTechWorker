import pyodbc
from utils.path_utils import get_database_conn_str
from tkinter import messagebox

def read_customer_data_from_access():
    """Fetches customer data from the Access database, including address details."""
    
    try:
        conn = pyodbc.connect(get_database_conn_str())
        cursor = conn.cursor()

        # SQL Query
        query = """
            SELECT CustomerID, FirstName, LastName, Email, Mobile, 
                   Address, Address2, City, State, Zipcode 
            FROM Customer
        """
        cursor.execute(query)

        # Fetch all rows
        rows = cursor.fetchall()

        # Convert rows to a list of dictionaries
        customer_data = [
            {
                "CustomerID": row[0],
                "FirstName": row[1],
                "LastName": row[2],
                "Email": row[3],
                "PhoneNumber": row[4],
                "Address": row[5],
                "Address2": row[6] if row[6] else "",  # Optional second address line
                "City": row[7],
                "State": row[8],
                "Zipcode": row[9]
            } for row in rows
        ]

        cursor.close()
        conn.close()

        return customer_data

    except pyodbc.Error as e:
        messagebox.showerror("Database Error", f"Error reading from database: {e}")
        return []  # Return an empty list if there's an error
    