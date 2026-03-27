import tkinter as tk
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Toplevel, messagebox
from tkinter import ttk
from pathlib import Path
import pyodbc

# 1. PATH SETUP
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Admin\OneDrive\Desktop\MIS 161\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# 2. DATABASE CONNECTION
conn_str = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=C:\Users\Admin\OneDrive\Desktop\MIS 161\AmericaAirsoft1.accdb;"
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# 3. MAIN WINDOW
window = Tk()
window.geometry("1440x1024")
window.configure(bg="#272549")
window.resizable(False, False)

# 4. CANVAS
canvas = Canvas(
    window,
    bg="#272549",
    height=1024,
    width=1440,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# ------------------------------------------------------------------
# 5. BACKGROUND & NAV BUTTONS
# ------------------------------------------------------------------

# Draw background rectangles
canvas.create_rectangle(79.0, 152.0, 1359.0, 872.0, fill="#FFFFFF", outline="")
canvas.create_rectangle(171.0, 325.0, 1125.0, 365.0, fill="#000000", outline="")

# -- HOME BUTTON (button_10.png) --
button_image_10 = PhotoImage(file=relative_to_assets("button_10.png"))
button_10 = Button(
    window,
    image=button_image_10,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("Home clicked"),
    relief="flat"
)
button_10.place(x=79.0, y=152.0, width=213.33, height=150.0)

# -- TICKETS BUTTON (button_11.png) --
button_image_11 = PhotoImage(file=relative_to_assets("button_11.png"))
button_11 = Button(
    window,
    image=button_image_11,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("Tickets clicked"),
    relief="flat"
)
button_11.place(x=933.0, y=152.0, width=214.0, height=150.0)

# -- INVENTORY BUTTON (button_12.png) --
button_image_12 = PhotoImage(file=relative_to_assets("button_12.png"))
button_12 = Button(
    window,
    image=button_image_12,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("Inventory clicked"),
    relief="flat"
)
button_12.place(x=1146.0, y=152.0, width=213.33, height=150.0)

# -- CUSTOMERS BUTTON (button_13.png) --
button_image_13 = PhotoImage(file=relative_to_assets("button_13.png"))
button_13 = Button(
    window,
    image=button_image_13,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("Customers clicked"),
    relief="flat"
)
button_13.place(x=719.0, y=152.0, width=214.0, height=150.0)

# -- NEW TICKET BUTTON (button_14.png) --
button_image_14 = PhotoImage(file=relative_to_assets("button_14.png"))
button_14 = Button(
    window,
    image=button_image_14,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("New Ticket clicked"),
    relief="flat"
)
button_14.place(x=506.0, y=152.0, width=214.0, height=150.0)

# -- ONBOARDING BUTTON (button_15.png) --
button_image_15 = PhotoImage(file=relative_to_assets("button_15.png"))
button_15 = Button(
    window,
    image=button_image_15,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("Onboarding clicked"),
    relief="flat"
)
button_15.place(x=292.0, y=152.0, width=214.0, height=150.0)

# -- SEARCH BUTTON (button_1.png) --
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    window,
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("Search clicked"),
    relief="flat"
)
button_1.place(x=106.0, y=319.0, width=47.0, height=46.0)

# -- DELETE BUTTON (button_16.png) --
button_image_16 = PhotoImage(file=relative_to_assets("button_16.png"))
button_16 = Button(
    window,
    image=button_image_16,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("Delete clicked"),
    relief="flat"
)
button_16.place(x=1130.0, y=326.0, width=120.0, height=33.0)

# -------------------------------------------------------------------------
# 6. SEARCH BAR, TABLE, SINGLE EDIT BUTTON, ETC.
# -------------------------------------------------------------------------
search_var = tk.StringVar()
search_entry = Entry(window, textvariable=search_var, font=("Arial", 14))
search_entry.place(x=172, y=326, width=950, height=36)

