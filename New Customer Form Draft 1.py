import tkinter as tk
from tkinter import ttk
import pandas as pd
import re
from tkinter import messagebox

class CustomerObject:
    def __init__(self, customerID, first_name, last_name, email, phone_number, address, address2, city, state, zipcode):
        self.customerID = customerID
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.address2 = address2
        self.city = city
        self.state = state
        self.zipcode = zipcode
    
    def to_dict(self):
        return {
            "Customer ID": self.customerID,
            "First Name": self.first_name,
            "Last Name": self.last_name,
            "Email": self.email,
            "Phone Number": self.phone_number,
            "Address": self.address,
            "Address 2": self.address2,
            "City": self.city,
            "State": self.state,
            "Zipcode": self.zipcode
        }

class CustomerForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Form")

        self.frame = tk.Frame(root)
        self.frame.pack(padx=20, pady=20)

        self.cust_info_frame = tk.Frame(self.frame)
        self.cust_info_frame.grid(row=0, column=0, columnspan=2)

        labels = ["First Name", "Last Name", "Email", "Mobile", "Address", "Address 2", "City", "State", "Zipcode"]
        self.entries = {}

        # List of US states
        self.states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA",
                       "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                       "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT",
                       "VA", "WA", "WV", "WI", "WY"]

        for i, label in enumerate(labels):
            tk.Label(self.cust_info_frame, text=label).grid(row=i//2 * 2, column=i%2)
            if label == "State":
                self.state_var = tk.StringVar()
                self.entries[label] = ttk.Combobox(self.cust_info_frame, textvariable=self.state_var, values=self.states)
                self.entries[label].bind("<KeyRelease>", self.filter_states)  # Bind event for autofill
            else:
                self.entries[label] = tk.Entry(self.cust_info_frame)

            self.entries[label].grid(row=i//2 * 2 + 1, column=i%2)

        for widget in self.cust_info_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        self.clear_button = tk.Button(self.frame, text="Clear", font=22, command=self.reset_form)
        self.clear_button.grid(row=3, column=1, padx=20, pady=10)

        self.save_button = tk.Button(self.frame, text="Save", font=22, bg="lime green", command=self.save_data)
        self.save_button.grid(row=3, column=2, padx=20, pady=10)

    def filter_states(self, event):
        """Filters the state dropdown based on user input."""
        typed_text = self.state_var.get().upper()
        if typed_text:
            filtered_states = [state for state in self.states if state.startswith(typed_text)]
            self.entries["State"]["values"] = filtered_states  # Update combobox options

    def reset_form(self):
        for key, widget in self.entries.items():
            if isinstance(widget, tk.Entry):
                widget.delete(0, 'end') 
            if isinstance(widget, ttk.Combobox):
                widget.set('')

    def generate_customer_id(self, last_name, mobile):
        last_name_part = last_name[:3].upper() if last_name else "XXX"
        mobile_part = mobile[-4:] if mobile else "0000"
        return f"{last_name_part}{mobile_part}"

    def validate_data(self):
        """Validates the data entered in the form."""
        
        # First Name and Last Name
        if not self.entries["First Name"].get().strip():
            messagebox.showerror("Invalid Input", "First Name cannot be empty.")
            return False
        
        if not self.entries["Last Name"].get().strip():
            messagebox.showerror("Invalid Input", "Last Name cannot be empty.")
            return False
        
        # Email Validation (simple regex for email format)
        email = self.entries["Email"].get().strip()
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Invalid Input", "Please enter a valid email address.")
            return False
        
        # Phone Number Validation (allow dashes)
        phone_number = self.entries["Mobile"].get().strip()
        # Remove dashes and check that we have 10 digits
        phone_digits = phone_number.replace('-', '')
        if not phone_digits.isdigit() or len(phone_digits) != 10:
            messagebox.showerror("Invalid Input", "Please enter a valid 10-digit phone number (dashes are allowed).")
            return False
        
        # Address Validation
        if not self.entries["Address"].get().strip():
            messagebox.showerror("Invalid Input", "Address cannot be empty.")
            return False
        
        # Zipcode Validation (only digits and length should be 5)
        zipcode = self.entries["Zipcode"].get().strip()
        if not zipcode.isdigit() or len(zipcode) != 5:
            messagebox.showerror("Invalid Input", "Please enter a valid 5-digit zipcode.")
            return False
        
        # State Validation (must be selected)
        if not self.entries["State"].get():
            messagebox.showerror("Invalid Input", "Please select a state.")
            return False
        
        return True

    def save_data(self):
        """Validates data before saving it."""
        if not self.validate_data():
            return  # Stop the save process if validation fails

        # Generate Customer ID
        customer_id = self.generate_customer_id(self.entries["Last Name"].get(), self.entries["Mobile"].get())
        
        # Create CustomerObject
        customer = CustomerObject(
            customer_id,
            self.entries["First Name"].get(),
            self.entries["Last Name"].get(),
            self.entries["Email"].get(),
            self.entries["Mobile"].get(),
            self.entries["Address"].get(),
            self.entries["Address 2"].get(),
            self.entries["City"].get(),
            self.entries["State"].get(),
            self.entries["Zipcode"].get()
        )

        # Save the data
        df = pd.DataFrame([customer.to_dict()])
        df.to_csv('customer_data.csv', mode='a', index=False, encoding='utf-8', header=not pd.io.common.file_exists('customer_data.csv'))
        messagebox.showinfo("Success", "Customer data saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerForm(root)
    root.mainloop()
