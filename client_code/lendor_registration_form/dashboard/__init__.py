from ._anvil_designer import dashboardTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
from anvil.tables import app_tables
from anvil import open_form, server
from anvil import server
#from anvil import get_current_user
#from ....bank_users.main_form import main_form_module
from ...bank_users.main_form import main_form_module


class dashboard(dashboardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
   
    self.email = main_form_module.email
    email = self.email
    self.user_id=main_form_module.userId
    user_id = self.user_id
 
    # customer_id = 1000
    
    # anvil.server.call('fetch_profile_data_and_insert', email,user_id)

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.view_opening_balance")

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.view_available_balance")

  def button_5_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.view_borrower_loan_request")

  def button_6_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.loan_disbursement")

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.today_dues")

  def outlined_button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.view_lost_oppurtunities")

  def outlined_button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.lender_view_loans")

  def outlined_button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.view_loan_extension_requests")

  def outlined_button_5_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.view_loan_foreclosure_Requests")

  def outlined_button_6_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.top_up_amount")

  def outlined_button_7_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.view_or_download_portfolio")

  def outlined_button_8_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.view_profile")

  def outlined_button_9_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.view_or_send_notifications")

  def outlined_button_10_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.change_password")

  def login_signup_button_click(self, **event_args):
    """This method is called when the button is clicked"""

    alert("Logged out sucessfully")
    anvil.users.logout()
    open_form('bank_users.main_form')

  def home_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor_registration_form.dashboard")

  def about_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor_registration_form.dashboard.dasboard_about")

  def contact_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor_registration_form.dashboard.dasboard_contact")

  def button_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def button_show(self, **event_args):
    """This method is called when the Button is shown on the screen"""
    pass

  def button_hide(self, **event_args):
    """This method is called when the Button is removed from the screen"""
    pass

  
  def toggleswitch_1_x_change(self, **event_args):
    
    if self.toggleswitch_1.checked:
      self.button_status.text = "ONLINE"
      self.button_status.background = '#0876e8'  # Green color
      self.button_status.foreground = '#FFFFFF'  # White text
      # Update 'make_visibility' column in the 'lender' table to True
      lender_row = app_tables.fin_lender.search() # Assuming you have a row with id=1 for the lender
      lender_row[0]['make_visibility'] = True
      lender_row[0].update()
    else:
      self.button_status.text = "OFFLINE"
      self.button_status.background = '#FFFFFF'  # White color
      self.button_status.foreground = '#FF0000'  # Red text
      lender_row = app_tables.fin_lender.search()# Assuming you have a row with id=1 for the lender
      lender_row[0]['make_visibility'] = False
      lender_row[0].update()

  def notification_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('lendor_registration_form.dashboard.notification')

  # def wallet_dashboard_link_click(self, **event_args):
  #   """This method is called when the link is clicked"""
  #   open_form('wallet.wallet')

  def wallet_dashboard_link_click(self, **event_args):
    user_profiles = server.call('fetch_user_profiles')
    
    for profile in user_profiles:
        result = server.call(
            'create_wallet_entry',
            profile['email_user'],
            profile['customer_id'],
            profile['full_name'],
            profile['usertype']
        ) 
        print(result)
    
    open_form('wallet.wallet')
    
    
  