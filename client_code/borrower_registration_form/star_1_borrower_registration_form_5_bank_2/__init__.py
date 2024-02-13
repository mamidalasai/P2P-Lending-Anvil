from ._anvil_designer import star_1_borrower_registration_form_5_bank_2Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class star_1_borrower_registration_form_5_bank_2(star_1_borrower_registration_form_5_bank_2Template):
  def __init__(self,user_id, **properties):
    self.userId = user_id
    user_data=app_tables.fin_user_profile.get(customer_id=user_id)
    if user_data:
      self.text_box_1.text=user_data['bank_id']
      self.text_box_2.text=user_data['account_bank_branch']
      
      # Set Form properties and Data Bindings.
      self.init_components(**properties)
      self.accepted_terms = False
      self.button_2.enabled = False

  def button_2_click(self, **event_args):
    bank_id = self.text_box_1.text
    # salary_type = self.drop_down_1.selected_value
    bank_branch = self.text_box_2.text
    
    user_id = self.userId
    if not bank_id or not bank_branch:
      Notification("please fill all required fields").show()
    else:
      anvil.server.call('add_borrower_step9', bank_id,bank_branch, user_id)
      open_form('borrower_registration_form.dashboard')

  def button_1_click(self, **event_args):
    open_form('borrower_registration_form.star_1_borrower_registration_form_5_bank_1',user_id=self.userId)

  def button_3_click(self, **event_args):
    open_form("bank_users.user_form")

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert('Agreements, Privacy Policy and Applicant should accept following:Please note that any information concealed (as what we ask for), would be construed as illegitimate action on your part and an intentional attempt to hide material information which if found in future, would attract necessary action (s) at your sole cost. Hence, request to be truthful to your best knowledge while sharing your details)')

  def check_box_1_copy_2_change(self, **event_args):
        """This method is called when the check box is checked or unchecked"""
        self.accepted_terms = self.check_box_1_copy_2.checked
        self.button_2.enabled = self.accepted_terms

