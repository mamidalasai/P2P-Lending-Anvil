from ._anvil_designer import lender_registration_form_3_marital_detailsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class lender_registration_form_3_marital_details(lender_registration_form_3_marital_detailsTemplate):
  def __init__(self,user_id, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.userId = user_id
    user_data=app_tables.fin_user_profile.get(customer_id=user_id)
    if user_data:
      self.marital_status_lender_registration_dropdown.selected_value=user_data['marital_status']
      user_data.update()

    options = app_tables.fin_lendor_marrital_status.search()
    options_string = [str(option['lendor_marrital_status']) for option in options]
    self.marital_status_lender_registration_dropdown.items = options_string
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  # def home_borrower_registration_form_copy_1_click(self, **event_args):
  #   open_form('bank_users.user_form')

  def button_next_click(self, **event_args):
    marital_status = self.marital_status_lender_registration_dropdown.selected_value
    user_id = self.userId
    if not marital_status or marital_status not in ['Not Married', 'Married', 'Other']:
      Notification("Please select a valid marital status").show()
    else:
      anvil.server.call('add_lendor_marital',marital_status,user_id)
      if marital_status == 'Not Married':
        open_form('lendor_registration_form.lender_registration_form_3_marital_details.lender_registration_form_3_marital_married',user_id = user_id)
      elif marital_status == 'Married':
        open_form('lendor_registration_form.lender_registration_form_3_marital_details.lender_registration_form_3_marital_married',user_id = user_id)
      else:
        open_form('lendor_registration_form.lender_registration_form_4_bank_form_1',user_id = user_id)

  def button_1_click(self, **event_args):
    open_form('lendor_registration_form.lender_registration_form_2',user_id=self.userId)
    # Any code you write here will run before the form opens.

  def marital_status_borrower_registration_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    pass
