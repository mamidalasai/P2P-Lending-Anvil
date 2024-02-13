from ._anvil_designer import RowTemplate10Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
from anvil import open_form


class RowTemplate10(RowTemplate10Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        

    # Any code you write here will run before the form opens.

    def button_1_click(self, **event_args):
      """This method is called when the button is clicked"""
      # Get the selected row data
      selected_row = self.item
      

        # Open the Borr_loan_request form with the selected row data
      open_form("lendor_registration_form.dashboard.view_borrower_loan_request.Borr_loan_request", selected_row=selected_row)