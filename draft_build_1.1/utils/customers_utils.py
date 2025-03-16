import pyodbc
from tkinter import messagebox

# Database connection string
DB_PATH = r"C:\Users\Sean\Documents\VSCODEPROJECTS\AirsoftTechWorker-ATW-v.0.2.0\AirsoftTechWorker-ATW-v.0.2.0\draft_build_1.1\database\AmericaAirsoftDatabase.accdb"

def read_customer_data_from_access():
    """Reads customer data from the Access database and returns it as a list of dictionaries."""
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        fr'DBQ={DB_PATH};'  # Use an f-string for better readability
    )

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # SQL Select Query
        query = "SELECT * FROM Customer"
        cursor.execute(query)

        # Fetch all rows
        rows = cursor.fetchall()

        # Convert rows to a list of dictionaries
        customer_data = [{"FirstName": row[1], "LastName": row[2], "Email": row[3], "PhoneNumber": row[4]} for row in rows]

        cursor.close()
        conn.close()

        return customer_data

    except pyodbc.Error as e:
        messagebox.showerror("Database Error", f"Error reading from database: {e}")
        return []  # Return an empty list if there's an error