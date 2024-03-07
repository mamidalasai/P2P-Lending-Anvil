from ._anvil_designer import view_loan_extension_requestsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class view_loan_extension_requests(view_loan_extension_requestsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
      
    self.repeating_panel_6.items=app_tables.fin_extends_loan.search()

    self.repeating_panel_7.items = app_tables.fin_extends_loan.search(status=q.like('approved%'))
    self.label_5.text = str(len(self.repeating_panel_7.items))

    self.repeating_panel_8.items = app_tables.fin_extends_loan.search(status=q.like('rejected%'))
    self.label_6.text = str(len(self.repeating_panel_8.items))

    self.repeating_panel_9.items = app_tables.fin_extends_loan.search(status=q.like('under process%'))
    self.label_5_copy.text = str(len(self.repeating_panel_9.items))

    self.repeating_panel_5.items = app_tables.fin_extends_loan.search(status=q.like('under process%'))
    self.new_request.text = str(len(self.repeating_panel_5.items))

    self.all.text = str(len(self.repeating_panel_6.items))
    
  
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard")

  
  


  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_2.visible = True
    #self.data_grid_2.visible = True
    self.label_3.visible = False
    self.data_grid_2_copy.visible = False
    self.label_4.visible = False
    self.data_grid_3.visible = False
    self.new.visible = False
    self.data_grid_4.visible = False
    self.label_1.visible = False
    self.data_grid_4_copy.visible = False
    self.repeating_panel_5.visible = True
    self.repeating_panel_6.visible = False
    self.repeating_panel_7.visible =True
    self.repeating_panel_8.visible = False
    self.repeating_panel_9.visible = False


  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_3.visible = True
   # self.data_grid_2_copy.visible = True
    self.label_4.visible = False
    self.data_grid_3.visible = False
    self.label_2.visible = False
    self.data_grid_2.visible = False
    self.new.visible = False
    self.data_grid_4.visible = False
    self.label_1.visible = False
    self.data_grid_4_copy.visible = False
    self.repeating_panel_5.visible = False
    self.repeating_panel_6.visible = False
    self.repeating_panel_7.visible =False
    self.repeating_panel_8.visible = True
    self.repeating_panel_9.visible = False

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_4.visible = True
   # self.data_grid_3.visible = True
    self.label_2.visible = False
    self.data_grid_2.visible = False
    self.label_3.visible = False
    self.data_grid_2_copy.visible = False
    self.new.visible = False
    self.data_grid_4.visible = False
    self.label_1.visible = False
    self.data_grid_4_copy.visible = False
    self.repeating_panel_5.visible = False
    self.repeating_panel_6.visible = False
    self.repeating_panel_7.visible =False
    self.repeating_panel_8.visible = False
    self.repeating_panel_9.visible = True

  def button_5_click(self, **event_args):
    """This method is called when the button is clicked"""
    # self.data_grid_1.visible = not self.data_grid_1.visible
    self.new.visible = True
    #self.data_grid_4.visible = True
    self.label_4.visible = False
    self.data_grid_3.visible = False
    self.label_2.visible = False
    self.data_grid_2.visible = False
    self.label_3.visible = False
    self.data_grid_2_copy.visible = False
    self.label_1.visible = False
    self.data_grid_4_copy.visible = False
    self.repeating_panel_5.visible = True
    self.repeating_panel_6.visible = False
    self.repeating_panel_7.visible =False
    self.repeating_panel_8.visible = False
    self.repeating_panel_9.visible = False

  def button_6_click(self, **event_args):
    """This method is called when the button is clicked"""
    #self.data_grid_4_copy.visible = True
    self.label_1.visible = True
    self.label_4.visible = False
    self.data_grid_3.visible = False
    self.label_2.visible = False
    self.data_grid_2.visible = False
    self.label_3.visible = False
    self.data_grid_2_copy.visible = False
    self.new.visible = False
    self.data_grid_4.visible = False
    self.repeating_panel_5.visible = False
    self.repeating_panel_6.visible = True
    self.repeating_panel_7.visible =False
    self.repeating_panel_8.visible = False
    self.repeating_panel_9.visible = False