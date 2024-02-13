from ._anvil_designer import add_lender_dropdown_detailsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class add_lender_dropdown_details(add_lender_dropdown_detailsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh()

  def refresh(self):
        """Refresh repeating panels with the latest data"""
        # self.repeating_panel_1.items = app_tables.fin_lendor_gender.search()
        self.repeating_panel_2.items = app_tables.fin_lendor_qualification.search()
        self.repeating_panel_3.items = app_tables.fin_lendor_business_type.search()
        self.repeating_panel_4.items = app_tables.fin_lendor_lending_type.search()
        self.repeating_panel_5.items = app_tables.fin_lendor_employee_type.search()
        self.repeating_panel_6.items = app_tables.fin_lendor_organization_type.search()
        self.repeating_panel_7.items = app_tables.fin_lendor_account_type.search()
        self.repeating_panel_8.items = app_tables.fin_lendor_marrital_status.search()
        self.repeating_panel_9.items = app_tables.fin_lendor_no_of_employees.search()
        self.repeating_panel_10.items = app_tables.fin_lendor_lending_period.search()
  
  # def link_1_click(self, **event_args):
  #   """This method is called when the link is clicked"""
  #   open_form('admin.dashboard.manage_cms.manage_dropdowns')


  # def gender_click(self, **event_args):
  #   """This method is called when the button is clicked"""
  #   self.column_panel_7.visible = False
  #   self.column_panel_8.visible = False
  #   self.column_panel_9.visible = False
  #   self.column_panel_10.visible = False
  #   self.column_panel_6.visible = False
  #   self.column_panel_5.visible = False   
  #   self.column_panel_4.visible = False
  #   self.column_panel_3.visible = False
  #   self.column_panel_2.visible = True
  #   self.column_panel_11.visible = False

  def business_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_7.visible = False
    self.column_panel_8.visible = False
    self.column_panel_9.visible = False
    self.column_panel_10.visible = False
    self.column_panel_6.visible = False
    self.column_panel_5.visible = False   
    self.column_panel_4.visible = True
    self.column_panel_3.visible = False
    # self.column_panel_2.visible = False
    self.column_panel_11.visible = False

  def professioon_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_7.visible = False
    self.column_panel_8.visible = False
    self.column_panel_9.visible = False
    self.column_panel_10.visible = False
    self.column_panel_6.visible = True
    self.column_panel_5.visible = False   
    self.column_panel_4.visible = False
    self.column_panel_3.visible = False
    # self.column_panel_2.visible = False   
    self.column_panel_11.visible = False
  def No_of_emp_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_7.visible = False
    self.column_panel_8.visible = False
    self.column_panel_9.visible = False
    self.column_panel_10.visible = False
    self.column_panel_6.visible = False
    self.column_panel_5.visible = True   
    self.column_panel_4.visible = False
    self.column_panel_3.visible = False
    # self.column_panel_2.visible = False
    self.column_panel_11.visible = False
  def emp_type_button(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_7.visible = True
    self.column_panel_8.visible = False
    self.column_panel_9.visible = False
    self.column_panel_10.visible = False
    self.column_panel_6.visible = False
    self.column_panel_5.visible = False   
    self.column_panel_4.visible = False
    self.column_panel_3.visible = False
    # self.column_panel_2.visible = False
    self.column_panel_11.visible = False
  def organization_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_7.visible = False
    self.column_panel_8.visible = True
    self.column_panel_9.visible = False
    self.column_panel_10.visible = False
    self.column_panel_6.visible = False
    self.column_panel_5.visible = False   
    self.column_panel_4.visible = False
    self.column_panel_3.visible = False
    # self.column_panel_2.visible = False
    self.column_panel_11.visible = False
  def account_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_7.visible = False
    self.column_panel_8.visible = False
    self.column_panel_9.visible = True
    self.column_panel_10.visible = False
    self.column_panel_6.visible = False
    self.column_panel_5.visible = False   
    self.column_panel_4.visible = False
    self.column_panel_3.visible = False
    # self.column_panel_2.visible = False
    self.column_panel_11.visible = False
  def marital_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_7.visible = False
    self.column_panel_8.visible = False
    self.column_panel_9.visible = False
    self.column_panel_10.visible = True
    self.column_panel_6.visible = False
    self.column_panel_5.visible = False   
    self.column_panel_4.visible = False
    self.column_panel_3.visible = False
    # self.column_panel_2.visible = False
    self.column_panel_11.visible = False
  def lending_period_button(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_11.visible = True
    self.column_panel_7.visible = False
    self.column_panel_8.visible = False
    self.column_panel_9.visible = False
    self.column_panel_10.visible = False
    self.column_panel_6.visible = False
    self.column_panel_5.visible = False   
    self.column_panel_4.visible = False
    self.column_panel_3.visible = False
    # self.column_panel_2.visible = False
    
  def qualification(self, **event_args):
    """This method is called when the button is clicked"""
    entered_data = self.text_box_2.text
    # Check if the entered status is valid
    valid_statuses = ['10th class', 'Intermediate / PUC', 'Btech / B.E','Mtech','Phd']
    if entered_data not in valid_statuses:
        alert("Please enter a valid qualificarion : '10th class', 'Intermediate / PUC', 'Btech / B.E','Mtech','Phd'.")
        return
    new_row = app_tables.fin_lendor_qualification.add_row(lendor_qualification=entered_data)
    self.text_box_2.text = ' '
    self.refresh()
    
  # def gender_button_click(self, **event_args):
  #   """This method is called when the button is clicked"""
  #   entered_data = self.text_box_1.text
  #   new_row = app_tables.fin_lendor_gender.add_row(lendor_gender=entered_data)
  #   self.text_box_1.text = ' '
  #   self.refresh()
  
  def business_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_data = self.text_box_3.text
    new_row = app_tables.fin_lendor_business_type.add_row(lendor_business_type=entered_data)
    self.text_box_3.text = ' '
    self.refresh()

  def no_of_emp_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_data = self.text_box_4.text
    new_row = app_tables.fin_lendor_no_of_employees.add_row(lendor_no_of_employees=entered_data)
    self.text_box_4.text = ' '
    self.refresh()

  def lending_type(self, **event_args):
    """This method is called when the button is clicked"""
    entered_data = self.text_box_5.text
    valid_statuses = ['Individual', 'Institutional']
    if entered_data not in valid_statuses:
        alert("Please enter a valid lending type : 'Individual', 'Institutional'.")
        return
    new_row = app_tables.fin_lendor_lending_type.add_row(lendor_lending_type=entered_data)
    self.text_box_5.text = ' '
    self.refresh()

  def emp_type_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_data = self.text_box_6.text
    new_row = app_tables.fin_lendor_employee_type.add_row(lendor_employee_type=entered_data)
    self.text_box_6.text = ' '
    self.refresh()

  def organization_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_data = self.text_box_7.text
    new_row = app_tables.fin_lendor_organization_type.add_row(lendor_organization_type=entered_data)
    self.text_box_7.text = ' '
    self.refresh()

  def account_Type_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_data = self.text_box_8.text
    new_row = app_tables.fin_lendor_account_type.add_row(lendor_account_type=entered_data)
    self.text_box_8.text = ' '
    self.refresh()

  def marital_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_data = self.text_box_9.text
    valid_statuses = ['Not Married', 'Married', 'Other']
    if entered_data not in valid_statuses:
        alert("Please enter a valid marital status: 'Not Married', 'Married', 'Other'.")
        return
    new_row = app_tables.fin_lendor_marrital_status.add_row(lendor_marrital_status=entered_data)
    self.text_box_9.text = ' '
    self.refresh()

  def qualification_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_7.visible = False
    self.column_panel_8.visible = False
    self.column_panel_9.visible = False
    self.column_panel_10.visible = False
    self.column_panel_6.visible = False
    self.column_panel_5.visible = False   
    self.column_panel_4.visible = False
    self.column_panel_3.visible = True
    # self.column_panel_2.visible = False
    self.column_panel_11.visible = False

  def lending_period_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_data = self.text_box_10.text
    new_row = app_tables.fin_lendor_lending_period.add_row(lendor_lending_period=entered_data)
    self.text_box_10.text = ' '
    self.refresh()

  def button_1_copy_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.manage_cms.manage_dropdowns')

