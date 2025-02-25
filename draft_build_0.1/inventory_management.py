from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)

# Specify the path to your CSV file
CSV_FILE_PATH = 'inventory.csv'

def load_inventory():
    """Read the CSV file and return the data"""
    inventory = []
    if os.path.exists(CSV_FILE_PATH):
        with open(CSV_FILE_PATH, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                inventory.append(row)
    return inventory

@app.route('/search_item', methods=['POST'])
def search_item():
    # Get the item name from the request
    item_name = request.json.get('item_name', '').lower()
    
    # Load inventory from CSV
    inventory = load_inventory()
    
    # Search for the item in inventory
    for item in inventory:
        if item['item_name'].lower() == item_name:
            # Format the output string in the requested order
            result = f"{item['description']}\n" \
                    f"{item['location']}\n" \
                    f"{item['reorder_level']}\n" \
                    f"{item['quantity']}\n" \
                    f"{item['sku']}"
            return jsonify({
                'success': True,
                'result': result
            })
    
    # If item not found
    return jsonify({
        'success': False,
        'error': 'Item not found in inventory'
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)