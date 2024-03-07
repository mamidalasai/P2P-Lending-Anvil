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
    self.repeating_panel_1.items = app_tables.fin_admin_beseem_categories.search(group_name="gender")
    self.repeating_panel_2.items = app_tables.fin_admin_beseem_categories.search(group_name="qualification")
    self.repeating_panel_3.items = app_tables.fin_admin_beseem_categories.search(group_name="marrital_status")
    
  def gender_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_sub = self.text_box_1.text
    entered_min_pts = int(self.text_box_2.text)
    new_row = app_tables.fin_admin_beseem_categories.add_row(group_name='gender',sub_category=entered_sub,min_points=entered_min_pts)
    self.text_box_1.text = ' '
    self.text_box_2.text = ' '
    self.refresh()

    existing_min_points = [row["min_points"] for row in app_tables.fin_admin_beseem_categories.search(group_name='gender')]

    max_points = max(existing_min_points + [entered_min_pts])

    existing_group_row  = app_tables.fin_admin_beseem_groups.get(group_name="gender")
    if existing_group_row:
      existing_group_row['max_points'] = max_points
      existing_group_row.update()

    else:
      new_group_row = app_tables.fin_admin_beseem_groups.add_row(
            group_name="gender", max_points=max_points
        )

  def qualification_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_sub = self.text_box_3.text
    entered_min_pts = int(self.text_box_4.text)
    new_row = app_tables.fin_admin_beseem_categories.add_row(group_name='qualification',sub_category=entered_sub,min_points=entered_min_pts)
    self.text_box_3.text = ' '
    self.text_box_4.text = ' '
    self.refresh()

    existing_min_points = [row["min_points"] for row in app_tables.fin_admin_beseem_categories.search(group_name='qualification')]

    max_points = max(existing_min_points + [entered_min_pts])

    existing_group_row  = app_tables.fin_admin_beseem_groups.get(group_name="qualification")
    if existing_group_row:
      existing_group_row['max_points'] = max_points
      existing_group_row.update()

    else:
      new_group_row = app_tables.fin_admin_beseem_groups.add_row(
            group_name="qualification", max_points=max_points
        )

  def marrital_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_sub = self.text_box_5.text
    entered_min_pts = int(self.text_box_6.text)
    new_row = app_tables.fin_admin_beseem_categories.add_row(group_name='marrital_status',sub_category=entered_sub,min_points=entered_min_pts)
    self.text_box_5.text = ' '
    self.text_box_4.text = ' '
    self.refresh()

    existing_min_points = [row["min_points"] for row in app_tables.fin_admin_beseem_categories.search(group_name='marrital_status')]

    max_points = max(existing_min_points + [entered_min_pts])

    existing_group_row  = app_tables.fin_admin_beseem_groups.get(group_name="marrital_status")
    if existing_group_row:
      existing_group_row['max_points'] = max_points
      existing_group_row.update()

    else:
      new_group_row = app_tables.fin_admin_beseem_groups.add_row(
            group_name="marrital_status", max_points=max_points
        )
  
  def gender_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.grid_panel_1.visible = True
    self.grid_panel_2.visible = False
    self.grid_panel_3.visible = False

  def qualification_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.grid_panel_1.visible = False
    self.grid_panel_2.visible = True
    self.grid_panel_3.visible = False

  def marrital_status_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.grid_panel_1.visible = False
    self.grid_panel_2.visible = False
    self.grid_panel_3.visible = True
