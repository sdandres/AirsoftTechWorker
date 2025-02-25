import csv

def search_inventory(entry_widget, output_widget):
    """
    Search for an item in the inventory CSV and display results vertically in the output widget.
    
    Parameters:
        entry_widget: The Tkinter Entry widget where the user types the item name.
        output_widget: The Tkinter Text widget where results or errors are shown.
    """
    # Clear the output widget
    output_widget.delete(1.0, "end")
    
    # Get the item name from the entry widget
    item_name = entry_widget.get().lower()  # Case-insensitive search
    
    # Path to the CSV file (easy to change if needed)
    csv_file = "inventory.csv"
    
    # Column names in the CSV (modify these if your CSV uses different headers)
    description_key = "ItemDescription"
    location_key = "Location"
    reorder_key = "ReorderLevel"
    quantity_key = "Quantity"
    sku_key = "SKU"
    
    try:
        with open(csv_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row[description_key].lower() == item_name:
                    # List items vertically, one per line
                    output_widget.insert("end", f"Item Description: {row[description_key]}\n")
                    output_widget.insert("end", f"Location: {row[location_key]}\n")
                    output_widget.insert("end", f"Reorder Level: {row[reorder_key]}\n")
                    output_widget.insert("end", f"Quantity: {row[quantity_key]}\n")
                    output_widget.insert("end", f"SKU Number: {row[sku_key]}\n")
                    return  # Stop once found
            # If not found
            output_widget.insert("end", "Error: Item not found in inventory.\n")
    except FileNotFoundError:
        output_widget.insert("end", f"Error: Could not find {csv_file}.\n")
    except Exception as e:
        output_widget.insert("end", f"Error: {str(e)}\n")
