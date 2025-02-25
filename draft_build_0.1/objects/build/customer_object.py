class customer_object:
    def __init__ (self, customerID, first_name, last_name, email, phone_number, address, address2, city, state, zipcode):
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

def save_data(self, customer_object):
    df = pd.DataFrame([self.to_dict()])
    df.to_csv('customer_data.csv', mode='a', index=False, encoding='utf-8', header=not pd.io.common.file_exists('customer_data.csv'))
