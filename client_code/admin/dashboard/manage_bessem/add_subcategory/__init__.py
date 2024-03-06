from ._anvil_designer import add_subcategoryTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class add_subcategory(add_subcategoryTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh()

    # Any code you write here will run before the form opens.

  def refresh(self):
    """Refresh repeating panels with the latest data"""
    self.repeating_panel_1.items = app_tables.fin_admin_beseem_categories.search()
    
  def gender_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_sub = self.text_box_1.text
    entered_min_pts = int(self.text_box_2.text)
    new_row = app_tables.fin_admin_beseem_categories.add_row(group_name='gender',sub_category=entered_sub,min_points=entered_min_pts)
    self.text_box_1.text = ' '
    self.text_box_2.text = ' '
    self.refresh()

    existing_min_points = [row["min_points"] for row in app_tables.fin_admin_beseem_categories.search()]

    max_points = max(existing_min_points + [entered_min_pts])

    new_row = app_tables.fin_admin_beseem_groups.add_row(
        group_name="gender", max_points=max_points
    )

            
      

  def gender_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.grid_panel_1.visible = True

  def qualification_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.grid_panel_1.visible = False

  def marrital_status_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.grid_panel_1.visible = False

  

  
