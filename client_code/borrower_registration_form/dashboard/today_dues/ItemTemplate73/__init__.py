from ._anvil_designer import ItemTemplate73Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate73(ItemTemplate73Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    selected_row = self.item
    open_form('borrower_registration_form.dashboard.today_dues.payment_details_t', selected_row = selected_row)

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    selected_row = self.item
    open_form('borrower_registration_form.dashboard.today_dues.check_out', selected_row = selected_row)
    