style = ttk.Style()
style.configure("Treeview", rowheight=30)
style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

table_frame = tk.Frame(window)
table_frame.place(x=169, y=425, width=1162, height=400)

tree_scrollbar = ttk.Scrollbar(table_frame, orient="vertical")
tree_scrollbar.pack(side="right", fill="y")

columns = ("CustomerID", "FirstName", "LastName", "Email", "Mobile", "Address")
tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    yscrollcommand=tree_scrollbar.set,
    style="Treeview"
)

tree.column("CustomerID", width=80, anchor="center")
tree.column("FirstName", width=120, anchor="center")
tree.column("LastName", width=120, anchor="center")
tree.column("Email", width=180, anchor="center")
tree.column("Mobile", width=120, anchor="center")
tree.column("Address", width=200, anchor="w")

for col in columns:
    tree.heading(col, text=col)

tree.pack(side="left", fill="both", expand=True)
tree_scrollbar.config(command=tree.yview)

# -------------------------------------------------------------------------
# 7. FUNCTIONS
# -------------------------------------------------------------------------
def refresh_table():
    """Load numeric IDs from the DB and clean up extra characters in data."""
    for item in tree.get_children():
        tree.delete(item)
    
    cursor.execute("SELECT CustomerID, FirstName, LastName, Email, Mobile, Address FROM Customer")
    rows = cursor.fetchall()
    
    for row in rows:
        # Convert row from tuple with potential trailing commas to clean values
        cleaned_row = tuple(str(value).strip().replace(",", "").replace("'", "") for value in row)
        tree.insert("", tk.END, values=cleaned_row)


def on_search():
    """Search by numeric CustomerID. E.g., user types '1' if they want ID=1."""
    raw_input = search_var.get().strip()
    if not raw_input:
        messagebox.showwarning("Warning", "Please enter a numeric Customer ID to search.")
        return
    
    try:
        cust_id = int(raw_input)
    except ValueError:
        messagebox.showerror("Error", "Customer ID must be a number (e.g., 1, 2, 3).")
        return

    for item in tree.get_children():
        tree.delete(item)

    cursor.execute(
        "SELECT CustomerID, FirstName, LastName, Email, Mobile, Address FROM Customer WHERE CustomerID = ?",
        (cust_id,)
    )
    row = cursor.fetchone()
    if row:
        tree.insert("", tk.END, values=row)
    else:
        messagebox.showerror("Not Found", f"No customer with numeric ID {cust_id}")

def on_delete_click():
    delete_win = Toplevel(window)
    delete_win.title("Delete Customer")
    delete_win.geometry("300x150")

    tk.Label(delete_win, text="Enter numeric Customer ID to delete:").pack(pady=10)
    del_id_var = tk.StringVar()
    del_id_entry = Entry(delete_win, textvariable=del_id_var)
    del_id_entry.pack(pady=5)

    def confirm_delete():
        raw = del_id_var.get().strip()
        if not raw:
            messagebox.showwarning("Warning", "Please enter a numeric Customer ID.")
            return
        try:
            cust_id = int(raw)
        except ValueError:
            messagebox.showerror("Error", "Customer ID must be a number.")
            return
        
        answer = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete ID {cust_id}?")
        if answer:
            cursor.execute("DELETE FROM Customer WHERE CustomerID = ?", (cust_id,))
            conn.commit()
            messagebox.showinfo("Deleted", f"Customer {cust_id} deleted.")
            refresh_table()
            delete_win.destroy()

    delete_btn = Button(delete_win, text="Delete", command=confirm_delete)
    delete_btn.pack(pady=5)

