import csv
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox

def create_work_orders():
    root = tk.Tk()
    root.withdraw()
    
    while True:
        work_order = {
            "Order Number": simpledialog.askstring("Input", "Enter Order Number:"),
            "Pickup Date": simpledialog.askstring("Input", "Enter Pickup Date (YYYY-MM-DD):"),
            "Received by": simpledialog.askstring("Input", "Received by:"),
            "Drop off Date": simpledialog.askstring("Input", "Enter Drop off Date (YYYY-MM-DD):"),
            "Customer Name": simpledialog.askstring("Input", "Customer Name:"),
            "Gun Manufacturer": simpledialog.askstring("Input", "Gun Manufacturer:"),
            "Model": simpledialog.askstring("Input", "Gun Model:"),
            "S/N": simpledialog.askstring("Input", "Serial Number:"),
            "Condition": simpledialog.askstring("Input", "Condition of Gun:"),
            "Purchase Details": simpledialog.askstring("Input", "When and where was the gun purchased?"),
            "Previous Upgrades/Repairs": simpledialog.askstring("Input", "List any previous upgrades or repairs:"),
            "Parts & Extras Left": simpledialog.askstring("Input", "All parts and extras left with the gun:"),
            "Work Description": simpledialog.askstring("Input", "Work Description:"),
            "Additional Comments": simpledialog.askstring("Input", "Additional Comments:")
        }
        
        save_to_csv(work_order)
        
        more_entries = messagebox.askyesno("Continue", "Do you want to add another work order?")
        if not more_entries:
            break
    
    messagebox.showinfo("Success", "All work orders have been created successfully!")

def save_to_csv(work_order, filename="work_orders.csv"):
    file_exists = False
    try:
        with open(filename, "r") as file:
            file_exists = True
    except FileNotFoundError:
        pass
    
    with open(filename, "a", newline='') as file:
        fieldnames = work_order.keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()  # Write header only if file does not exist
        
        writer.writerow(work_order)

if __name__ == "__main__":
    create_work_orders()