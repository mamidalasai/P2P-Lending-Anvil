from ._anvil_designer import ItemTemplate48Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate48(ItemTemplate48Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    selected_row = self.item
        # Open the Borr_loan_request form with the selected row data
    open_form("lendor_registration_form.dashboard.view_borrower_loan_request.Borr_loan_request", selected_row=selected_row)
