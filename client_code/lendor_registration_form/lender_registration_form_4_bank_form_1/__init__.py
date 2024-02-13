from ._anvil_designer import lender_registration_form_4_bank_form_1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class lender_registration_form_4_bank_form_1(lender_registration_form_4_bank_form_1Template):
  def __init__(self,user_id, **properties):
    self.userId = user_id
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    user_data = anvil.server.call('get_user_data', user_id)
    if user_data:
            self.account_name = user_data.get('account_name', '')
            self.account_type = user_data.get('account_type', '')
            self.account_number = user_data.get('account_number', '')
            self.bank_name = user_data.get('bank_name', '')
            
    else:
        self.account_name = ''
        self.account_type = ''
        self.account_number = ''
        self.bank_name = ''
        

       #Restore previously entered data if available
    if self.account_name:
            self.text_box_1.text= self.account_name
    if self.account_type:
            self.drop_down_1.selected_value = self.account_type
    if self.account_number:
          self.text_box_2.text = self.account_number
    if self.bank_name:
           self.text_box_3.text = self.bank_name
      
    options = app_tables.fin_lendor_account_type.search()
    options_string =[str(option['lendor_account_type']) for option in options]
    self.drop_down_1.items = options_string
    # Any code you write here will run before the form opens.

  def button_2_click(self, **event_args):
    account_name = self.text_box_1.text
    account_type = self.drop_down_1.selected_value
    account_number = self.text_box_2.text
    bank_name = self.text_box_3.text
    user_id = self.userId
    if not account_name or not account_type or not account_number or not bank_name:
      Notification("please fill the all required fields").show()
    else:
      anvil.server.call('add_lendor_bank_details_form_1', account_name, account_type,account_number,bank_name, user_id)
      open_form('lendor_registration_form.lender_registration_form_4_bank_form_2',user_id=self.userId)

  def button_1_click(self, **event_args):
    user_id = self.userId
    open_form('lendor_registration_form.lender_registration_form_3_marital_details',user_id=self.userId)

  def button_3_click(self, **event_args):
    open_form("bank_users.user_form")
    
