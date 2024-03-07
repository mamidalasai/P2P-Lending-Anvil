from ._anvil_designer import star_1_borrower_registration_form_1_educationTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class star_1_borrower_registration_form_1_education(star_1_borrower_registration_form_1_educationTemplate):
  def __init__(self,user_id, **properties):
    self.userId = user_id
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # user_data = anvil.server.call('get_user_data', user_id)
    user_data = app_tables.fin_user_profile.get(customer_id=user_id)
    if user_data:
      self.drop_down_1.selected_value = user_data['qualification']
      user_data.update()
    options = app_tables.fin_borrower_qualification.search()
    options_string = [str(option['borrower_qualification']) for option in options]
    self.drop_down_1.items = options_string


    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    user_id = self.userId
    # open_form('lendor_registration_form.Lender_reg_form_2',user_id=user_id)
    """This method is called when the button is clicked"""

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    qualification = self.drop_down_1.selected_value
    user_id = self.userId
    if qualification not in  ['10th Class','Intermediate / PUC','Btech / B.E','Mtech','Phd']:
      Notification("Please select a valid qualification status").show()
    elif not user_id:
      Notification("User ID is missing").show()
    else:
      anvil.server.call('add_borrower_step1',qualification,user_id)
    
    if qualification == '10th Class':
      open_form('borrower_registration_form.star_1_borrower_registration_form_1_education.star_1_borrower_registration_form_education_10th_class',user_id=user_id)
    elif qualification == 'Intermediate / PUC':
      open_form('borrower_registration_form.star_1_borrower_registration_form_1_education.star_1_borrower_registration_form_education_intermediate',user_id = user_id)
    elif qualification == 'Btech / B.E':
      open_form('borrower_registration_form.star_1_borrower_registration_form_1_education.star_1_borrower_registration_form_education_btech',user_id=user_id)
    elif qualification == 'Mtech':
      open_form('borrower_registration_form.star_1_borrower_registration_form_1_education.star_1_borrower_registration_form_education_mtech',user_id = user_id)
    elif qualification == 'Phd':
      open_form('borrower_registration_form.star_1_borrower_registration_form_1_education.star_1_borrower_registration_form_education_phd',user_id=user_id)
    else:
      open_form('borrower_registration_form.star_1_borrower_registration_form_1_education',user_id=user_id)
      # alert('Please select a valid qualification')

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("bank_users.user_form")

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    pass

