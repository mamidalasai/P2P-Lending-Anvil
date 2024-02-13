from ._anvil_designer import ItemTemplate3Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate3(ItemTemplate3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def link_01_click(self, **event_args):
    """This method is called when the link is clicked"""
    item_data = self.item
    open_form('admin.dashboard.manage_cms.manage_dropdowns.edit_gender', selected_row=item_data)
    
