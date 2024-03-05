from ._anvil_designer import view_bessemTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class view_bessem(view_bessemTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.fetch_data()

  def fetch_data(self):
    self.data = app_tables.fin_admin_beseem_groups.search()
    if not self.data:
        Notification("No Data Available Here!").show()
    else:
        self.result = [{'group_name': i['group_name'],
                        'sub_category': i['sub_category'],
                        'min_points': i['min_points'],
                        'max_points': i['max_points']}
                       for i in self.data]
        self.repeating_panel_1.items = self.result

  def back_btn_click(self, **event_args):
    open_form('admin.dashboard.manage_bessem')
