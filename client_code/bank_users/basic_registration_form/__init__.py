from ._anvil_designer import basic_registration_formTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime,timedelta
# from ..borrower_dashboard import borrower_main_form_module
from ..main_form import main_form_module
from ..user_form import user_module
import re

class basic_registration_form(basic_registration_formTemplate):
  def __init__(self,**properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.email = main_form_module.email
    email=self.email
    self.user_id =  user_module.find_user_id(email)
    print(self.user_id)
    
    user_id = self.user_id
    user_data=app_tables.fin_user_profile.get(customer_id=user_id)
    if user_data:
          self.full_name_text_box.text=user_data['full_name']
          self.date_picker_1.date=user_data['date_of_birth']
          self.mobile_number_box.text=user_data['mobile']
          self.alternate_email_text_box.text=user_data['another_email']
          self.govt_id1_text_box.text=user_data['aadhaar_no']
          self.govt_id2_text_box.text=user_data['pan_number']
          self.text_box_1.text=user_data['street_adress_1']
          self.text_box_2.text=user_data['street_address_2']
          self.text_box_3.text=user_data['city']
          self.text_box_4.text=user_data['pincode']
          self.text_box_5.text=user_data['state']
          self.text_box_6.text=user_data['country']
          user_data.update()
      
          options = app_tables.fin_gender.search()
          option_strings = [str(option['gender']) for option in options]
          self.gender_dd.items = option_strings
          

    # Any code you write here will run before the form opens.

  def submit_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    full_name = self.full_name_text_box.text
    gender = self.gender_dd.selected_value
    dob = self.date_picker_1.date
    mobile_no = self.mobile_number_box.text
    user_photo = self.registration_img_file_loader.file
    alternate_email = self.alternate_email_text_box.text
    aadhar = self.govt_id1_text_box.text
    aadhar_card = self.registration_img_aadhar_file_loader.file
    pan = self.govt_id2_text_box.text
    pan_card = self.registration_img_pan_file_loader.file
    street_adress_1 = self.text_box_1.text
    street_address_2 = self.text_box_2.text
    city = self.text_box_3.text
    pincode = self.text_box_4.text
    state = self.text_box_5.text
    country = self.text_box_6.text
    
    user_id = self.user_id
    
    self.full_name_label.text = ''
    self.dob_label.text = ''
    self.mobile_label.text = ''
    self.email_label.text = ''
    self.label_1.text=''
    self.label_2.text=''
    
    # Validate full name
    if not re.match(r'^[A-Za-z\s]+$', full_name):
            self.full_name_label.text = 'Enter a valid full name'
    elif not dob or dob > datetime.now().date():
            self.dob_label.text = 'Enter a valid date of birth'
    # Validate age (must be 18 or older)
    elif datetime.now().date() - dob < timedelta(days=365 * 18):
            self.dob_label.text = 'You must be at least 18 years old'
    elif not re.match(r'^\d{10}$', mobile_no):
      self.mobile_label.text = 'Enter valid mobile no'
    elif not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', alternate_email):
      self.email_label.text = 'Enter a valid email address'
    # elif not re.match(r'^\d{12}$', aadhar):
    #   self.label_1.text='enter valid aadhar no'
    # elif not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', pan):
    #   self.label_2.text='enter valid pan no'
    elif not full_name or not gender or not dob or not mobile_no or not alternate_email or not user_photo or not aadhar or not aadhar_card or not pan or not pan_card or not street_adress_1 and not street_address_2 or not city or not pincode or not state or not state or not country:
      Notification('Please fill all details').show()
    else:
      anvil.server.call('add_basic_details', full_name, gender, dob, mobile_no, user_photo, alternate_email, aadhar, aadhar_card, pan, pan_card, street_adress_1, street_address_2, city, pincode, state, country, user_id)
      Notification("basic details form fill up submitted successfully")
      open_form('bank_users.user_form')
            

  def full_name_text_box_change(self, **event_args):
        # This event is triggered when the text in the full name text box changes.
        # Check the format and hide the error label if the format is correct.
        full_name = self.full_name_text_box.text
        if re.match(r'^[A-Za-z\s]+$', full_name):
            self.full_name_label.text = ''
    
  def date_picker_1_change(self, **event_args):
        # This event is triggered when the date in the date picker changes.
        # Check if the date is valid and hide the error label if it is correct.
        dob = self.date_picker_1.date
        if not dob or dob > datetime.now().date():
            self.dob_label.text = ''
