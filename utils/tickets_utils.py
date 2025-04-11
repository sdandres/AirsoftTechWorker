import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import asksaveasfilename
import pyodbc
from datetime import datetime, date
from decimal import Decimal
import webbrowser  # Built-in module to open a file in the default browser
from utils.path_utils import get_database_conn_str

# ---------- Global State ----------
current_ticket = None
current_parts = []

ticket_ui_elements = {
    "entries": {},
    "textboxes": {},
    "dropdowns": {},
    "labels": {},
    "tree": None
}

# ---------- UI Initialization ----------
def open_ticket_editor(ticket_data, refresh_callback=None):
    global current_ticket, current_parts
    current_ticket = ticket_data
    current_parts = read_part_list(ticket_data["LaborID"])

    window = tk.Toplevel()
    window.title(f"Edit Ticket #{ticket_data['LaborID']}")
    window.geometry("1000x810")
    window.resizable(False, False)

    canvas_obj = tk.Canvas(window)
    canvas_obj.pack(fill="both", expand=True)

    frame = tk.Frame(canvas_obj, padx=20, pady=20)
    frame.pack()

    build_sections(frame)
    populate_fields(ticket_data)
    bind_total_events()

    def on_close():
        if refresh_callback:
            refresh_callback()
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_close)
    window.bind("<Control-s>", lambda e: save_changes())
    window.mainloop()

# ---------- Section Builders ----------
def build_label_textbox(frame, label, height=3):
    tk.Label(frame, text=label).pack(anchor="w")
    textbox = tk.Text(frame, width=60, height=height)
    textbox.pack(pady=2)
    ticket_ui_elements["textboxes"][label] = textbox

def build_dropdown(frame, label, options):
    tk.Label(frame, text=label).pack(anchor="w")
    var = tk.StringVar()
    dropdown = ttk.Combobox(frame, textvariable=var, values=options, state="readonly", width=48)
    dropdown.pack(pady=2)
    ticket_ui_elements["dropdowns"][label] = dropdown

def build_label_entry(frame, label):
    row = tk.Frame(frame)
    row.pack(anchor="w", pady=2, fill="x")
    tk.Label(row, text=label, width=18, anchor="w").pack(side="left")
    entry = tk.Entry(row, width=30)
    if label in ["First Name", "Last Name", "Mobile", "Email"]:
        entry.insert(0, "")
        entry.config(state="readonly", disabledbackground="#f0f0f0")
    entry.pack(side="left")
    ticket_ui_elements["entries"][label] = entry

def bind_total_events():
    ticket_ui_elements["entries"]["Labor Price"].bind("<KeyRelease>", lambda e: update_totals())
    ticket_ui_elements["entries"]["Labor Price"].bind("<FocusOut>", lambda e: update_totals())
    ticket_ui_elements["entries"]["Tax"].bind("<KeyRelease>", lambda e: update_totals())
    ticket_ui_elements["entries"]["Tax"].bind("<FocusOut>", lambda e: update_totals())
    ticket_ui_elements["parts_name"].bind("<KeyRelease>", lambda e: update_totals())
    ticket_ui_elements["parts_qty"].bind("<KeyRelease>", lambda e: update_totals())
    ticket_ui_elements["parts_price"].bind("<KeyRelease>", lambda e: update_totals())
    ticket_ui_elements["dropdowns"]["Labor Type"].bind("<<ComboboxSelected>>", lambda e: update_labor_price())
    for field in ["Purchase Date", "DropOff Date", "Finish Date", "PickUp Date"]:
        ticket_ui_elements["entries"][field].bind("<KeyRelease>", lambda e, entry=ticket_ui_elements["entries"][field]: format_and_validate_date(e, entry))