def open_edit_window(cust_id):
    """Open a Toplevel to edit the row with numeric CustomerID=cust_id."""
    cursor.execute(
        "SELECT CustomerID, FirstName, LastName, Email, Mobile, Address FROM Customer WHERE CustomerID = ?",
        (cust_id,)
    )
    row = cursor.fetchone()
    if not row:
        messagebox.showerror("Error", f"No record found for numeric ID {cust_id}")
        return

    edit_win = Toplevel(window)
    edit_win.title(f"Edit Customer {cust_id}")
    edit_win.geometry("400x350")

    tk.Label(edit_win, text="Customer ID").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(edit_win, text="First Name").grid(row=1, column=0, padx=10, pady=5)
    tk.Label(edit_win, text="Last Name").grid(row=2, column=0, padx=10, pady=5)
    tk.Label(edit_win, text="Email").grid(row=3, column=0, padx=10, pady=5)
    tk.Label(edit_win, text="Mobile").grid(row=4, column=0, padx=10, pady=5)
    tk.Label(edit_win, text="Address").grid(row=5, column=0, padx=10, pady=5)

    id_var = tk.IntVar(value=row[0])
    fn_var = tk.StringVar(value=row[1])
    ln_var = tk.StringVar(value=row[2])
    mobile_var = tk.StringVar(value=row[3])
    email_var = tk.StringVar(value=row[4])
    addr_var = tk.StringVar(value=row[5])

    Entry(edit_win, textvariable=id_var, state='readonly').grid(row=0, column=1, padx=10, pady=5)
    Entry(edit_win, textvariable=fn_var).grid(row=1, column=1, padx=10, pady=5)
    Entry(edit_win, textvariable=ln_var).grid(row=2, column=1, padx=10, pady=5)
    Entry(edit_win, textvariable=mobile_var).grid(row=3, column=1, padx=10, pady=5)
    Entry(edit_win, textvariable=email_var).grid(row=4, column=1, padx=10, pady=5)
    Entry(edit_win, textvariable=addr_var).grid(row=5, column=1, padx=10, pady=5)

    def save_changes():
        cursor.execute("""
            UPDATE Customer
            SET FirstName = ?, LastName = ?, Email = ?, Mobile = ?, Address = ?
            WHERE CustomerID = ?
        """, (
            fn_var.get(),
            ln_var.get(),
            mobile_var.get(),
            email_var.get(),
            addr_var.get(),
            id_var.get()
        ))
        conn.commit()
        messagebox.showinfo("Success", f"Customer {id_var.get()} updated.")
        refresh_table()
        edit_win.destroy()

    Button(edit_win, text="Save", command=save_changes).grid(row=6, column=1, pady=10)

def on_edit_click():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Warning", "No row selected to edit.")
        return

    selected_item = selected_items[0]
    row_values = tree.item(selected_item, "values")
    if not row_values:
        messagebox.showerror("Error", "No data in selected row.")
        return

    # Convert the first column (row_values[0]) from something like "(4," to "4"
    raw_id = str(row_values[0]).strip()
    # If it looks like "(4," or "(5," etc., remove parentheses & comma
    if raw_id.startswith("(") and raw_id.endswith(","):
        raw_id = raw_id.replace("(", "").replace(")", "").replace(",", "").strip()

    # Now convert to integer
    numeric_id = int(raw_id)

    open_edit_window(numeric_id)


# 8. EDIT BUTTON (button_2.png)
button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_edit = Button(
    window,
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    relief="flat",
    command=on_edit_click
)
button_edit.place(x=106.0, y=380.0, width=47.0, height=46.0)

# 9. CONFIGURE THE SEARCH & DELETE BUTTON COMMANDS
button_1.config(command=on_search)
button_16.config(command=on_delete_click)

# 11. (Optional) ADD REFRESH BUTTON UNDER THE DELETE BUTTON
button_refresh = PhotoImage(file=relative_to_assets("button_refresh.png"))
refresh_btn = Button(
    window,
    image=button_refresh,
    borderwidth=0,
    highlightthickness=0,
    relief="flat",
    command=refresh_table
)
refresh_btn.place(x=1130.0, y=370.0, width=120.0, height=33.0)

# 11. Start the app
refresh_table()
window.mainloop()

