from ._anvil_designer import lender_registration_form_1_education_formTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class lender_registration_form_1_education_form(lender_registration_form_1_education_formTemplate):
  def __init__(self,user_id, **properties):
    self.userId = user_id
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    user_data = anvil.server.call('get_user_data', user_id)
    
    options = app_tables.fin_lendor_qualification.search()
    options_string = [str(option['lendor_qualification']) for option in options]
    self.drop_down_1.items = options_string

    # Any code you write here will run before the form opens.

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    qualification = self.drop_down_1.selected_value
    user_id = self.userId
    if qualification == '10th class':
      open_form('lendor_registration_form.lender_registration_form_1_education_form.lender_registration_education_10th_class',user_id=user_id)
    elif qualification == 'Intermediate / PUC':
      open_form('lendor_registration_form.lender_registration_form_1_education_form.lender_registration_education_Intermediate',user_id = user_id)
    elif qualification == 'Btech / B.E':
      open_form('lendor_registration_form.lender_registration_form_1_education_form.lender_registration_education_Btech',user_id=user_id)
    elif qualification == 'Mtech':
      open_form('lendor_registration_form.lender_registration_form_1_education_form.lender_registration_education_Mtech',user_id = user_id)
    else:
      qualification == 'Phd'
      open_form('lendor_registration_form.lender_registration_form_1_education_form.lender_registration_education_Phd',user_id=user_id)

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("bank_users.user_form")
    

  
   