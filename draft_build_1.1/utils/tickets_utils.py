import pyodbc
from utils.path_utils import get_database_conn_str
from utils.onboarding_utils import read_customer_data_from_access
from utils.new_ticket_utils import format_customer_data
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk, END

# Labor price dictionary
labor_prices = {
    "Did not specify": "",
    "External": "30",
    "Internal": "60",
    "External & Internal": "75",
    "Advanced": "80",
    "Connector Swap": "19",
    "Custom": ""  # Blank for manual input
}

def update_totals(price_entry, parts_tree, subtotal_label, tax_entry, total_label):
    """Calculates and updates subtotal, tax, and total amount dynamically."""
    try:
        labor_cost = float(price_entry.get()) if price_entry.get() else 0
        parts_cost = sum(float(parts_tree.item(item, "values")[2][1:]) for item in parts_tree.get_children())  # Extracting price
        subtotal = labor_cost + parts_cost
        tax = (subtotal * float(tax_entry.get()) / 100) if tax_entry.get() else 0
        total = subtotal + tax
        subtotal_label.config(text=f"Subtotal: ${subtotal:.2f}")
        total_label.config(text=f"Total: ${total:.2f}")
    except ValueError:
        pass  # Prevents crashes due to empty/non-numeric values

def add_part_to_tree(part_name_entry, part_qty_entry, part_price_entry, parts_tree, price_entry, subtotal_label, tax_entry, total_label):
    """Adds a part to the Treeview with name, quantity, and price."""
    
    item = part_name_entry.get().strip()
    qty = part_qty_entry.get().strip()
    price = part_price_entry.get().strip()

    if item and qty.isdigit() and price.replace(".", "", 1).isdigit():
        total_price = float(qty) * float(price)
        parts_tree.insert("", "end", values=(item, qty, f"${total_price:.2f}"))

        part_name_entry.delete(0, tk.END)
        part_qty_entry.delete(0, tk.END)
        part_price_entry.delete(0, tk.END)

        update_totals(price_entry, parts_tree, subtotal_label, tax_entry, total_label)
    else:
        messagebox.showerror("Input Error", "Please enter a valid item, quantity, and price.")

def delete_part_from_tree(parts_tree, price_entry, subtotal_label, tax_entry, total_label):
    """Deletes the selected part from the Treeview."""
    
    selected_item = parts_tree.selection()
    if selected_item:
        parts_tree.delete(selected_item)
        update_totals(price_entry, parts_tree, subtotal_label, tax_entry, total_label)
    else:
        messagebox.showerror("Selection Error", "Please select a part to delete.")

