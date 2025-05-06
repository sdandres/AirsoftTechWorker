# tickets_utils.py (overhauled)

import tkinter as tk
from tkinter import ttk, messagebox
from utils.path_utils import get_database_conn_str
from utils.path_utils import get_assets_path
import os
import pyodbc
from datetime import datetime, date
from decimal import Decimal

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

    canvas = tk.Canvas(window)
    canvas.pack(fill="both", expand=True)

    frame = tk.Frame(canvas, padx=20, pady=20)
    frame.pack()

    build_sections(frame)
    populate_fields(ticket_data)
    bind_total_events()
    update_totals()
    update_totals()

    def on_close():
            if refresh_callback:
                refresh_callback()
            window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_close)
    window.bind("<Control-s>", lambda e: save_changes())
    window.mainloop()

# ---------- Section Builders ----------
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

    if label in ["Labor Price"]:
        entry.config(validate="key", validatecommand=(row.register(validate_numeric_input), "%P"))

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

# ---------- Numeric Field Formatter ----------
def validate_numeric_input(new_value):
    if new_value == "":
        return True
    try:
        float(new_value)
        return True
    except ValueError:
        return False

    
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

    vcmd = (parts_frame.register(validate_numeric_input), "%P")

    tk.Label(entry_row, text="Part Name").grid(row=0, column=0, padx=5)
    part_name_entry = tk.Entry(entry_row, width=20)
    part_name_entry.grid(row=1, column=0, padx=5)
    ticket_ui_elements["parts_name"] = part_name_entry

    tk.Label(entry_row, text="Quantity").grid(row=0, column=1, padx=5)
    part_qty_entry = tk.Entry(entry_row, width=10, validate="key", validatecommand=vcmd)
    part_qty_entry.grid(row=1, column=1, padx=5)
    ticket_ui_elements["parts_qty"] = part_qty_entry

    tk.Label(entry_row, text="Price ($)").grid(row=0, column=2, padx=5)
    part_price_entry = tk.Entry(entry_row, width=10, validate="key", validatecommand=vcmd)
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

    vcmd = (totals_frame.register(validate_numeric_input), "%P")

    ticket_ui_elements["labels"]["subtotal"] = tk.Label(totals_frame, text="Subtotal: $0.00", font=("Arial", 10))
    ticket_ui_elements["labels"]["subtotal"].pack(anchor="w")

    tk.Label(totals_frame, text="Tax (%)").pack(anchor="w")
    tax_entry = tk.Entry(totals_frame, width=10, validate="key", validatecommand=vcmd)
    tax_entry.insert(0, "8.75")
    tax_entry.pack(anchor="w")
    ticket_ui_elements["entries"]["Tax"] = tax_entry

    ticket_ui_elements["labels"]["total"] = tk.Label(totals_frame, text="Total: $0.00", font=("Arial", 10, "bold"))
    ticket_ui_elements["labels"]["total"].pack(anchor="w", pady=(5, 0))

    # Dates & Status Section
    dates_frame = tk.LabelFrame(right_col, text="Current Status & Dates")
    dates_frame.pack(padx=10, pady=5, anchor="nw")
    build_dropdown(dates_frame, "Labor Status", ["Pending", "In Progress", "Waiting on Parts", "Warranty","Awaiting Pickup", "Completed", "Canceled"])
    build_label_entry(dates_frame, "DropOff Date")
    build_label_entry(dates_frame, "Finish Date")
    build_label_entry(dates_frame, "PickUp Date")

    # Save & PDF Buttons
    save_frame = tk.Frame(right_col)
    save_frame.pack(padx=10, pady=10, anchor="w")
    tk.Button(save_frame, text="Save Changes", command=save_changes).pack(side="left", padx=5)
    tk.Button(save_frame, text="Print Ticket", command=print_ticket).pack(side="left", padx=5)
    tk.Button(save_frame, text="Print Invoice", command=print_invoice).pack(side="left", padx=5)

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

    # check date logic if editing Finish or PickUp
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
                finish_text = ticket_ui_elements["entries"].get("Finish Date")
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
    
