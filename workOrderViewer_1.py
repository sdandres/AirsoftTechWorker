import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import pyodbc

class WorkOrderViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("Work Order Viewer")
        self.master.geometry("1000x600")  # Adjusted to match Figma layout size

        # Mapping from display headers to actual database column names
        self.header_key_map = {
            "Order #": "OrderID",
            "CustomerID": "CustomerID",
            "ReceivedBy": "ReceivedBy",
            "Date of Approval": "DateofApproval",
            "WorkCompletedBy": "WorkCompletedBy",
            "Expected Finish Date": "ExpectedFinishDate",
            "Drop-off Date": "DropOffDate",
            "Pick-up Date": "PickUpDate"
        }

        # These are the “friendly” headers shown in the table
        self.headers = [
            "Order #", "CustomerID", "ReceivedBy", "Date of Approval",
            "WorkCompletedBy", "Expected Finish Date", "Drop-off Date", "Pick-up Date"
        ]

        # Database connection
        self.conn = pyodbc.connect(
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ=path_to_your_database.accdb;'  # Replace with your Access DB path
        )
        self.cursor = self.conn.cursor()

        # Main frame
        self.main_frame = ttk.Frame(self.master, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Configure grid weights for resizing
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Navigation bar
        nav_frame = ttk.Frame(self.main_frame, height=50, style="Nav.TFrame")
        nav_frame.grid(row=0, column=0, sticky="ew")
        nav_buttons = [
            ("Home", lambda: print("Home clicked")),
            ("Onboarding", lambda: print("Onboarding clicked")),
            ("New Ticket", lambda: print("New Ticket clicked")),
            ("Customers", lambda: print("Customers clicked")),
            ("Tickets", None),  # This section is active
            ("Inventory", lambda: print("Inventory clicked"))
        ]
        for i, (text, cmd) in enumerate(nav_buttons):
            btn = ttk.Button(nav_frame, text=text, command=cmd, style="Nav.TButton")
            btn.grid(row=0, column=i, padx=5, pady=5)

        # Search bar
        self.search_frame = ttk.Frame(self.main_frame, height=30)
        self.search_frame.grid(row=1, column=0, sticky="ew", pady=(5, 10))
        self.search_entry = ttk.Entry(self.search_frame, width=30)
        self.search_entry.grid(row=0, column=0, padx=5)
        ttk.Button(self.search_frame, text="Search", command=self.filter_records).grid(row=0, column=1, padx=5)

        # Table frame
        table_frame = ttk.Frame(self.main_frame)
        table_frame.grid(row=2, column=0, sticky="nsew")

        self.button_frame = ttk.Frame(table_frame, width=30)
        self.button_frame.grid(row=0, column=0, sticky="ns", padx=(0, 5))

        self.display_frame = ttk.Frame(table_frame)
        self.display_frame.grid(row=0, column=1, sticky="nsew")

        self.edit_buttons = []
        self.load_records()

        # Styling (approximate colors)
        self.master.configure(bg="#2c3e50")  # Dark blue background
        style = ttk.Style()
        style.configure("Nav.TFrame", background="#3498db")  # Light blue for nav bar
        style.configure("Nav.TButton", background="#3498db", foreground="white", font=("Arial", 10))
        style.configure("Treeview", background="#ecf0f1", fieldbackground="#ecf0f1", font=("Arial", 10))
        style.configure("TFrame", background="#2c3e50")

    def load_records(self):
        # Clear existing widgets
        for widget in self.display_frame.winfo_children():
            widget.destroy()
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        # Create Treeview
        self.tree = ttk.Treeview(self.display_frame, columns=self.headers, show="headings", height=9)
        for col in self.headers:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="w")
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.display_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Configure frame for resizing
        self.display_frame.grid_columnconfigure(0, weight=1)
        self.display_frame.grid_rowconfigure(0, weight=1)

        # Fetch records from the database
        self.cursor.execute("SELECT * FROM Orders LIMIT 9")  # Limiting to 9 rows
        records = self.cursor.fetchall()

        # Display records and create edit buttons
        for row, record in enumerate(records, 1):
            btn = ttk.Button(self.button_frame, text="✏", command=lambda r=record: self.open_editor(r))
            btn.grid(row=row-1, column=0, pady=2, sticky="w")
            self.edit_buttons.append(btn)

            # Map database record (tuple) to display values using header_key_map
            values = [
                str(record[self.headers.index(h)] if record[self.headers.index(h)] is not None else "")
                for h in self.headers
            ]
            self.tree.insert("", "end", iid=record[0], values=values)  # Using OrderID (index 0) as iid

    def filter_records(self):
        search_term = self.search_entry.get().lower()
        # Searching by OrderID or CustomerID in the database
        query = """
            SELECT * FROM Orders 
            WHERE OrderID LIKE ? OR CustomerID LIKE ?
            LIMIT 9
        """
        self.cursor.execute(query, (f'%{search_term}%', f'%{search_term}%'))
        filtered_records = self.cursor.fetchall()
        self.load_records_with_data(filtered_records)

    def load_records_with_data(self, data):
        for widget in self.display_frame.winfo_children():
            widget.destroy()
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        self.tree = ttk.Treeview(self.display_frame, columns=self.headers, show="headings", height=9)
        for col in self.headers:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="w")
        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.display_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.display_frame.grid_columnconfigure(0, weight=1)
        self.display_frame.grid_rowconfigure(0, weight=1)

        for row, record in enumerate(data[:9], 1):
            btn = ttk.Button(self.button_frame, text="✏", command=lambda r=record: self.open_editor(r))
            btn.grid(row=row-1, column=0, pady=2, sticky="w")
            self.edit_buttons.append(btn)

            values = [
                str(record[self.headers.index(h)] if record[self.headers.index(h)] is not None else "")
                for h in self.headers
            ]
            self.tree.insert("", "end", iid=record[0], values=values)  # Using OrderID (index 0) as iid

    def open_editor(self, record):
        editor = tk.Toplevel(self.master)
        editor.title("Edit Work Order")
        editor.geometry("400x400")

        # These are the user-friendly labels to display in the editor
        labels = [
            "Order #", "Customer ID", "Received By", "Date of Approval",
            "Work Completed By", "Expected Finish Date", "Drop-off Date", "Pick-up Date"
        ]
        entries = []
        
        for i, (label, header) in enumerate(zip(labels, self.headers)):
            ttk.Label(editor, text=label).grid(row=i, column=0, padx=5, pady=5)
            entry = ttk.Entry(editor)
            entry.grid(row=i, column=1, padx=5, pady=5)
            # Use the database record (tuple) directly, indexed by position
            entry.insert(
                0,
                str(record[self.headers.index(header)] if record[self.headers.index(header)] is not None else "")
            )
            entries.append(entry)

        # Buttons
        ttk.Button(
            editor, text="Save",
            command=lambda: self.save_changes(record[0], entries, editor)  # Use OrderID (index 0)
        ).grid(row=9, column=0, pady=10)

        ttk.Button(
            editor, text="Delete",
            command=lambda: self.delete_record(record[0], editor)  # Use OrderID (index 0)
        ).grid(row=9, column=1, pady=10)

    def validate_date(self, date_str):
        try:
            if date_str:
                datetime.strptime(date_str, '%Y-%m-%d')
                return True
            return True  # Allow empty dates
        except ValueError:
            return False

    def save_changes(self, order_id, entries, window):
        values = [entry.get() for entry in entries]
        
        # Validate the date fields: indexes 3, 5, 6, 7 in your `values`
        for date_str in [values[3], values[5], values[6], values[7]]:
            if not self.validate_date(date_str):
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
                return

        if messagebox.askyesno("Confirm", "Save changes?"):
            # Update the database
            update_query = """
                UPDATE Orders 
                SET CustomerID=?, ReceivedBy=?, DateofApproval=?,
                    WorkCompletedBy=?, ExpectedFinishDate=?, DropOffDate=?, PickUpDate=?
                WHERE OrderID=?
            """
            self.cursor.execute(update_query, (
                values[1], values[2], values[3],  # CustomerID, ReceivedBy, DateofApproval
                values[4], values[5], values[6], values[7],  # WorkCompletedBy, ExpectedFinishDate, DropOffDate, PickUpDate
                order_id  # OrderID for WHERE clause
            ))
            self.conn.commit()
            self.load_records()
            window.destroy()
            messagebox.showinfo("Success", "Record updated successfully")

    def delete_record(self, order_id, window):
        if messagebox.askyesno("Confirm", "Delete this record?"):
            self.cursor.execute("DELETE FROM Orders WHERE OrderID=?", (order_id,))
            self.conn.commit()
            self.load_records()
            window.destroy()
            messagebox.showinfo("Success", "Record deleted successfully")

    def __del__(self):
        # Ensure database connection is closed when the object is destroyed
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

def main():
    root = tk.Tk()
    app = WorkOrderViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()