def read_ticket_data_from_access():
    try:
        conn = pyodbc.connect(get_database_conn_str())
        cursor = conn.cursor()

        # Query to select all columns from Guns (Tickets) and Customer
        query = """
        SELECT 
            [l].[LaborID], 
            [l].[GunID], 
            [l].[Employee], 
            [l].[WorkDescription], 
            [l].[AdditionalComments], 
            [l].[AdditionalParts], 
            [l].[Technician], 
            [l].[LaborType], 
            [l].[LaborPrice], 
            [l].[LaborStatus], 
            [l].[CompleteDate],

            [g].[GunID] AS [GunRefID], 
            [g].[CustomerID], 
            [g].[DropOffDate], 
            [g].[GunBrand], 
            [g].[GunModel], 
            [g].[SerialNum], 
            [g].[PurchaseLocation], 
            [g].[PurchaseDate], 
            [g].[PastInfo], 
            [g].[PickUpDate],

            [c].[CustomerID] AS [CustID], 
            [c].[FirstName], 
            [c].[LastName], 
            [c].[Email], 
            [c].[Mobile] AS [PhoneNumber], 
            [c].[Address], 
            [c].[Address2], 
            [c].[City], 
            [c].[State], 
            [c].[Zipcode]

        FROM ([Labor] AS [l]
        LEFT JOIN [Guns] AS [g] ON [l].[GunID] = [g].[GunID])
        LEFT JOIN [Customer] AS [c] ON [g].[CustomerID] = [c].[CustomerID];
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
    
def read_part_list_from_access(ticket):
    parts_list = []
    try:
        conn = pyodbc.connect(get_database_conn_str())
        cursor = conn.cursor()

        # Query to select all columns from Guns (Tickets) and Customer
        query = """
            SELECT PartName, PartQuantity, PartPrice
            FROM Parts
            WHERE LaborID = ?
        """

        cursor.execute(query, ticket['LaborID'])
        rows = cursor.fetchall()

        for row in rows:
            parts_list.append({
                "PartName": row.PartName,
                "PartQuantity": row.PartQuantity,
                "PartPrice": row.PartPrice
            })

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error retrieving parts for LaborID {ticket['LaborID']}: {e}")

    return parts_list

def create_customer_section(parent_frame, ticket):
    """Creates the customer details section (Read-Only)."""
    customer_frame = tk.Frame(parent_frame, padx=10, pady=10)
    customer_frame.pack(fill="x", padx=5, pady=5)

    tk.Label(customer_frame, text="Customer Details", font=("Arial", 12, "bold")).pack(anchor="w")

    customer_fields = {
        "First Name": ticket["FirstName"],
        "Last Name": ticket["LastName"],
        "Phone Number": ticket["PhoneNumber"],
        "Email": ticket["Email"],
    }

    for label, value in customer_fields.items():
        row_frame = tk.Frame(customer_frame)
        row_frame.pack(fill="x", padx=5, pady=2)
        tk.Label(row_frame, text=label, width=15, anchor="w").pack(side="left")
        tk.Label(row_frame, text=str(value), width=30, bg="lightgray", relief="ridge").pack(side="left")

    return customer_frame

def create_gun_section(parent_frame, ticket):
    """Creates the gun information section with editable fields, including multi-line inputs."""
    gun_frame = tk.Frame(parent_frame, padx=10, pady=10)
    gun_frame.pack(fill="x", padx=5, pady=5)

    tk.Label(gun_frame, text="Gun Information", font=("Arial", 12, "bold")).pack(anchor="w")

    # Gun Info Fields (Editable)
    gun_fields = {
        "Gun Brand": ticket["GunBrand"],
        "Gun Model": ticket["GunModel"],
        "Employee": ticket["Employee"],
        "Purchase Location": ticket["PurchaseLocation"],
        "Purchase Date": ticket["PurchaseDate"],
    }

    entry_widgets = {}

    for label, value in gun_fields.items():
        row_frame = tk.Frame(gun_frame)
        row_frame.pack(fill="x", padx=5, pady=2)
        tk.Label(row_frame, text=label, width=15, anchor="w").pack(side="left")
        entry = tk.Entry(row_frame, width=30)
        entry.insert(0, str(value))
        entry.pack(side="left")
        entry_widgets[label] = entry

    # Multi-line fields for long text inputs
    multi_line_fields = {
        "Past Info": (2, ticket["PastInfo"]),
        "Work Description": (4, ticket["WorkDescription"]),
        "Additional Parts": (2, ticket["AdditionalParts"]),
        "Additional Comments": (2, ticket["AdditionalComments"]),
    }

    for label, (height, value) in multi_line_fields.items():
        tk.Label(gun_frame, text=label).pack(anchor="w", padx=5, pady=2)
        text_widget = tk.Text(gun_frame, width=50, height=height)
        text_widget.insert("1.0", str(value))
        text_widget.pack(padx=5, pady=3)
        entry_widgets[label] = text_widget

    return gun_frame, entry_widgets

def create_labor_section(parent_frame, ticket):
    """Creates the labor section with technician entry and labor pricing, keeping labels and fields inline."""
    labor_frame = tk.Frame(parent_frame, padx=10, pady=10)
    labor_frame.pack(fill="x", padx=5, pady=5)

    tk.Label(labor_frame, text="Labor Details", font=("Arial", 12, "bold")).pack(anchor="w")

    # Technician Entry (Single Row)
    row_frame1 = tk.Frame(labor_frame)
    row_frame1.pack(fill="x", padx=5, pady=3)
    tk.Label(row_frame1, text="Technician", width=12, anchor="w").pack(side="left")
    technician_entry = tk.Entry(row_frame1, width=30)
    technician_entry.pack(side="left")

    if ticket['Technician'] != None:
        technician_entry.insert(ticket['Technician'])

    # Labor Type Dropdown (Single Row)
    row_frame2 = tk.Frame(labor_frame)
    row_frame2.pack(fill="x", padx=5, pady=3)
    tk.Label(row_frame2, text="Labor Type", width=12, anchor="w").pack(side="left")

    labor_selection = ttk.Combobox(row_frame2, values=list(labor_prices.keys()), state="readonly", width=28)
    if ticket['LaborPrice'] == None:
        labor_selection.set("Did not specify")
    else:
        labor_selection.set(ticket['LaborPrice'])
    labor_selection.pack(side="left")

    # Labor Price Entry (Single Row)
    row_frame3 = tk.Frame(labor_frame)
    row_frame3.pack(fill="x", padx=5, pady=3)
    tk.Label(row_frame3, text="Labor Price $", width=12, anchor="w").pack(side="left")
    price_entry = tk.Entry(row_frame3, width=10)
    price_entry.pack(side="left")

    if ticket['LaborPrice'] != None:
        technician_entry.insert(ticket['LaborPrice'])

    return labor_frame, technician_entry, labor_selection, price_entry

def populate_parts_tree(tree, parts):
    # Clear any existing rows
    for item in tree.get_children():
        tree.delete(item)

    # Add new parts from the list
    for part in parts:
        tree.insert('', 'end', values=(
            part["PartName"],
            part["PartQuantity"],
            f"${part['PartPrice']:.2f}"
        ))

def create_parts_section(parent_frame, price_entry, parts_list, ticket):
    """Creates the parts section with entry fields and a Treeview list."""
    parts_frame = tk.Frame(parent_frame, padx=10, pady=10)
    parts_frame.pack(fill="x", padx=5, pady=5)

    tk.Label(parts_frame, text="Parts Used", font=("Arial", 12, "bold")).pack(anchor="w")

    # Entry fields for adding parts
    entry_frame = tk.Frame(parts_frame)
    entry_frame.pack(fill="x", padx=5, pady=3)

    part_name_entry = tk.Entry(entry_frame, width=15)
    part_qty_entry = tk.Entry(entry_frame, width=5)
    part_price_entry = tk.Entry(entry_frame, width=10)

    tk.Label(entry_frame, text="Item").pack(side="left", padx=5)
    part_name_entry.pack(side="left", padx=5)

    tk.Label(entry_frame, text="Qty").pack(side="left", padx=5)
    part_qty_entry.pack(side="left", padx=5)

    tk.Label(entry_frame, text="Price").pack(side="left", padx=5)
    part_price_entry.pack(side="left", padx=5)

    # Ensure we pass all required parameters when calling `add_part_to_tree`
    tk.Button(entry_frame, text="Add", command=lambda: add_part_to_tree(
        part_name_entry, part_qty_entry, part_price_entry, parts_tree, price_entry
    )).pack(side="left", padx=5)

    # Treeview with scrollbar
    tree_frame = tk.Frame(parts_frame)
    tree_frame.pack(fill="x", padx=5, pady=5)

    tree_scroll = tk.Scrollbar(tree_frame, orient="vertical")
    parts_tree = ttk.Treeview(tree_frame, columns=("Name", "Quantity", "Price"), show="headings", height=5, yscrollcommand=tree_scroll.set)

    parts_tree.heading("Name", text="Item Name")
    parts_tree.heading("Quantity", text="Qty")
    parts_tree.heading("Price", text="Price ($)")

    parts_tree.column("Name", width=150)
    parts_tree.column("Quantity", width=50, anchor="center")
    parts_tree.column("Price", width=80, anchor="center")

    parts_tree.pack(side="left", fill="x", expand=True)
    tree_scroll.pack(side="right", fill="y")
    tree_scroll.config(command=parts_tree.yview)

    populate_parts_tree(parts_tree, parts_list)

    # Delete button for removing selected parts
    tk.Button(parts_frame, text="Delete Selected", command=lambda: delete_part_from_tree(
        parts_tree, price_entry,
    )).pack(pady=5)

    return parts_frame, parts_tree

def create_total_section(parent_frame):
    """Creates the total section with subtotal, tax, and final total, aligning tax label and entry inline."""
    total_frame = tk.Frame(parent_frame, padx=10, pady=10)
    total_frame.pack(fill="x", padx=5, pady=5)

    # Subtotal Label
    subtotal_label = tk.Label(total_frame, text="Subtotal: $0.00", font=("Arial", 10, "bold"))
    subtotal_label.pack(anchor="w")

    # Tax Label & Entry
    tax_row = tk.Frame(total_frame)
    tax_row.pack(fill="x", padx=5, pady=3)
    tk.Label(tax_row, text="Tax (%)", width=12, anchor="w").pack(side="left")
    tax_entry = tk.Entry(tax_row, width=10)
    tax_entry.insert(0, "8.75")  # Default tax value
    tax_entry.pack(side="left")

    # Total Label
    total_label = tk.Label(total_frame, text="Total: $0.00", font=("Arial", 12, "bold"))
    total_label.pack(anchor="w")

    return total_frame, subtotal_label, tax_entry, total_label

def create_date_section(parent_frame, ticket):
    """Creates the date section with drop-off, finish, and pick-up dates, as well as a status dropdown."""
    date_frame = tk.Frame(parent_frame, padx=10, pady=10)
    date_frame.pack(fill="x", padx=5, pady=5)

    tk.Label(date_frame, text="Date & Status", font=("Arial", 12, "bold")).pack(anchor="w")

    # Drop-Off Date
    dropoff_row = tk.Frame(date_frame)
    dropoff_row.pack(fill="x", padx=5, pady=2)
    tk.Label(dropoff_row, text="Drop-Off Date", width=15, anchor="w").pack(side="left")
    dropoff_entry = tk.Entry(dropoff_row, width=30)
    raw_date = ticket.get("DropOffDate")
    if raw_date:
        try:
            # If it's already a datetime object
            formatted_date = raw_date.strftime("%m/%d/%Y")
        except AttributeError:
            # If it's a string, parse and then format
            parsed = datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S")
            formatted_date = parsed.strftime("%m/%d/%Y")
    else:
        formatted_date = ""
    
    dropoff_entry.insert(0, formatted_date)  # Use ticket value or empty string
    dropoff_entry.pack(side="left")

    # Finish Date
    finish_row = tk.Frame(date_frame)
    finish_row.pack(fill="x", padx=5, pady=2)
    tk.Label(finish_row, text="Finish Date", width=15, anchor="w").pack(side="left")
    finish_entry = tk.Entry(finish_row, width=30)
    finish_entry.pack(side="left")

    # Pick-Up Date
    pickup_row = tk.Frame(date_frame)
    pickup_row.pack(fill="x", padx=5, pady=2)
    tk.Label(pickup_row, text="Pick-Up Date", width=15, anchor="w").pack(side="left")
    pickup_entry = tk.Entry(pickup_row, width=30)
    pickup_entry.pack(side="left")

    # Status Dropdown (Default to "Pending")
    status_row = tk.Frame(date_frame)
    status_row.pack(fill="x", padx=5, pady=2)
    tk.Label(status_row, text="Current Status", width=15, anchor="w").pack(side="left")

    status_options = ["Pending", "Awaiting Parts", "Work in Progress", "Awaiting Pick Up", "Completed", "Canceled"]
    
    status_var = ticket["LaborStatus"]
    if status_var is None:
        status_var = "Pending" # Default to "Pending" if not provided
    status_dropdown = ttk.Combobox(status_row, values=status_options, state="readonly", width=27)
    status_dropdown.set(status_var)
    status_dropdown.pack(side="left")

    return date_frame, dropoff_entry, finish_entry, pickup_entry, status_dropdown

def create_buttons(parent_frame, ticket, gun_entries, technician_entry, labor_selection, price_entry, parts_tree, subtotal_label, tax_entry, total_label):
    """Creates the print and save buttons and ensures they are positioned correctly in the right column."""
    
    tk.Button(parent_frame, text="Print Ticket", width=15).pack(side="left", padx=5)
    tk.Button(parent_frame, text="Print Invoice", width=15).pack(side="left", padx=5)

    save_button = tk.Button(parent_frame, text="Save Changes", width=20, height=2, font=("Arial", 10, "bold"),
                            command=lambda: save_changes(ticket, gun_entries, technician_entry, labor_selection, price_entry, parts_tree, subtotal_label, tax_entry, total_label))
    save_button.pack(side="right", padx=5)

def edit_ticket_window(ticket):
    """Main function that opens the ticket editing window and assembles all sections with a two-column layout."""
    
    parts_list = read_part_list_from_access(ticket)

    edit_window = tk.Toplevel()
    edit_window.title(f"Edit Ticket ID {ticket['LaborID']}")
    edit_window.geometry("1000x800")  
    edit_window.resizable(False, False)

    # Create main frames to separate left and right columns
    left_column = tk.Frame(edit_window)
    right_column = tk.Frame(edit_window)

    left_column.pack(side="left", fill="both", expand=True, padx=10, pady=5)
    right_column.pack(side="right", fill="y", padx=10, pady=5)

    # === LEFT COLUMN (Customer & Gun Info) ===
    create_customer_section(left_column, ticket)  # Customer Details (Read-Only)
    gun_frame, gun_entries = create_gun_section(left_column, ticket)  # Gun Data (Editable)

    # === RIGHT COLUMN (Labor, Parts, Totals, Dates, Buttons) ===
    labor_frame, technician_entry, labor_selection, price_entry = create_labor_section(right_column, ticket)
    parts_frame, parts_tree = create_parts_section(right_column, price_entry, parts_list, ticket)
    
    # Totals Section
    total_frame, subtotal_label, tax_entry, total_label = create_total_section(right_column)

    # Date Section
    date_frame, dropoff_entry, finish_entry, pickup_entry, status_dropdown = create_date_section(right_column, ticket)

    # Buttons
    button_frame = tk.Frame(right_column, padx=10, pady=10)
    button_frame.pack(fill="x", padx=5, pady=5)

    create_buttons(button_frame, ticket, gun_entries, technician_entry, labor_selection, price_entry, parts_tree, subtotal_label, tax_entry, total_label)

    edit_window.mainloop()

def refresh_treeview(treeview):
    """Refreshes the ticket list in the Treeview by fetching updated data from the database."""
    
    # Fetch updated customer data
    raw_customers = read_customer_data_from_access()  # Get latest data from database
    customers = format_customer_data(raw_customers)  # Format data correctly

    # Clear current Treeview entries
    treeview.delete(*treeview.get_children())

    # Insert updated data
    for customer in customers:
        treeview.insert("", "end", values=(customer["CustomerID"], customer["FullName"]))