def build_sections(frame):
    # Use a 2-column layout
    left_col = tk.Frame(frame)
    left_col.grid(row=0, column=0, sticky="n")

    right_col = tk.Frame(frame)
    right_col.grid(row=0, column=1, padx=(40, 0), sticky="n")

    # --- LEFT COLUMN ---
    # Customer Info
    customer_frame = tk.LabelFrame(left_col, text="Customer Info")
    customer_frame.pack(padx=10, pady=5, anchor="nw")
    build_label_entry(customer_frame, "First Name")
    build_label_entry(customer_frame, "Last Name")
    build_label_entry(customer_frame, "Mobile")
    build_label_entry(customer_frame, "Email")

    # Received by
    received_frame = tk.LabelFrame(left_col, text="Received by")
    received_frame.pack(padx=10, pady=5, anchor="nw")
    build_label_entry(received_frame, "Employee")

    # Purchase Info
    purchase_frame = tk.LabelFrame(left_col, text="Purchase Info")
    purchase_frame.pack(padx=10, pady=5, anchor="nw")
    build_label_entry(purchase_frame, "Purchase Location")
    build_label_entry(purchase_frame, "Purchase Date")

    # Gun & Notes Info
    gun_frame = tk.LabelFrame(left_col, text="Gun & Notes")
    gun_frame.pack(padx=10, pady=5, anchor="nw")
    build_label_entry(gun_frame, "Gun Brand")
    build_label_entry(gun_frame, "Gun Model")
    build_label_entry(gun_frame, "Serial Number")
    build_label_textbox(gun_frame, "Past Info", height=3)
    build_label_textbox(gun_frame, "Work Description", height=4)
    build_label_textbox(gun_frame, "Additional Parts", height=3)
    build_label_textbox(gun_frame, "Additional Comments", height=3)

    # --- RIGHT COLUMN ---
    # Labor Info
    labor_frame = tk.LabelFrame(right_col, text="Labor Info")
    labor_frame.pack(padx=10, pady=5, anchor="nw", fill="x")

    build_label_entry(labor_frame, "Technician")

    labor_row = tk.Frame(labor_frame)
    labor_row.pack(fill="x")
    build_dropdown(labor_row, "Labor Type", ["Did not specify", "External", "Internal", "External & Internal", "Advanced", "Connector Swap", "Custom"])
    build_label_entry(labor_row, "Labor Price")

    # Parts Table
    parts_frame = tk.LabelFrame(right_col, text="Parts List")
    parts_frame.pack(padx=10, pady=5, anchor="nw")

    entry_row = tk.Frame(parts_frame)
    entry_row.pack(anchor="w", pady=5)

    tk.Label(entry_row, text="Part Name").grid(row=0, column=0, padx=5)
    part_name_entry = tk.Entry(entry_row, width=20)
    part_name_entry.grid(row=1, column=0, padx=5)
    ticket_ui_elements["parts_name"] = part_name_entry

    tk.Label(entry_row, text="Quantity").grid(row=0, column=1, padx=5)
    part_qty_entry = tk.Entry(entry_row, width=10)
    part_qty_entry.grid(row=1, column=1, padx=5)
    ticket_ui_elements["parts_qty"] = part_qty_entry

    tk.Label(entry_row, text="Price ($)").grid(row=0, column=2, padx=5)
    part_price_entry = tk.Entry(entry_row, width=10)
    part_price_entry.grid(row=1, column=2, padx=5)
    ticket_ui_elements["parts_price"] = part_price_entry

    def add_part():
        name = part_name_entry.get()
        qty = part_qty_entry.get()
        price = part_price_entry.get()
        if name and qty and price:
            try:
                qty = int(qty)
                price = Decimal(price)
                total_price = qty * price
                ticket_ui_elements["tree"].insert("", "end", values=(name, qty, f"${total_price:.2f}"))
                current_parts.append({"PartName": name, "PartQuantity": qty, "PartPrice": price})
                part_name_entry.delete(0, tk.END)
                part_qty_entry.delete(0, tk.END)
                part_price_entry.delete(0, tk.END)
                update_totals()
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid quantity and price.")
        else:
            messagebox.showerror("Missing Data", "Please fill in all part fields.")

    tk.Button(parts_frame, text="Add Part", command=add_part).pack(pady=5)

    build_parts_table(parts_frame)
    tk.Button(parts_frame, text="Delete Selected Part", command=delete_selected_part).pack(pady=5)

    # Totals Section
    totals_frame = tk.LabelFrame(right_col, text="Totals")
    totals_frame.pack(padx=10, pady=5, anchor="nw")

    ticket_ui_elements["labels"]["subtotal"] = tk.Label(totals_frame, text="Subtotal: $0.00", font=("Arial", 10))
    ticket_ui_elements["labels"]["subtotal"].pack(anchor="w")

    tk.Label(totals_frame, text="Tax (%)").pack(anchor="w")
    tax_entry = tk.Entry(totals_frame, width=10)
    tax_entry.insert(0, "8.75")
    tax_entry.pack(anchor="w")
    ticket_ui_elements["entries"]["Tax"] = tax_entry

    ticket_ui_elements["labels"]["total"] = tk.Label(totals_frame, text="Total: $0.00", font=("Arial", 10, "bold"))
    ticket_ui_elements["labels"]["total"].pack(anchor="w", pady=(5, 0))

    # Dates & Status Section
    dates_frame = tk.LabelFrame(right_col, text="Current Status & Dates")
    dates_frame.pack(padx=10, pady=5, anchor="nw")
    build_dropdown(dates_frame, "Labor Status", ["Pending", "In Progress", "Waiting on Parts", "Warranty", "Completed", "Canceled"])
    build_label_entry(dates_frame, "DropOff Date")
    build_label_entry(dates_frame, "Finish Date")
    build_label_entry(dates_frame, "PickUp Date")

    # Save Buttons Section - Save Changes and Save as HTML for PDF
    save_frame = tk.Frame(right_col)
    save_frame.pack(padx=10, pady=10, anchor="w")
    tk.Button(save_frame, text="Save Changes", command=save_changes).pack(side="left", padx=5)
    add_save_pdf_button(save_frame)

def build_parts_table(frame):
    tree = ttk.Treeview(frame, columns=("Name", "Quantity", "Price"), show="headings", height=5)
    tree.heading("Name", text="Item")
    tree.heading("Quantity", text="Qty")
    tree.heading("Price", text="Price ($)")
    tree.column("Name", width=200)
    tree.column("Quantity", width=80, anchor="center")
    tree.column("Price", width=100, anchor="center")
    tree.pack(pady=10)
    ticket_ui_elements["tree"] = tree
    populate_parts_table()

# ---------- Date Field Formatter ----------
def format_and_validate_date(event, date_entry):
    if event.keysym == "BackSpace":
        return

    digits = [c for c in date_entry.get() if c.isdigit()]
    new_text = ""

    # Month (MM)
    if len(digits) >= 1:
        if int(digits[0]) > 1:
            digits.insert(0, '0')
    if len(digits) >= 2:
        month = int(''.join(digits[0:2]))
        month = min(max(month, 1), 12)
        new_text += f"{month:02d}/"
    elif len(digits) >= 1:
        new_text += digits[0]

    # Day (DD)
    if len(digits) >= 3:
        if int(digits[2]) > 3:
            digits.insert(2, '0')
    if len(digits) >= 4:
        day = int(''.join(digits[2:4]))
        day = min(max(day, 1), 31)
        new_text += f"{day:02d}/"
    elif len(digits) >= 3:
        new_text += digits[2]

    # Year (YYYY starting with '2')
    if len(digits) >= 5:
        if digits[4] != '2':
            digits[4] = '2'
    if len(digits) >= 5:
        year_digits = digits[4:8]
        new_text += ''.join(year_digits)

    formatted_date = new_text[:10]
    date_entry.delete(0, tk.END)
    date_entry.insert(0, formatted_date)

    # Extra date logic for Finish or PickUp dates
    field_map = {v: k for k, v in ticket_ui_elements["entries"].items()}
    label = field_map.get(date_entry, "")
    if label in ["Finish Date", "PickUp Date"]:
        drop_entry = ticket_ui_elements["entries"].get("DropOff Date")
        finish_text = ticket_ui_elements["entries"].get("Finish Date")
        pickup_text = ticket_ui_elements["entries"].get("PickUp Date")
        try:
            drop_date = datetime.strptime(drop_entry.get(), "%m/%d/%Y")
            if label == "Finish Date":
                finish_date = datetime.strptime(finish_text.get(), "%m/%d/%Y")
                if finish_date < drop_date:
                    messagebox.showerror("Invalid Date", "Finish Date cannot be before DropOff Date.")
            elif label == "PickUp Date":
                pickup_date = datetime.strptime(pickup_text.get(), "%m/%d/%Y")
                if finish_text:
                    finish_date = datetime.strptime(finish_text.get(), "%m/%d/%Y")
                    if pickup_date < finish_date:
                        messagebox.showerror("Invalid Date", "PickUp Date cannot be before Finish Date.")
                        date_entry.delete(0, tk.END)
                        return
                if pickup_date < drop_date:
                    messagebox.showerror("Invalid Date", "PickUp Date cannot be before DropOff Date.")
                    date_entry.delete(0, tk.END)
        except:
            pass

