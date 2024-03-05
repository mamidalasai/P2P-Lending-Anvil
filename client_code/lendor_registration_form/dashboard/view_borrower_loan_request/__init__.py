from ._anvil_designer import view_borrower_loan_requestTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import lendor_main_form_module as main_form_module
from ....bank_users.main_form import main_form_module as main_module

class view_borrower_loan_request(view_borrower_loan_requestTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user_id=main_module.userId
    user_id = self.user_id
    self.email = main_module.email
    email = self.email
    
    
    self.repeating_panel_2.items=app_tables.fin_loan_details.search(loan_updated_status="under process")
    
    anvil.server.call('transfer_user_profile_to_loan_details', email,self.user_id) 

  
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard")
