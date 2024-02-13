from ._anvil_designer import manage_dropdownsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class manage_dropdowns(manage_dropdownsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh()

  def refresh(self):
    """Refresh repeating panels with the latest data"""
    self.repeating_panel_1.items = app_tables.fin_gender.search()

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.repeating_panel_1.visible = False
    open_form('admin.dashboard.manage_cms.add_borrower_dropdown_details')

  def button_2_copy_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_02.visible = False
    open_form('admin.dashboard.manage_cms.add_lender_dropdown_details')

  def button_1_copy_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.manage_cms')

  def gender_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_data = self.text_box_01.text
    new_row = app_tables.fin_gender.add_row(gender=entered_data)
    self.text_box_01.text = ' '
    self.refresh()

  def gender_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_02.visible = True
    self.button_2.visible = False
    self.button_2_copy.visible = False
    
