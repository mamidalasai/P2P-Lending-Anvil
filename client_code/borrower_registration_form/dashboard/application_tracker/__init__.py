from ._anvil_designer import application_trackerTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import main_form_module as main_form_module

class application_tracker(application_trackerTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user_id=main_form_module.userId
    
    # Any code you write here will run before the form oopens.
    under_process_items = app_tables.fin_loan_details.search(loan_updated_status=q.like('under proces%'), borrower_customer_id=self.user_id)
    self.repeating_panel_2.items = under_process_items
    #self.label_1.text = str(len(under_process_items))

    approved_items = app_tables.fin_loan_details.search(loan_updated_status=q.like('approve%'), borrower_customer_id=self.user_id)
    self.repeating_panel_3.items = approved_items
    #self.label_2.text = str(len(approved_items))      
  
  def home_borrower_registration_button_click(self, **event_args):
    open_form('borrower_registration_form.dashboard')

  def borrower_dashboard_home_linkhome_borrower_registration_button_copy_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

