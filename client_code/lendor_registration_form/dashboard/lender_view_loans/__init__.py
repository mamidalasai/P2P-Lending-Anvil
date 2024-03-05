from ._anvil_designer import lender_view_loansTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import lendor_main_form_module as main_form_module


class lender_view_loans(lender_view_loansTemplate):
  def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.user_id = main_form_module.userId

        # Retrieve and display open loans
        self.repeating_panel_6.items = app_tables.fin_loan_details.search(
            loan_updated_status=q.any_of(
                q.like('disbursed loan%'),
                q.like('foreclosure%'),
                #q.like('close%')
            )
        )
        self.label_5.text = str(len(self.repeating_panel_6.items))

        # Retrieve and display closed loans
        self.repeating_panel_7.items = app_tables.fin_loan_details.search(loan_updated_status=q.like('close%'))
        self.label_6.text = str(len(self.repeating_panel_7.items))

        # Retrieve and display rejected loans
        self.repeating_panel_8.items = app_tables.fin_loan_details.search(loan_updated_status=q.like('reject%'))
        self.label_7.text = str(len(self.repeating_panel_8.items))

        # Retrieve and display underprocess loans
        self.repeating_panel_9.items = app_tables.fin_loan_details.search(loan_updated_status=q.like('under process%'))

        self.label_8.text = str(len(self.repeating_panel_9.items))

        # Retrieve and display foreclosure loans
        self.repeating_panel_10.items = app_tables.fin_loan_details.search(loan_updated_status=q.like('foreclosure%'))
        self.label_9.text = str(len(self.repeating_panel_10.items))

        # Any code you write here will run before the form opens.

    # ... (other methods)

    # Any code you write here will run before the form opens.

  


  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_1.visible=True
    self.label_2.visible=False
    self.label_3.visible=False
    self.label_4.visible=False
    self.label_10.visible=False
    #self.data_grid_1.visible=True
    # self.data_grid_2.visible=False
    # self.data_grid_3.visible=False
    # self.data_grid_4.visible=False
    # self.data_grid_5.visible=False
    self.repeating_panel_6.visible = True
    self.repeating_panel_7.visible = False
    self.repeating_panel_8.visible = False
    self.repeating_panel_9.visible = False
    self.repeating_panel_10.visible = False

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_1.visible=False
    self.label_2.visible=True
    self.label_3.visible=False
    self.label_4.visible=False
    self.label_10.visible=False
    # self.data_grid_1.visible=False
    # self.data_grid_2.visible=True
    # self.data_grid_3.visible=False
    # self.data_grid_4.visible=False
    # self.data_grid_5.visible=False
    self.repeating_panel_6.visible = False
    self.repeating_panel_7.visible = True
    self.repeating_panel_8.visible = False
    self.repeating_panel_9.visible = False
    self.repeating_panel_10.visible = False

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_1.visible=False
    self.label_2.visible=False
    self.label_3.visible=True
    self.label_4.visible=False
    self.label_10.visible=False
    # self.data_grid_1.visible=False
    # self.data_grid_2.visible=False
    # self.data_grid_3.visible=True
    # self.data_grid_4.visible=False
    # self.data_grid_5.visible=False
    self.repeating_panel_6.visible =False
    self.repeating_panel_7.visible = False
    self.repeating_panel_8.visible = True
    self.repeating_panel_9.visible = False
    self.repeating_panel_10.visible = False

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_1.visible=False
    self.label_2.visible=False
    self.label_3.visible=False
    self.label_4.visible=True
    self.label_10.visible=False
    # self.data_grid_1.visible=False
    # self.data_grid_2.visible=False
    # self.data_grid_3.visible=False
    # self.data_grid_4.visible=True
    # self.data_grid_5.visible=False
    self.repeating_panel_6.visible = False
    self.repeating_panel_7.visible = False
    self.repeating_panel_8.visible = False
    self.repeating_panel_9.visible = True
    self.repeating_panel_10.visible = False

  def button_5_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_1.visible=False
    self.label_2.visible=False
    self.label_3.visible=False
    self.label_4.visible=False
    self.label_10.visible=True
    # self.data_grid_1.visible=False
    # self.data_grid_2.visible=False
    # self.data_grid_3.visible=False
    # self.data_grid_4.visible=False
    # self.data_grid_5.visible=True
    self.repeating_panel_6.visible = False
    self.repeating_panel_7.visible = False
    self.repeating_panel_8.visible = False
    self.repeating_panel_9.visible = False
    self.repeating_panel_10.visible = True

  def home_lender_registration_form_copy_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard")
