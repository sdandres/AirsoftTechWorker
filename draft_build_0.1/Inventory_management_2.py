import csv
import tkinter as tk
from tkinter import ttk

# Constants for easy configuration
CSV_FILE = "inventory.csv"
ITEM_FIELDS = {
    "description": "ItemDescription",
    "location": "Location",
    "reorder": "ReorderLevel",
    "quantity": "Quantity",
    "sku": "SKU"
}

def search_inventory(entry_widget, output_widget):
    """
    Search for an item in the inventory CSV and display results or error messages
    vertically in the output widget: Item Description, Location, Reorder Level,
    Quantity, SKU Number (one per line).
    
    Parameters:
        entry_widget: Tkinter Entry widget for user input.
        output_widget: Tkinter Text widget for displaying results or errors.
    """
    # Clear the output widget
    output_widget.delete(1.0, "end")
    
    # Get the item name from the entry widget (case-insensitive)
    item_name = entry_widget.get().strip().lower()
    
    if not item_name:
        output_widget.insert("end", "Error: Please enter an item name to search.\n")
        return

    try:
        # Open and read the CSV file
        with open(CSV_FILE, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            item_found = False
            
            # Search for the item by description
            for row in reader:
                if row[ITEM_FIELDS["description"]].lower() == item_name:
                    item_found = True
                    # Display results vertically, one field per line, with a small separator for clarity
                    output_widget.insert("end", "Item Description: " + row[ITEM_FIELDS["description"]] + "\n")
                    output_widget.insert("end", "Location: " + row[ITEM_FIELDS["location"]] + "\n")
                    output_widget.insert("end", "Reorder Level: " + row[ITEM_FIELDS["reorder"]] + "\n")
                    output_widget.insert("end", "Quantity: " + row[ITEM_FIELDS["quantity"]] + "\n")
                    output_widget.insert("end", "SKU Number: " + row[ITEM_FIELDS["sku"]] + "\n")
                    break
            
            # If item not found, display error vertically
            if not item_found:
                output_widget.insert("end", "Error: Item not found in inventory.\n")

    except FileNotFoundError:
        output_widget.insert("end", f"Error: Could not find {CSV_FILE}. Please ensure the file exists.\n")
    except Exception as e:
        output_widget.insert("end", f"Error: An unexpected error occurred - {str(e)}\n")

def create_gui():
    """
    Create a simple Tkinter GUI matching the Figma design for inventory search.
    """
    # Create the main window
    root = tk.Tk()
    root.title("Inventory Management System")
    root.geometry("600x400")  # Approximate size based on the Figma design
    
    # Styling to match the Figma design (blue and white theme)
    root.configure(bg="#1E3A8A")  # Dark blue background
    
    # Navigation bar (simulating the top bar in the Figma design)
    nav_frame = tk.Frame(root, bg="#3B82F6", height=60)  # Light blue for navigation
    nav_frame.pack(fill="x")
    
    nav_buttons = [
        ("Home", "\u2302"),  # House icon (Unicode)
        ("Onboarding", "\uFF0B"),  # Plus icon (Unicode)
        ("New Ticket", "\u270E"),  # Pencil icon (Unicode)
        ("Customers", "\uD83D\uDC65"),  # People icon (Unicode)
        ("Tickets", "\uD83D\uDCDC"),  # Clipboard icon (Unicode)
        ("Inventory", "\uD83D\uDCCA")  # Chart icon (Unicode)
    ]
    
    for text, icon in nav_buttons:
        btn = tk.Button(nav_frame, text=f"{icon} {text}", bg="#3B82F6", fg="white", relief="flat")
        btn.pack(side="left", padx=10, pady=10)
    
    # Search frame
    search_frame = tk.Frame(root, bg="white", padx=20, pady=20)
    search_frame.pack(fill="both", expand=True)
    
    # Search entry field
    search_label = tk.Label(search_frame, text="Search Inventory", bg="white", font=("Arial", 12))
    search_label.pack(pady=(0, 5))
    
    entry = tk.Entry(search_frame, width=40, font=("Arial", 12))
    entry.pack(pady=(0, 10))
    
    # Search button
    search_btn = tk.Button(search_frame, text="🔍", command=lambda: search_inventory(entry, output_text),
                          bg="#3B82F6", fg="white", font=("Arial", 12), relief="flat")
    search_btn.pack(pady=(0, 10))
    
    # Output text box
    output_text = tk.Text(search_frame, height=10, width=50, font=("Arial", 12), bg="white")
    output_text.pack(pady=(10, 0))
    
    # Bind Enter key to search
    root.bind('<Return>', lambda event: search_inventory(entry, output_text))
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