def simple_date_format(value):
    if isinstance(value, (datetime, date)):
        return value.strftime("%m/%d/%Y")
    elif isinstance(value, str) and len(value) >= 10:
        return value[:10]
    else:
        return str(value)

# ---------- Field Populators ----------
def populate_fields(ticket):
    field_map = {
        "First Name": "FirstName",
        "Last Name": "LastName",
        "Mobile": "Mobile",
        "Email": "Email",
        "Employee": "Employee",
        "Technician": "Technician",
        "Labor Type": "LaborType",
        "Labor Price": "LaborPrice",
        "Labor Status": "LaborStatus",
        "DropOff Date": "DropOffDate",
        "Finish Date": "CompleteDate",
        "PickUp Date": "PickUpDate",
        "Gun Brand": "GunBrand",
        "Gun Model": "GunModel",
        "Serial Number": "SerialNum",
        "Purchase Location": "PurchaseLocation",
        "Purchase Date": "PurchaseDate",
    }

    for ui_key, entry in ticket_ui_elements["entries"].items():
        data_key = field_map.get(ui_key, ui_key.replace(" ", ""))
        if data_key in ticket and ticket[data_key] is not None:
            value = ticket[data_key]
            if data_key.endswith("Date"):
                value = simple_date_format(value)
            was_readonly = str(entry.cget("state")) == "readonly"
            if was_readonly:
                entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, str(value))
            if was_readonly:
                entry.config(state="readonly")

    for ui_key, textbox in ticket_ui_elements["textboxes"].items():
        data_key = field_map.get(ui_key, ui_key.replace(" ", ""))
        if data_key in ticket and ticket[data_key] is not None:
            textbox.delete("1.0", tk.END)
            textbox.insert("1.0", str(ticket[data_key]))

    for ui_key, dropdown in ticket_ui_elements["dropdowns"].items():
        data_key = field_map.get(ui_key, ui_key.replace(" ", ""))
        value = ticket.get(data_key)
        if data_key == "LaborType":
            dropdown.set(str(value) if value else "Did not specify")
        elif data_key == "LaborStatus":
            dropdown.set(str(value) if value else "Pending")
        elif value is not None:
            dropdown.set(str(value))

# ---------- Labor Handling ----------
def update_labor_price():
    mapping = {
        "Did not specify": "0.00",
        "External": "30.00",
        "Internal": "60.00",
        "External & Internal": "75.00",
        "Advanced": "80.00",
        "Connector": "19.00"
    }
    labor_type_value = ticket_ui_elements["dropdowns"]["Labor Type"].get()
    if labor_type_value in mapping:
        labor_price_entry = ticket_ui_elements["entries"]["Labor Price"]
        labor_price_entry.delete(0, tk.END)
        labor_price_entry.insert(0, mapping[labor_type_value])
    update_totals()

# ---------- Totals Calculation ----------
def update_totals():
    try:
        labor_price = Decimal(ticket_ui_elements["entries"]["Labor Price"].get() or 0)
        parts_total = sum(p["PartQuantity"] * p["PartPrice"] for p in current_parts)
        subtotal = labor_price + parts_total

        tax_rate = Decimal(ticket_ui_elements["entries"]["Tax"].get() or 0)
        tax_amount = subtotal * (tax_rate / 100)
        total = subtotal + tax_amount

        ticket_ui_elements["labels"]["subtotal"].config(text=f"Subtotal: ${subtotal:.2f}")
        ticket_ui_elements["labels"]["total"].config(text=f"Total: ${total:.2f}")
    except Exception as e:
        print("Error updating totals:", e)

def populate_parts_table():
    tree = ticket_ui_elements["tree"]
    for part in current_parts:
        tree.insert("", "end", values=(part["PartName"], part["PartQuantity"], f"${part['PartPrice']:.2f}"))

def delete_selected_part():
    tree = ticket_ui_elements["tree"]
    selected = tree.selection()
    if selected:
        for item in selected:
            values = tree.item(item, "values")
            name = values[0]
            qty = int(values[1])
            price = Decimal(values[2].replace("$", ""))
            tree.delete(item)
            for p in current_parts:
                if p["PartName"] == name and p["PartQuantity"] == qty and p["PartPrice"] == price:
                    current_parts.remove(p)
                    break
        update_totals()
    else:
        messagebox.showerror("No selection", "Please select a part to delete.")

