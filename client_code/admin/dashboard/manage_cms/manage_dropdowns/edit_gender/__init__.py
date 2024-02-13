from ._anvil_designer import edit_genderTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class edit_gender(edit_genderTemplate):
  def __init__(self,selected_row, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.text_box_1.text = selected_row['gender']
        # Store the selected row for later use
    self.selected_row = selected_row
    
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Get the updated gender from the textbox
    updated_gender = self.text_box_01.text

        # Update the 'borrower_gender' field in the database
    self.selected_row['gender'] = updated_gender
    self.selected_row.update()
        # Close the form
    alert("Changes saved successfully!")
    open_form('admin.dashboard.manage_cms.manage_dropdowns')

  def delete_button(self, **event_args):
    """This method is called when the button is clicked"""
    confirmation = alert(
            "Are you sure you want to delete this data?",
            title="Confirm Deletion",
            buttons=[("Cancel", False), ("Delete", True)],
        )
    if confirmation:
            # Get the name of the group to be deleted
            group_name = self.selected_row['gender']

            # Delete the rows from the product_group table
            self.selected_row.delete()
            open_form('admin.dashboard.manage_cms.manage_dropdowns')

  def home_button(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard')

  def button_1_copy_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.manage_cms.manage_dropdowns')
