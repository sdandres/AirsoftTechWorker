from tkinter import END, messagebox
from datetime import datetime
from utils.path_utils import get_database_conn_str
import webbrowser
from html import escape
from utils.path_utils import relative_to_assets
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
    
    if not window.gun_model_entry.get().strip():
        messagebox.showerror("Invalid Input", "Gun model cannot be empty.")
        return False
    
    if not window.gun_serial_entry.get().strip():
        messagebox.showerror("Invalid Input", "Gun model cannot be empty.")
        return False
    
    if not window.gun_serial_entry.get().strip():
        messagebox.showerror("Invalid Input", "Gun model cannot be empty.")
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

        cursor.execute(guns_insert_query, guns_values)

        # Retrieve generated GunID
        cursor.execute("SELECT @@IDENTITY")
        gun_id = cursor.fetchone()[0]

        # Insert into Labor table
        labor_insert_query = """
        INSERT INTO Labor (GunID, Employee, WorkDescription, AdditionalComments, AdditionalParts, Technician, LaborType, LaborPrice, LaborStatus, CompleteDate)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        labor_values = (
            gun_id,
            window.received_by_entry.get(),
            window.work_entry.get(),
            window.add_comment_entry.get(),
            window.add_parts_entry.get(),
            None,
            None,
            None,
            "Pending",
            None,
        )
        cursor.execute(labor_insert_query, labor_values)

        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Success", "Gun record added successfully!")
        generate_new_ticket_work_order(window)
        clear_form(window)

    except Exception as e:
        messagebox.showerror("Database Error", f"Error saving to database: {e}")

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

def generate_new_ticket_work_order(window):
    def esc(x): return escape(x.strip()) if x else ""
    today = datetime.today().strftime("%m/%d/%Y")

    # Retrieve customer information from database using hidden_customer_id
    customer_id = window.hidden_customer_id.get()
    first_name = last_name = mobile = email = ""
    try:
        conn = pyodbc.connect(get_database_conn_str())
        cursor = conn.cursor()
        cursor.execute("SELECT FirstName, LastName, Mobile, Email FROM Customer WHERE CustomerID = ?", customer_id)
        row = cursor.fetchone()
        if row:
            first_name = esc(row.FirstName)
            last_name = esc(row.LastName)
            mobile = esc(row.Mobile)
            email = esc(row.Email)
        cursor.close()
        conn.close()
    except Exception as e:
        print("Error retrieving customer info:", e)

    full_name = f"{first_name} {last_name}".strip()
    employee = esc(window.received_by_entry.get())
    logo_path = relative_to_assets("aalogo_resized.png").as_uri()

    purchase_location = esc(window.purchase_location_entry.get())
    purchase_date = esc(window.purchase_date_entry.get())
    gun_brand = esc(window.gun_brand_combobox.get())
    gun_model = esc(window.gun_model_entry.get())
    gun_serial = esc(window.gun_serial_entry.get())
    drop_off_date = esc(window.drop_off_date_entry.get())

    past_info = esc(window.past_entry.get()).replace("\n", "<br>")
    work_desc = esc(window.work_entry.get()).replace("\n", "<br>")
    add_parts = esc(window.add_parts_entry.get()).replace("\n", "<br>")
    add_comments = esc(window.add_comment_entry.get()).replace("\n", "<br>")

    html = f"""
    <html>
    <head>
        <meta charset='UTF-8'>
        <title>Work Order</title>
        <style>
            body {{ font-family: Arial, sans-serif; font-size: 10pt; margin: 0; padding: 0; }}
            .header {{ display: flex; justify-content: space-between; align-items: center; padding: 15px 25px 5px; }}
            .logo img {{ height: 70px; }}
            .bar {{ background: #6E6E48; color: white; text-align: center; padding: 6px; font-weight: bold; }}
            .content {{ padding: 20px 30px; }}
            .section {{ margin-bottom: 20px; }}
            .row {{ display: flex; justify-content: space-between; margin-bottom: 6px; }}
            .column {{ display: flex; flex-direction: column; }}
            .label {{ font-weight: bold; margin-right: 5px; }}
            .signature-space .line {{
                display: inline-block;
                border-bottom: 1px solid #000;
                width: 160px;
            }}
            .signature-space p {{
                margin-bottom: 40px;
            }}
            .terms-box {{
                border: 1px solid #ccc;
                display: flex;
                margin-top: 40px;
            }}
            .terms-box .title {{
                background-color: #6E6E48;
                color: white;
                font-weight: bold;
                padding: 10px;
                width: 140px;
            }}
            .terms-box .text {{
                padding: 10px;
                font-size: 9pt;
            }}
            .terms-box .text b {{
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="business-info">
                <strong>America Airsoft</strong><br>
                12401 Folsom Blvd Suite 109<br>
                Rancho Cordova, CA 95742<br>
                Located inside Nimbus Winery<br>
                (916) 790 - 8376
            </div>
            <div class="logo"><img src="{logo_path}"></div>
        </div>

        <div class="bar">WORK ORDER</div>

        <div class="content">
            <div class="section">
                <div><span class="label">Customer:</span> {full_name}</div>
                <div><span class="label">Mobile:</span> {mobile}</div>
                <div><span class="label">Email:</span> {email}</div>
            </div>

            <div class="section">
                <div><span class="label">Employee:</span> {employee}</div>
            </div>

            <div class="section">
                <div><span class="label">Purchase Location:</span> {purchase_location}</div>
                <div><span class="label">Purchase Date:</span> {purchase_date}</div>
            </div>

            <div class="section">
                <div><span class="label">Gun Brand:</span> {gun_brand}</div>
                <div><span class="label">Gun Model:</span> {gun_model}</div>
                <div><span class="label">Serial Number:</span> {gun_serial}</div>
                <div><span class="label">DropOff Date:</span> {drop_off_date}</div>
            </div>

            <div class="section">
                <div><span class="label">Past Info:</span><br>{past_info}</div>
            </div>
            <div class="section">
                <div><span class="label">Work Description:</span><br>{work_desc}</div>
            </div>
            <div class="section">
                <div><span class="label">Additional Parts:</span><br>{add_parts}</div>
            </div>
            <div class="section">
                <div><span class="label">Additional Comments:</span><br>{add_comments}</div>
            </div>

            <div class="terms-box">
                <div class="title">TERMS OF SERVICE</div>
                <div class="text">
                    All work will be subject to a minimum non-refundable $40 evaluation fee; If client decides to
                    proceed with repair, fee will be applied to final repair cost. Repair work will be warrantied for 30
                    days from repair finish date. <b>***Any item(s) that are not picked up within 60 days after finish date,
                    will have ownership forfeited to America Airsoft to be dealt with at their discretion.</b>
                </div>
            </div>

            <div class="section signature-space">
                <p><strong>Date:</strong> {today}</p>
                <p>
                    <strong>Customer Printed Name:</strong> <span class="line">{full_name}</span>
                    &nbsp;&nbsp;&nbsp;&nbsp;
                    <strong>Signature:</strong> <span class="line"></span>
                </p>
                <p>
                    <strong>Employee Printed Name:</strong> <span class="line">{employee}</span>
                    &nbsp;&nbsp;&nbsp;&nbsp;
                    <strong>Signature:</strong> <span class="line"></span>
                </p>
            </div>
        </div>
    </body>
    </html>
    """

    preview_file = relative_to_assets("work_order_preview.html")
    with open(preview_file, "w", encoding="utf-8") as f:
        f.write(html)
    webbrowser.open(preview_file.as_uri())