# ---------- Field Populators ----------
def simple_date_format(value):
    if isinstance(value, (datetime, date)):
        return value.strftime("%m/%d/%Y")
    elif isinstance(value, str) and len(value) >= 10:
        return value[:10]
    else:
        return str(value)
    
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
    # Mapping of labor types to default prices
    mapping = {
        "Did not specify" : "0.00",
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

# ---------- Part Handling ----------
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
    update_totals()

def delete_selected_part():
    tree = ticket_ui_elements["tree"]
    selected = tree.selection()
    if selected:
        for item in selected:
            values = tree.item(item, "values")
            name = values[0]
            qty = int(values[1])
            price = Decimal(values[2].replace("$", ""))
            # Remove from tree
            tree.delete(item)
            # Remove from global part list
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
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

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
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

def validate_ticket_data():
    # Required Entry Fields
    required_entry_fields = [
        "DropOff Date", "Employee", "Gun Brand", "Gun Model",
        "Serial Number", "Labor Price"
    ]
    for field in required_entry_fields:
        entry = ticket_ui_elements["entries"].get(field)
        if not entry or not entry.get().strip():
            messagebox.showerror("Validation Error", f"{field} cannot be empty.")
            return False

    # Required Textboxes
    required_textboxes = ["Past Info", "Work Description"]
    for label in required_textboxes:
        if not ticket_ui_elements["textboxes"][label].get("1.0", tk.END).strip():
            messagebox.showerror("Validation Error", f"{label} cannot be empty.")
            return False

    # Required Dropdowns
    required_dropdowns = ["Labor Type", "Labor Status"]
    for label in required_dropdowns:
        if not ticket_ui_elements["dropdowns"][label].get().strip():
            messagebox.showerror("Validation Error", f"{label} must be selected.")
            return False

    # Labor Price must be a number
    try:
        float(ticket_ui_elements["entries"]["Labor Price"].get())
    except ValueError:
        messagebox.showerror("Validation Error", "Labor Price must be a valid number.")
        return False

    def parse(label):
        try:
            return datetime.strptime(ticket_ui_elements["entries"][label].get(), "%m/%d/%Y")
        except:
            return None

    drop = parse("DropOff Date")
    finish = parse("Finish Date")
    pickup = parse("PickUp Date")

    if finish and drop and finish < drop:
        messagebox.showerror("Validation Error", "Finish Date cannot be before DropOff Date.")
        return False
    if pickup and finish and pickup < finish:
        messagebox.showerror("Validation Error", "PickUp Date cannot be before Finish Date.")
        return False
    if pickup and drop and pickup < drop:
        messagebox.showerror("Validation Error", "PickUp Date cannot be before DropOff Date.")
        return False

    return True

def save_changes():
    if not validate_ticket_data():
        return
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
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

from tkinter.filedialog import asksaveasfilename
import tempfile
import webbrowser
from html import escape

def open_html_in_browser(html):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8") as temp_file:
            temp_file.write(html)
            webbrowser.open(f"file:///{temp_file.name}")
    except Exception as e:
        messagebox.showerror("Print Error", f"Could not open print preview:\n{e}")

def print_invoice():
    save_changes()
    html = generate_invoice_html()
    open_html_in_browser(html)

def print_ticket():
    save_changes()
    html = generate_ticket_html()
    open_html_in_browser(html)

def generate_invoice_html():
    def esc(x): return escape(x.strip()) if x else ""

    logo_path = get_assets_path() / "aalogo_resized.png"
    logo_url = f"file:///{logo_path}" if os.path.exists(logo_path) else ""

    today = datetime.now().strftime("%B %d, %Y")

    work_description = escape(ticket_ui_elements["textboxes"]["Work Description"].get("1.0", "end").strip()).replace("\n", "<br>")
    additional_parts = escape(ticket_ui_elements["textboxes"]["Additional Parts"].get("1.0", "end").strip()).replace("\n", "<br>")
    additional_comments = escape(ticket_ui_elements["textboxes"]["Additional Comments"].get("1.0", "end").strip()).replace("\n", "<br>")

    html = f"""
    <html>
    <head>
    <meta charset='UTF-8'>
    <title>Gunsmithing Invoice</title>
    <style>
        @page {{ size: letter; margin: 10mm; }}
        body {{ font-family: Arial, sans-serif; font-size: 10pt; margin: 0; padding: 10mm; }}
        h1 {{ font-size: 16pt; color: #808060; text-align: center; margin-bottom: 8px; }}
        h2 {{ font-size: 11pt; background: #808060; color: white; padding: 4px; text-align: center; margin-top: 20px; }}
        p {{ margin: 3px 0; }}
        .header-wrap {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px; }}
        .logo {{ max-height: 100px; }}
        .left-box {{ max-width: 65%; }}
        .section {{ margin-top: 15px; }}
        .signature-space p {{ margin-top: 25px; }}
        .line {{ display: inline-block; border-bottom: 1px solid #000; width: 300px; margin-left: 5px; }}
    </style>
    </head>
    <body>

    <h1>GUNSMITHING INVOICE</h1>

    <div class="header-wrap">
        <div class="left-box">
            <strong>America Airsoft</strong><br>
            12401 Folsom Blvd Suite 109<br>
            Rancho Cordova, CA 95742<br>
            Located inside Nimbus Winery<br>
            (916) 790 - 8376
        </div>
        <div>
            <img src="{logo_url}" class="logo">
        </div>
    </div>

    <h2>WORK ORDER</h2>

    <div class="section" style="display: flex; justify-content: space-between;">
        <div>
            <p><strong>First Name:</strong> {esc(ticket_ui_elements['entries']['First Name'].get())}</p>
            <p><strong>Last Name:</strong> {esc(ticket_ui_elements['entries']['Last Name'].get())}</p>
            <p><strong>Mobile:</strong> {esc(ticket_ui_elements['entries']['Mobile'].get())}</p>
            <p><strong>Email:</strong> {esc(ticket_ui_elements['entries']['Email'].get())}</p>
        </div>
        <div style="text-align: right;">
            <p><strong>Employee:</strong> {esc(ticket_ui_elements['entries']['Employee'].get())}</p>
            <p><strong>Technician:</strong> {esc(ticket_ui_elements['entries']['Technician'].get())}</p>
        </div>
    </div>

    <div class="section">
        <p><strong>Labor Type:</strong> {esc(ticket_ui_elements['dropdowns']['Labor Type'].get())}</p>
        <p><strong>Labor Status:</strong> {esc(ticket_ui_elements['dropdowns']['Labor Status'].get())}</p>
        <p><strong>Labor Price:</strong> ${esc(ticket_ui_elements['entries']['Labor Price'].get())}</p>
    </div>

    <div class="section">
        <p><strong>Gun Brand:</strong> {esc(ticket_ui_elements['entries']['Gun Brand'].get())}</p>
        <p><strong>Gun Model:</strong> {esc(ticket_ui_elements['entries']['Gun Model'].get())}</p>
        <p><strong>Serial Number:</strong> {esc(ticket_ui_elements['entries']['Serial Number'].get())}</p>
        <p><strong>DropOff Date:</strong> {esc(ticket_ui_elements['entries']['DropOff Date'].get())}</p>
        <p><strong>Finish Date:</strong> {esc(ticket_ui_elements['entries']['Finish Date'].get())}</p>
    </div>

    <div class="section">
        <h3>Parts List</h3>
    """
    if current_parts:
        for part in current_parts:
            html += f"<p>• {esc(part['PartName'])} (x{part['PartQuantity']}) - ${float(part['PartPrice']):.2f}</p>"
    else:
        html += "<p>No parts added.</p>"

    html += f"""
    <div class="section">
        <p><strong>{ticket_ui_elements['labels']['subtotal'].cget("text")}</strong></p>
        <p><strong>Tax Rate:</strong> 8.75%</p>
        <p><strong>{ticket_ui_elements['labels']['total'].cget("text")}</strong></p>
    </div>

    </body></html>
    """
    return html

from html import escape

def generate_ticket_html():
    def esc(x): return escape(x.strip()) if x else ""

    def generate_parts_table():
        if not current_parts:
            return "<p>No parts added.</p>"
        rows = ""
        for part in current_parts:
            rows += f"<p>• {esc(part['PartName'])} (x{part['PartQuantity']}) - ${float(part['PartPrice']):.2f}</p>"
        return rows

    def html_ticket_block():
        work = escape(ticket_ui_elements["textboxes"]["Work Description"].get("1.0", "end").strip()).replace("\n", "<br>")
        add_parts = escape(ticket_ui_elements["textboxes"]["Additional Parts"].get("1.0", "end").strip()).replace("\n", "<br>")
        add_comments = escape(ticket_ui_elements["textboxes"]["Additional Comments"].get("1.0", "end").strip()).replace("\n", "<br>")

        return f"""
        <div class="ticket">
            <h2>WORK ORDER</h2>

            <div class="row">
                <div class="left"><strong>First Name:</strong> {esc(ticket_ui_elements['entries']['First Name'].get())}</div>
                <div class="center"><strong>Last Name:</strong> {esc(ticket_ui_elements['entries']['Last Name'].get())}</div>
            </div>
            <div class="row">
                <div class="left"><strong>Email:</strong> {esc(ticket_ui_elements['entries']['Email'].get())}</div>
                <div class="center"><strong>Mobile:</strong> {esc(ticket_ui_elements['entries']['Mobile'].get())}</div>
            </div>

            <div class="spacer"></div>

            <div class="row">
                <div class="left"><strong>Employee:</strong> {esc(ticket_ui_elements['entries']['Employee'].get())}</div>
                <div class="center"><strong>Technician:</strong> {esc(ticket_ui_elements['entries']['Technician'].get())}</div>
            </div>

            <div class="spacer"></div>

            <div class="row">
                <div class="left full"><strong>Gun:</strong> {esc(ticket_ui_elements['entries']['Gun Brand'].get())} / {esc(ticket_ui_elements['entries']['Gun Model'].get())} / {esc(ticket_ui_elements['entries']['Serial Number'].get())}</div>
            </div>

            <div class="row">
                <div class="left"><strong>Work Description:</strong><br>{work}</div>
                <div class="right"><strong>Additional Parts:</strong><br>{add_parts}</div>
            </div>

            <div class="row">
                <div class="left full"><strong>Additional Comments:</strong><br>{add_comments}</div>
            </div>

            <div class="spacer"></div>
            <div class="left"><strong>Labor Type:</strong> {esc(ticket_ui_elements['dropdowns']['Labor Type'].get())}</div>
            <div class="left"><strong>Status:</strong> {esc(ticket_ui_elements['dropdowns']['Labor Status'].get())}</div>

            <div class="spacer"></div>
            <div class="left"><strong>DropOff Date:</strong> {esc(ticket_ui_elements['entries']['DropOff Date'].get())}</div>
            <div class="left"><strong>Finish Date:</strong> {esc(ticket_ui_elements['entries']['Finish Date'].get())}</div>

            <div class="spacer"></div>
            <div class="row"><strong>Parts List:</strong></div>
            <div class="parts">{generate_parts_table()}</div>
        </div>
        """

    html = f"""
    <html>
    <head>
    <meta charset='UTF-8'>
    <title>Internal Ticket</title>
    <style>
        @page {{ size: letter; margin: 0; }}
        body {{
            font-family: Arial, sans-serif;
            font-size: 9pt;
            margin: 0;
            padding: 0;
            position: relative;
            height: 100vh;
        }}
        .ticket {{
            height: 50vh;
            padding: 15mm;
            box-sizing: border-box;
            overflow: hidden;
        }}
        h2 {{
            font-size: 14pt;
            text-align: center;
            margin-bottom: 5px;
        }}
        .row {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 2px;
        }}
        .left {{ width: 48%; }}
        .center {{ width: 48%; text-align: right; }}
        .right {{ width: 48%; text-align: right; }}
        .full {{ width: 100%; }}
        .spacer {{ height: 8px; }}
        .cut-line {{
            position: absolute;
            top: 50%;
            left: 0;
            width: 100%;
            border-top: 1px dashed #000;
            text-align: center;
            font-size: 10pt;
        }}
        .parts p {{ margin: 1px 0; }}
    </style>
    </head>
    <body>
        {html_ticket_block()}
        <div class="cut-line">✂️ CUT HERE ✂️</div>
        {html_ticket_block()}
    </body>
    </html>
    """
    return html