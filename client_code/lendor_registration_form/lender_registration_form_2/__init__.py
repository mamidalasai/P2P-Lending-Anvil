from ._anvil_designer import lender_registration_form_2Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class lender_registration_form_2(lender_registration_form_2Template):
    def __init__(self, user_id, **properties):
        self.userId = user_id
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Initialize variables
        lending_type = None
        investment = None
        lending_period = None

        # Search for user_data in the lender table
        user_data = app_tables.fin_lender.search(customer_id = user_id)

        if user_data and len(user_data) > 0:
            lending_type = user_data[0]['lending_type']
            investment = user_data[0]['investment']
            lending_period = user_data[0]['lending_period']

        # Set selected values for dropdowns
        if lending_type:
            self.lending_type_dropdown.selected_value = lending_type
        if investment:
            self.text_box_1.text = investment  # No need to convert to string
        if lending_period:
            self.drop_down_2.selected_value = lending_period

        options = app_tables.fin_lendor_lending_type.search()
        options_string = [str(option['lendor_lending_type']) for option in options]
        self.lending_type_dropdown.items = options_string

        options = app_tables.fin_lendor_lending_period.search()
        options_string =[str(option['lendor_lending_period']) for option in options]
        self.drop_down_2.items = options_string
        # Any code you write here will run before the form opens.

    def button_1_click(self, **event_args):
        open_form('lendor_registration_form.lender_registration_form_1_education_form', user_id=self.userId)

    def button_2_click(self, **event_args):
        lending_type = self.lending_type_dropdown.selected_value
        investment = self.text_box_1.text
        lending_period = self.drop_down_2.selected_value
        user_id = self.userId

        # Check if user_data is not empty before accessing its elements
        if lending_type and investment and lending_period:
            # Search for existing user data in the lender table
            user_data = app_tables.fin_lender.search(customer_id = user_id)

            if user_data and len(user_data) > 0:
                # If the row exists, update the existing row
                user_row = user_data[0]
                user_row['lending_type'] = lending_type
                user_row['investment'] = int(investment)
                user_row['lending_period'] = lending_period
                user_row['membership'] = self.calculate_membership(float(investment))
                user_row.update()
            else:
                # If the row doesn't exist, add a new row
                app_tables.fin_lender.add_row(customer_id = user_id, lending_type=lending_type, investment=int(investment), lending_period=lending_period, membership=self.calculate_membership(float(investment)))

            if lending_type == 'Individual':
                open_form('lendor_registration_form.lender_registration_form_2.lender_registration_individual_form_1', user_id=user_id)
            elif lending_type == 'Institutional':
                open_form('lendor_registration_form.lender_registration_form_2.lender_registration_Institutional_form_1', user_id=user_id)

    def button_3_click(self, **event_args):
        open_form("bank_users.user_form")

    # Function to calculate membership based on investment
    def calculate_membership(self, investment):
        if investment <= 500000:
            return 'Silver'
        elif investment <= 1000000:
            return 'Gold'
        else:
            return 'Platinum'

    