# ---------- Data Handling ----------
def read_part_list(labor_id):
    try:
        conn = pyodbc.connect(get_database_conn_str())
        cursor = conn.cursor()
        query = "SELECT PartName, PartQuantity, PartPrice FROM Parts WHERE LaborID = ?"
        cursor.execute(query, labor_id)
        rows = cursor.fetchall()
        return [{"PartName": r[0], "PartQuantity": r[1], "PartPrice": r[2]} for r in rows]
    except Exception as e:
        print(f"Failed to load parts: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def read_ticket_data_from_access():
    try:
        conn = pyodbc.connect(get_database_conn_str())
        cursor = conn.cursor()
        query = '''
            SELECT Labor.LaborID, Labor.GunID, Labor.Employee, Labor.WorkDescription, Labor.AdditionalComments,
                   Labor.AdditionalParts, Labor.Technician, Labor.LaborType, Labor.LaborPrice, Labor.LaborStatus, Labor.CompleteDate,
                   Guns.GunID, Guns.CustomerID, Guns.DropOffDate, Guns.GunBrand, Guns.GunModel, Guns.SerialNum,
                   Guns.PurchaseLocation, Guns.PurchaseDate, Guns.PastInfo, Guns.PickUpDate,
                   Customer.CustomerID, Customer.FirstName, Customer.LastName, Customer.Email, Customer.Mobile
            FROM ((Labor
            LEFT JOIN Guns ON Labor.GunID = Guns.GunID)
            LEFT JOIN Customer ON Guns.CustomerID = Customer.CustomerID)
        '''
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        tickets = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return tickets
    except Exception as e:
        messagebox.showerror("Database Error", f"Error retrieving tickets: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def save_changes():
    try:
        conn = pyodbc.connect(get_database_conn_str())
        cursor = conn.cursor()
        labor_id = current_ticket["LaborID"]

        def parse_date(label):
            try:
                date_str = ticket_ui_elements["entries"][label].get()
                dt = datetime.strptime(date_str, "%m/%d/%Y")
                return dt.date()
            except:
                return None

        # --- Update Labor ---
        cursor.execute('''
            UPDATE Labor SET
                Employee = ?, WorkDescription = ?, AdditionalComments = ?,
                AdditionalParts = ?, Technician = ?, LaborType = ?,
                LaborPrice = ?, LaborStatus = ?, CompleteDate = ?
            WHERE LaborID = ?
        ''', (
            ticket_ui_elements["entries"]["Employee"].get(),
            ticket_ui_elements["textboxes"]["Work Description"].get("1.0", tk.END).strip(),
            ticket_ui_elements["textboxes"]["Additional Comments"].get("1.0", tk.END).strip(),
            ticket_ui_elements["textboxes"]["Additional Parts"].get("1.0", tk.END).strip(),
            ticket_ui_elements["entries"]["Technician"].get(),
            ticket_ui_elements["dropdowns"]["Labor Type"].get(),
            float(ticket_ui_elements["entries"]["Labor Price"].get() or 0),
            ticket_ui_elements["dropdowns"]["Labor Status"].get(),
            parse_date("Finish Date"),
            labor_id
        ))

        # --- Update Guns ---
        cursor.execute('''
            UPDATE Guns SET
                DropOffDate = ?, GunBrand = ?, GunModel = ?,
                PurchaseLocation = ?, PurchaseDate = ?, PastInfo = ?, PickUpDate = ?
            WHERE GunID = ?
        ''', (
            parse_date("DropOff Date"),
            ticket_ui_elements["entries"]["Gun Brand"].get(),
            ticket_ui_elements["entries"]["Gun Model"].get(),
            ticket_ui_elements["entries"]["Purchase Location"].get(),
            parse_date("Purchase Date"),
            ticket_ui_elements["textboxes"]["Past Info"].get("1.0", tk.END).strip(),
            parse_date("PickUp Date"),
            current_ticket["GunID"]
        ))

        # --- Update Customer ---
        cursor.execute('''
            UPDATE Customer SET
                FirstName = ?, LastName = ?, Email = ?, Mobile = ?
            WHERE CustomerID = ?
        ''', (
            ticket_ui_elements["entries"]["First Name"].get(),
            ticket_ui_elements["entries"]["Last Name"].get(),
            ticket_ui_elements["entries"]["Email"].get(),
            ticket_ui_elements["entries"]["Mobile"].get(),
            current_ticket["CustomerID"]
        ))

        # --- Clear & Reinsert Parts ---
        cursor.execute("DELETE FROM Parts WHERE LaborID = ?", labor_id)
        for part in current_parts:
            cursor.execute('''
                INSERT INTO Parts (LaborID, PartName, PartQuantity, PartPrice)
                VALUES (?, ?, ?, ?)
            ''', (labor_id, part["PartName"], part["PartQuantity"], part["PartPrice"]))

        conn.commit()
        messagebox.showinfo("Success", "Ticket and parts saved successfully.")
    except Exception as e:
        messagebox.showerror("Save Error", f"An error occurred while saving: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# ---------- Save as HTML for PDF Functionality (No External Libraries) ----------
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import asksaveasfilename
import pyodbc
from datetime import datetime, date
from decimal import Decimal
import webbrowser  # Built-in module to open a file in the default browser
from utils.path_utils import get_database_conn_str

# ---------- Global State ----------
current_ticket = None
current_parts = []

ticket_ui_elements = {
    "entries": {},
    "textboxes": {},
    "dropdowns": {},
    "labels": {},
    "tree": None
}

# ---------- UI Initialization ----------
def open_ticket_editor(ticket_data, refresh_callback=None):
    global current_ticket, current_parts
    current_ticket = ticket_data
    current_parts = read_part_list(ticket_data["LaborID"])

    window = tk.Toplevel()
    window.title(f"Edit Ticket #{ticket_data['LaborID']}")
    window.geometry("1000x810")
    window.resizable(False, False)

    canvas_obj = tk.Canvas(window)
    canvas_obj.pack(fill="both", expand=True)

    frame = tk.Frame(canvas_obj, padx=20, pady=20)
    frame.pack()

    build_sections(frame)
    populate_fields(ticket_data)
    bind_total_events()

    def on_close():
        if refresh_callback:
            refresh_callback()
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_close)
    window.bind("<Control-s>", lambda e: save_changes())
    window.mainloop()

# ---------- Section Builders ----------
def build_label_textbox(frame, label, height=3):
    tk.Label(frame, text=label).pack(anchor="w")
    textbox = tk.Text(frame, width=60, height=height)
    textbox.pack(pady=2)
    ticket_ui_elements["textboxes"][label] = textbox

def build_dropdown(frame, label, options):
    tk.Label(frame, text=label).pack(anchor="w")
    var = tk.StringVar()
    dropdown = ttk.Combobox(frame, textvariable=var, values=options, state="readonly", width=48)
    dropdown.pack(pady=2)
    ticket_ui_elements["dropdowns"][label] = dropdown

def build_label_entry(frame, label):
    row = tk.Frame(frame)
    row.pack(anchor="w", pady=2, fill="x")
    tk.Label(row, text=label, width=18, anchor="w").pack(side="left")
    entry = tk.Entry(row, width=30)
    if label in ["First Name", "Last Name", "Mobile", "Email"]:
        entry.insert(0, "")
        entry.config(state="readonly", disabledbackground="#f0f0f0")
    entry.pack(side="left")
    ticket_ui_elements["entries"][label] = entry

def bind_total_events():
    ticket_ui_elements["entries"]["Labor Price"].bind("<KeyRelease>", lambda e: update_totals())
    ticket_ui_elements["entries"]["Labor Price"].bind("<FocusOut>", lambda e: update_totals())
    ticket_ui_elements["entries"]["Tax"].bind("<KeyRelease>", lambda e: update_totals())
    ticket_ui_elements["entries"]["Tax"].bind("<FocusOut>", lambda e: update_totals())
    ticket_ui_elements["parts_name"].bind("<KeyRelease>", lambda e: update_totals())
    ticket_ui_elements["parts_qty"].bind("<KeyRelease>", lambda e: update_totals())
    ticket_ui_elements["parts_price"].bind("<KeyRelease>", lambda e: update_totals())
    ticket_ui_elements["dropdowns"]["Labor Type"].bind("<<ComboboxSelected>>", lambda e: update_labor_price())
    for field in ["Purchase Date", "DropOff Date", "Finish Date", "PickUp Date"]:
        ticket_ui_elements["entries"][field].bind("<KeyRelease>", lambda e, entry=ticket_ui_elements["entries"][field]: format_and_validate_date(e, entry))

def build_sections(frame):
    # Use a 2-column layout
    left_col = tk.Frame(frame)
    left_col.grid(row=0, column=0, sticky="n")

    right_col = tk.Frame(frame)
    right_col.grid(row=0, column=1, padx=(40, 0), sticky="n")

    # --- LEFT COLUMN ---
    # Customer Info
    customer_frame = tk.LabelFrame(left_col, text="Customer Info")
    customer_frame.pack(padx=10, pady=5, anchor="nw")
    build_label_entry(customer_frame, "First Name")
    build_label_entry(customer_frame, "Last Name")
    build_label_entry(customer_frame, "Mobile")
    build_label_entry(customer_frame, "Email")

    # Received by
    received_frame = tk.LabelFrame(left_col, text="Received by")
    received_frame.pack(padx=10, pady=5, anchor="nw")
    build_label_entry(received_frame, "Employee")

    # Purchase Info
    purchase_frame = tk.LabelFrame(left_col, text="Purchase Info")
    purchase_frame.pack(padx=10, pady=5, anchor="nw")
    build_label_entry(purchase_frame, "Purchase Location")
    build_label_entry(purchase_frame, "Purchase Date")

    # Gun & Notes Info
    gun_frame = tk.LabelFrame(left_col, text="Gun & Notes")
    gun_frame.pack(padx=10, pady=5, anchor="nw")
    build_label_entry(gun_frame, "Gun Brand")
    build_label_entry(gun_frame, "Gun Model")
    build_label_entry(gun_frame, "Serial Number")
    build_label_textbox(gun_frame, "Past Info", height=3)
    build_label_textbox(gun_frame, "Work Description", height=4)
    build_label_textbox(gun_frame, "Additional Parts", height=3)
    build_label_textbox(gun_frame, "Additional Comments", height=3)

    # --- RIGHT COLUMN ---
    # Labor Info
    labor_frame = tk.LabelFrame(right_col, text="Labor Info")
    labor_frame.pack(padx=10, pady=5, anchor="nw", fill="x")

    build_label_entry(labor_frame, "Technician")

    labor_row = tk.Frame(labor_frame)
    labor_row.pack(fill="x")
    build_dropdown(labor_row, "Labor Type", ["Did not specify", "External", "Internal", "External & Internal", "Advanced", "Connector Swap", "Custom"])
    build_label_entry(labor_row, "Labor Price")

    # Parts Table
    parts_frame = tk.LabelFrame(right_col, text="Parts List")
    parts_frame.pack(padx=10, pady=5, anchor="nw")

    entry_row = tk.Frame(parts_frame)
    entry_row.pack(anchor="w", pady=5)

    tk.Label(entry_row, text="Part Name").grid(row=0, column=0, padx=5)
    part_name_entry = tk.Entry(entry_row, width=20)
    part_name_entry.grid(row=1, column=0, padx=5)
    ticket_ui_elements["parts_name"] = part_name_entry

    tk.Label(entry_row, text="Quantity").grid(row=0, column=1, padx=5)
    part_qty_entry = tk.Entry(entry_row, width=10)
    part_qty_entry.grid(row=1, column=1, padx=5)
    ticket_ui_elements["parts_qty"] = part_qty_entry

    tk.Label(entry_row, text="Price ($)").grid(row=0, column=2, padx=5)
    part_price_entry = tk.Entry(entry_row, width=10)
    part_price_entry.grid(row=1, column=2, padx=5)
    ticket_ui_elements["parts_price"] = part_price_entry

    def add_part():
        name = part_name_entry.get()
        qty = part_qty_entry.get()
        price = part_price_entry.get()
        if name and qty and price:
            try:
                qty = int(qty)
                price = Decimal(price)
                total_price = qty * price
                ticket_ui_elements["tree"].insert("", "end", values=(name, qty, f"${total_price:.2f}"))
                current_parts.append({"PartName": name, "PartQuantity": qty, "PartPrice": price})
                part_name_entry.delete(0, tk.END)
                part_qty_entry.delete(0, tk.END)
                part_price_entry.delete(0, tk.END)
                update_totals()
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid quantity and price.")
        else:
            messagebox.showerror("Missing Data", "Please fill in all part fields.")

    tk.Button(parts_frame, text="Add Part", command=add_part).pack(pady=5)

    build_parts_table(parts_frame)
    tk.Button(parts_frame, text="Delete Selected Part", command=delete_selected_part).pack(pady=5)

    # Totals Section
    totals_frame = tk.LabelFrame(right_col, text="Totals")
    totals_frame.pack(padx=10, pady=5, anchor="nw")

    ticket_ui_elements["labels"]["subtotal"] = tk.Label(totals_frame, text="Subtotal: $0.00", font=("Arial", 10))
    ticket_ui_elements["labels"]["subtotal"].pack(anchor="w")

    tk.Label(totals_frame, text="Tax (%)").pack(anchor="w")
    tax_entry = tk.Entry(totals_frame, width=10)
    tax_entry.insert(0, "8.75")
    tax_entry.pack(anchor="w")
    ticket_ui_elements["entries"]["Tax"] = tax_entry

    ticket_ui_elements["labels"]["total"] = tk.Label(totals_frame, text="Total: $0.00", font=("Arial", 10, "bold"))
    ticket_ui_elements["labels"]["total"].pack(anchor="w", pady=(5, 0))

    # Dates & Status Section
    dates_frame = tk.LabelFrame(right_col, text="Current Status & Dates")
    dates_frame.pack(padx=10, pady=5, anchor="nw")
    build_dropdown(dates_frame, "Labor Status", ["Pending", "In Progress", "Waiting on Parts", "Warranty", "Completed", "Canceled"])
    build_label_entry(dates_frame, "DropOff Date")
    build_label_entry(dates_frame, "Finish Date")
    build_label_entry(dates_frame, "PickUp Date")

    # Save Buttons Section - Save Changes and Save as HTML for PDF
    save_frame = tk.Frame(right_col)
    save_frame.pack(padx=10, pady=10, anchor="w")
    tk.Button(save_frame, text="Save Changes", command=save_changes).pack(side="left", padx=5)
    add_save_pdf_button(save_frame)

def build_parts_table(frame):
    tree = ttk.Treeview(frame, columns=("Name", "Quantity", "Price"), show="headings", height=5)
    tree.heading("Name", text="Item")
    tree.heading("Quantity", text="Qty")
    tree.heading("Price", text="Price ($)")
    tree.column("Name", width=200)
    tree.column("Quantity", width=80, anchor="center")
    tree.column("Price", width=100, anchor="center")
    tree.pack(pady=10)
    ticket_ui_elements["tree"] = tree
    populate_parts_table()

# ---------- Date Field Formatter ----------
def format_and_validate_date(event, date_entry):
    if event.keysym == "BackSpace":
        return

    digits = [c for c in date_entry.get() if c.isdigit()]
    new_text = ""

    # Month (MM)
    if len(digits) >= 1:
        if int(digits[0]) > 1:
            digits.insert(0, '0')
    if len(digits) >= 2:
        month = int(''.join(digits[0:2]))
        month = min(max(month, 1), 12)
        new_text += f"{month:02d}/"
    elif len(digits) >= 1:
        new_text += digits[0]

    # Day (DD)
    if len(digits) >= 3:
        if int(digits[2]) > 3:
            digits.insert(2, '0')
    if len(digits) >= 4:
        day = int(''.join(digits[2:4]))
        day = min(max(day, 1), 31)
        new_text += f"{day:02d}/"
    elif len(digits) >= 3:
        new_text += digits[2]

    # Year (YYYY starting with '2')
    if len(digits) >= 5:
        if digits[4] != '2':
            digits[4] = '2'
    if len(digits) >= 5:
        year_digits = digits[4:8]
        new_text += ''.join(year_digits)

    formatted_date = new_text[:10]
    date_entry.delete(0, tk.END)
    date_entry.insert(0, formatted_date)

    # Extra date logic for Finish or PickUp dates
    field_map = {v: k for k, v in ticket_ui_elements["entries"].items()}
    label = field_map.get(date_entry, "")
    if label in ["Finish Date", "PickUp Date"]:
        drop_entry = ticket_ui_elements["entries"].get("DropOff Date")
        finish_text = ticket_ui_elements["entries"].get("Finish Date")
        pickup_text = ticket_ui_elements["entries"].get("PickUp Date")
        try:
            drop_date = datetime.strptime(drop_entry.get(), "%m/%d/%Y")
            if label == "Finish Date":
                finish_date = datetime.strptime(finish_text.get(), "%m/%d/%Y")
                if finish_date < drop_date:
                    messagebox.showerror("Invalid Date", "Finish Date cannot be before DropOff Date.")
            elif label == "PickUp Date":
                pickup_date = datetime.strptime(pickup_text.get(), "%m/%d/%Y")
                if finish_text:
                    finish_date = datetime.strptime(finish_text.get(), "%m/%d/%Y")
                    if pickup_date < finish_date:
                        messagebox.showerror("Invalid Date", "PickUp Date cannot be before Finish Date.")
                        date_entry.delete(0, tk.END)
                        return
                if pickup_date < drop_date:
                    messagebox.showerror("Invalid Date", "PickUp Date cannot be before DropOff Date.")
                    date_entry.delete(0, tk.END)
        except:
            pass

def simple_date_format(value):
    if isinstance(value, (datetime, date)):
        return value.strftime("%m/%d/%Y")
    elif isinstance(value, str) and len(value) >= 10:
        return value[:10]
    else:
        return str(value)

# ---------- Field Populators ----------
def populate_fields(ticket):
    field_map = {
        "First Name": "FirstName",
        "Last Name": "LastName",
        "Mobile": "Mobile",
        "Email": "Email",
        "Employee": "Employee",
        "Technician": "Technician",
        "Labor Type": "LaborType",
        "Labor Price": "LaborPrice",
        "Labor Status": "LaborStatus",
        "DropOff Date": "DropOffDate",
        "Finish Date": "CompleteDate",
        "PickUp Date": "PickUpDate",
        "Gun Brand": "GunBrand",
        "Gun Model": "GunModel",
        "Serial Number": "SerialNum",
        "Purchase Location": "PurchaseLocation",
        "Purchase Date": "PurchaseDate",
    }

    for ui_key, entry in ticket_ui_elements["entries"].items():
        data_key = field_map.get(ui_key, ui_key.replace(" ", ""))
        if data_key in ticket and ticket[data_key] is not None:
            value = ticket[data_key]
            if data_key.endswith("Date"):
                value = simple_date_format(value)
            was_readonly = str(entry.cget("state")) == "readonly"
            if was_readonly:
                entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, str(value))
            if was_readonly:
                entry.config(state="readonly")

    for ui_key, textbox in ticket_ui_elements["textboxes"].items():
        data_key = field_map.get(ui_key, ui_key.replace(" ", ""))
        if data_key in ticket and ticket[data_key] is not None:
            textbox.delete("1.0", tk.END)
            textbox.insert("1.0", str(ticket[data_key]))

    for ui_key, dropdown in ticket_ui_elements["dropdowns"].items():
        data_key = field_map.get(ui_key, ui_key.replace(" ", ""))
        value = ticket.get(data_key)
        if data_key == "LaborType":
            dropdown.set(str(value) if value else "Did not specify")
        elif data_key == "LaborStatus":
            dropdown.set(str(value) if value else "Pending")
        elif value is not None:
            dropdown.set(str(value))

# ---------- Labor Handling ----------
def update_labor_price():
    mapping = {
        "Did not specify": "0.00",
        "External": "30.00",
        "Internal": "60.00",
        "External & Internal": "75.00",
        "Advanced": "80.00",
        "Connector": "19.00"
    }
    labor_type_value = ticket_ui_elements["dropdowns"]["Labor Type"].get()
    if labor_type_value in mapping:
        labor_price_entry = ticket_ui_elements["entries"]["Labor Price"]
        labor_price_entry.delete(0, tk.END)
        labor_price_entry.insert(0, mapping[labor_type_value])
    update_totals()

# ---------- Totals Calculation ----------
def update_totals():
    try:
        labor_price = Decimal(ticket_ui_elements["entries"]["Labor Price"].get() or 0)
        parts_total = sum(p["PartQuantity"] * p["PartPrice"] for p in current_parts)
        subtotal = labor_price + parts_total

        tax_rate = Decimal(ticket_ui_elements["entries"]["Tax"].get() or 0)
        tax_amount = subtotal * (tax_rate / 100)
        total = subtotal + tax_amount

        ticket_ui_elements["labels"]["subtotal"].config(text=f"Subtotal: ${subtotal:.2f}")
        ticket_ui_elements["labels"]["total"].config(text=f"Total: ${total:.2f}")
    except Exception as e:
        print("Error updating totals:", e)

def populate_parts_table():
    tree = ticket_ui_elements["tree"]
    for part in current_parts:
        tree.insert("", "end", values=(part["PartName"], part["PartQuantity"], f"${part['PartPrice']:.2f}"))

def delete_selected_part():
    tree = ticket_ui_elements["tree"]
    selected = tree.selection()
    if selected:
        for item in selected:
            values = tree.item(item, "values")
            name = values[0]
            qty = int(values[1])
            price = Decimal(values[2].replace("$", ""))
            tree.delete(item)
            for p in current_parts:
                if p["PartName"] == name and p["PartQuantity"] == qty and p["PartPrice"] == price:
                    current_parts.remove(p)
                    break
        update_totals()
    else:
        messagebox.showerror("No selection", "Please select a part to delete.")

# ---------- Data Handling ----------
def read_part_list(labor_id):
    try:
        conn = pyodbc.connect(get_database_conn_str())
        cursor = conn.cursor()
        query = "SELECT PartName, PartQuantity, PartPrice FROM Parts WHERE LaborID = ?"
        cursor.execute(query, labor_id)
        rows = cursor.fetchall()
        return [{"PartName": r[0], "PartQuantity": r[1], "PartPrice": r[2]} for r in rows]
    except Exception as e:
        print(f"Failed to load parts: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def read_ticket_data_from_access():
    try:
        conn = pyodbc.connect(get_database_conn_str())
        cursor = conn.cursor()
        query = '''
            SELECT Labor.LaborID, Labor.GunID, Labor.Employee, Labor.WorkDescription, Labor.AdditionalComments,
                   Labor.AdditionalParts, Labor.Technician, Labor.LaborType, Labor.LaborPrice, Labor.LaborStatus, Labor.CompleteDate,
                   Guns.GunID, Guns.CustomerID, Guns.DropOffDate, Guns.GunBrand, Guns.GunModel, Guns.SerialNum,
                   Guns.PurchaseLocation, Guns.PurchaseDate, Guns.PastInfo, Guns.PickUpDate,
                   Customer.CustomerID, Customer.FirstName, Customer.LastName, Customer.Email, Customer.Mobile
            FROM ((Labor
            LEFT JOIN Guns ON Labor.GunID = Guns.GunID)
            LEFT JOIN Customer ON Guns.CustomerID = Customer.CustomerID)
        '''
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        tickets = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return tickets
    except Exception as e:
        messagebox.showerror("Database Error", f"Error retrieving tickets: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def save_changes():
    try:
        conn = pyodbc.connect(get_database_conn_str())
        cursor = conn.cursor()
        labor_id = current_ticket["LaborID"]

        def parse_date(label):
            try:
                date_str = ticket_ui_elements["entries"][label].get()
                dt = datetime.strptime(date_str, "%m/%d/%Y")
                return dt.date()
            except:
                return None

        # --- Update Labor ---
        cursor.execute('''
            UPDATE Labor SET
                Employee = ?, WorkDescription = ?, AdditionalComments = ?,
                AdditionalParts = ?, Technician = ?, LaborType = ?,
                LaborPrice = ?, LaborStatus = ?, CompleteDate = ?
            WHERE LaborID = ?
        ''', (
            ticket_ui_elements["entries"]["Employee"].get(),
            ticket_ui_elements["textboxes"]["Work Description"].get("1.0", tk.END).strip(),
            ticket_ui_elements["textboxes"]["Additional Comments"].get("1.0", tk.END).strip(),
            ticket_ui_elements["textboxes"]["Additional Parts"].get("1.0", tk.END).strip(),
            ticket_ui_elements["entries"]["Technician"].get(),
            ticket_ui_elements["dropdowns"]["Labor Type"].get(),
            float(ticket_ui_elements["entries"]["Labor Price"].get() or 0),
            ticket_ui_elements["dropdowns"]["Labor Status"].get(),
            parse_date("Finish Date"),
            labor_id
        ))

        # --- Update Guns ---
        cursor.execute('''
            UPDATE Guns SET
                DropOffDate = ?, GunBrand = ?, GunModel = ?,
                PurchaseLocation = ?, PurchaseDate = ?, PastInfo = ?, PickUpDate = ?
            WHERE GunID = ?
        ''', (
            parse_date("DropOff Date"),
            ticket_ui_elements["entries"]["Gun Brand"].get(),
            ticket_ui_elements["entries"]["Gun Model"].get(),
            ticket_ui_elements["entries"]["Purchase Location"].get(),
            parse_date("Purchase Date"),
            ticket_ui_elements["textboxes"]["Past Info"].get("1.0", tk.END).strip(),
            parse_date("PickUp Date"),
            current_ticket["GunID"]
        ))

        # --- Update Customer ---
        cursor.execute('''
            UPDATE Customer SET
                FirstName = ?, LastName = ?, Email = ?, Mobile = ?
            WHERE CustomerID = ?
        ''', (
            ticket_ui_elements["entries"]["First Name"].get(),
            ticket_ui_elements["entries"]["Last Name"].get(),
            ticket_ui_elements["entries"]["Email"].get(),
            ticket_ui_elements["entries"]["Mobile"].get(),
            current_ticket["CustomerID"]
        ))

        # --- Clear & Reinsert Parts ---
        cursor.execute("DELETE FROM Parts WHERE LaborID = ?", labor_id)
        for part in current_parts:
            cursor.execute('''
                INSERT INTO Parts (LaborID, PartName, PartQuantity, PartPrice)
                VALUES (?, ?, ?, ?)
            ''', (labor_id, part["PartName"], part["PartQuantity"], part["PartPrice"]))

        conn.commit()
        messagebox.showinfo("Success", "Ticket and parts saved successfully.")
    except Exception as e:
        messagebox.showerror("Save Error", f"An error occurred while saving: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def save_to_pdf():
    # This method generates an HTML file that you can open in your browser
    # and then use the browser's built-in "Print to PDF" feature.
    file_path = asksaveasfilename(defaultextension=".html",
                                  filetypes=[("HTML Files", "*.html")],
                                  title="Save Ticket as HTML (Print to PDF)")
    if not file_path:
        return

    try:
        html_content = (
            "<html>"
            "<head>"
            "<meta charset='UTF-8'>"
            "<title>Ticket Information</title>"
            "<style>"
            "  @page { size: letter; margin: 5mm; }"
            "  body { margin: 0; padding: 5mm; font-family: Arial, sans-serif; font-size: 9pt; }"
            "  h1 { text-align: center; font-size: 14pt; margin: 0 0 5mm 0; }"
            "  h2 { font-size: 12pt; margin: 3mm 0 2mm 0; }"
            "  p { margin: 1mm 0; }"
            "  hr { border: 1px solid #000; margin: 2mm 0; }"
            "  .no-break { page-break-inside: avoid; }"
            "</style>"
            "</head>"
            "<body>"
        )
        
        # Title
        html_content += "<h1>Ticket Information</h1>"
        html_content += "<hr>"
        
        # Customer Info
        html_content += (
            f"<p><strong>First Name:</strong> {ticket_ui_elements['entries']['First Name'].get()}</p>"
            f"<p><strong>Last Name:</strong> {ticket_ui_elements['entries']['Last Name'].get()}</p>"
            f"<p><strong>Mobile:</strong> {ticket_ui_elements['entries']['Mobile'].get()}</p>"
            f"<p><strong>Email:</strong> {ticket_ui_elements['entries']['Email'].get()}</p>"
            "<br>"
        )
        
        # Received and Purchase Info
        html_content += (
            f"<p><strong>Employee:</strong> {ticket_ui_elements['entries']['Employee'].get()}</p>"
            f"<p><strong>Purchase Location:</strong> {ticket_ui_elements['entries']['Purchase Location'].get()}</p>"
            f"<p><strong>Purchase Date:</strong> {ticket_ui_elements['entries']['Purchase Date'].get()}</p>"
            "<br>"
        )
        
        # Gun and Notes Info
        html_content += (
            f"<p><strong>Gun Brand:</strong> {ticket_ui_elements['entries']['Gun Brand'].get()}</p>"
            f"<p><strong>Gun Model:</strong> {ticket_ui_elements['entries']['Gun Model'].get()}</p>"
            f"<p><strong>Serial Number:</strong> {ticket_ui_elements['entries']['Serial Number'].get()}</p>"
        )
        past_info = ticket_ui_elements["textboxes"]["Past Info"].get("1.0", tk.END).strip()
        if past_info:
            html_content += "<p><strong>Past Info:</strong><br>" + past_info.replace("\n", "<br>") + "</p>"
        work_desc = ticket_ui_elements["textboxes"]["Work Description"].get("1.0", tk.END).strip()
        if work_desc:
            html_content += "<p><strong>Work Description:</strong><br>" + work_desc.replace("\n", "<br>") + "</p>"
        additional_parts = ticket_ui_elements["textboxes"]["Additional Parts"].get("1.0", tk.END).strip()
        if additional_parts:
            html_content += "<p><strong>Additional Parts:</strong><br>" + additional_parts.replace("\n", "<br>") + "</p>"
        additional_comments = ticket_ui_elements["textboxes"]["Additional Comments"].get("1.0", tk.END).strip()
        if additional_comments:
            html_content += "<p><strong>Additional Comments:</strong><br>" + additional_comments.replace("\n", "<br>") + "</p>"
        html_content += "<br>"
        
        # Labor Info
        html_content += (
            f"<p><strong>Technician:</strong> {ticket_ui_elements['entries']['Technician'].get()}</p>"
            f"<p><strong>Labor Type:</strong> {ticket_ui_elements['dropdowns']['Labor Type'].get()}</p>"
            f"<p><strong>Labor Price:</strong> {ticket_ui_elements['entries']['Labor Price'].get()}</p>"
            "<br>"
        )
        
        # Parts List (with bold labels for each field)
        html_content += "<h2>Parts List</h2>"
        if current_parts:
            for part in current_parts:
                html_content += (
                    f"<p><strong>Part Name:</strong> {part['PartName']}, "
                    f"<strong>Quantity:</strong> {part['PartQuantity']}, "
                    f"<strong>Price:</strong> ${part['PartPrice']:.2f}</p>"
                )
        else:
            html_content += "<p>No parts added.</p>"
        html_content += "<br>"
        
        # Totals (with Tax Rate)
        html_content += f"<p><strong>Tax Rate:</strong> 8.75%</p>"
        subtotal = ticket_ui_elements["labels"]["subtotal"].cget("text")
        total = ticket_ui_elements["labels"]["total"].cget("text")
        html_content += f"<p><strong>{subtotal}</strong></p>"
        html_content += f"<p><strong>{total}</strong></p>"
        html_content += "<br>"
        
        # Dates & Status
        html_content += (
            f"<p><strong>Labor Status:</strong> {ticket_ui_elements['dropdowns']['Labor Status'].get()}</p>"
            f"<p><strong>DropOff Date:</strong> {ticket_ui_elements['entries']['DropOff Date'].get()}</p>"
            f"<p><strong>Finish Date:</strong> {ticket_ui_elements['entries']['Finish Date'].get()}</p>"
            f"<p><strong>PickUp Date:</strong> {ticket_ui_elements['entries']['PickUp Date'].get()}</p>"
            "<br>"
        )
        
        # Customer Print and Signature Section
        html_content += (
            "<h2>Customer Information</h2>"
            "<p><strong>Customer Print Name:</strong> _______________________________________</p>"
            "<p><strong>Customer Signature:</strong> _______________________________________</p>"
        )
        
        # Close HTML
        html_content += "</body></html>"
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        messagebox.showinfo("HTML Saved",
            "Ticket information saved as HTML.\nOpen it in your browser and use Print → Save as PDF (disable headers/footers if needed).")
        webbrowser.open(file_path)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving HTML:\n{e}")

def add_save_pdf_button(frame):
    pdf_button = tk.Button(frame, text="Save as HTML (Print to PDF)", command=save_to_pdf)
    pdf_button.pack(side="left", padx=5)
