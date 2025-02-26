import pandas as pd

class ticket_object:
    def __init__ (self, ticket_id, customer_id, employee_name, drop_off_date, finish_date, pickup_date, ticket_status, gun_manufacturer, gun_model, gun_serial_number, purchase_location, purchase_date, previous_repairs, work_description, additional_parts, additional_comments):
        self.ticket_id = ticket_id
        self.customer_id = customer_id
        self.employee_name = employee_name
        self.drop_off_date = drop_off_date
        self.finish_date = finish_date
        self.pickup_date = pickup_date
        self.ticket_status = ticket_status
        self.gun_manufacturer = gun_manufacturer
        self.gun_model = gun_model
        self.gun_serial_number = gun_serial_number
        self.purchase_location = purchase_location
        self.purchase_date = purchase_date
        self.previous_repairs = previous_repairs
        self.work_description = work_description
        self.additional_parts = additional_parts
        self.additional_comments = additional_comments

    def to_dict(self):
        return {
            "Ticket ID": self.ticket_id,
            "Customer ID": self.customer_id,
            "Employee Name": self.employee_name,
            "Drop Off Date": self.drop_off_date,
            "Finish Date": self.finish_date,
            "Pickup Date": self.pickup_date,
            "Ticket Status": self.ticket_status,
            "Gun Manufacturer": self.gun_manufacturer,
            "Gun Model": self.gun_model,
            "Gun Serial Number": self.gun_serial_number,
            "Purchase Location": self.purchase_location,
            "Purchase Date": self.purchase_date,
            "Previous Repairs": self.previous_repairs,
            "Work Description": self.work_description,
            "Additional Parts": self.additional_parts,
            "Additional Comments": self.additional_comments
        }
    
    def save_data(self, customer_object):
        df = pd.DataFrame([self.to_dict()])
        df.to_csv('ticket_data.csv', mode='a', index=False, encoding='utf-8', header=not pd.io.common.file_exists('ticket_data.csv'))