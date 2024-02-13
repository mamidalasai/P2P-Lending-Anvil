from ._anvil_designer import lender_registration_Institutional_form_2Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class lender_registration_Institutional_form_2(lender_registration_Institutional_form_2Template):
  def __init__(self, user_id,**properties):
    self.userId = user_id
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    user_data = anvil.server.call('get_user_data', user_id)
        
    if user_data:
            self.nearest_loc = user_data.get('nearest_location', '')
            self.business_type = user_data.get('business_type', '')
            self.empolyees_working = user_data.get('employees_working', '')
            self.year = user_data.get('year_estd', '')
            
            
    else:
        self.nearest_loc = ''
        self.business_type = ''
        self.empolyees_working = ''
        self.year = ''
        

       #Restore previously entered data if available
    if self.nearest_loc:
            self.text_box_1.text= self.nearest_loc
    if self.business_type:
            self.drop_down_1.selected_value = self.business_type
    if self.empolyees_working:
           self.drop_down_2.selected_value = self.empolyees_working
    if self.year:
           self.date_picker_1.date = self.year

    options = app_tables.fin_lendor_business_type.search()
    options_string = [str(option['lendor_business_type']) for option in options]
    self.drop_down_1.items = options_string

    options = app_tables.fin_lendor_no_of_employees.search()
    options_string = [str(option['lendor_no_of_employees']) for option in options]
    self.drop_down_2.items = options_string


    # Any code you write here will run before the form opens.

  def button_2_click(self, **event_args):
    nearest_loc = self.text_box_1.text
    business_type = self.drop_down_1.selected_value
    empolyees_working = self.drop_down_2.selected_value
    year = self.date_picker_1.date
    user_id = self.userId
    if not nearest_loc or not business_type or not empolyees_working or not year:
      Notification("Please fill all the fields")
    else:
     anvil.server.call('add_lendor_institutional_form_2',nearest_loc,business_type,empolyees_working,year,user_id)
     open_form('lendor_registration_form.lender_registration_form_2.lender_registration_Institutional_form_3',user_id = user_id)
    """This method is called when the button is clicked"""

  def button_1_click(self, **event_args):
    user_id = self.userId
    open_form('lendor_registration_form.lender_registration_form_2.lender_registration_Institutional_form_1',user_id = user_id)
    """This method is called when the button is clicked"""

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("bank_users.user_form")
    
