from ._anvil_designer import lender_registration_form_3_marital_marriedTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class lender_registration_form_3_marital_married(lender_registration_form_3_marital_marriedTemplate):
    def __init__(self, user_id, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.userId = user_id

    def is_married(self):
        # Check the marital status in the user profile table
        user_profile = app_tables.fin_user_profile.get(customer_id=self.userId)
        return user_profile['marital_status'] == 'Married'

    def button_1_click(self, **event_args):
        open_form('lendor_registration_form.lender_registration_form_2.lender_registration_form_3_marital_details',user_id=self.userId)

    def radio_button_1_clicked(self, **event_args):
        """This method is called when this radio button is selected"""
        self.grid_panel_1.visible = True
        self.grid_panel_2.visible = False
        self.grid_panel_3.visible = False
        self.grid_panel_4.visible = False
        self.button_submit.visible = True
        self.button_submit_copy.visible = False
        self.button_submit_copy_2.visible = False
        self.button_submit_copy_3.visible = False
        self.selected_radio_button = "father"

    def radio_button_2_clicked(self, **event_args):
        """This method is called when this radio button is selected"""
        self.grid_panel_1.visible = False
        self.grid_panel_2.visible = True
        self.grid_panel_3.visible = False
        self.grid_panel_4.visible = False
        self.button_submit.visible = False
        self.button_submit_copy.visible = True
        self.button_submit_copy_2.visible = False
        self.button_submit_copy_3.visible = False
        self.selected_radio_button = "Mother"

    def radio_button_3_clicked(self, **event_args):
        """This method is called when this radio button is selected"""
        if self.is_married():
            self.grid_panel_1.visible = False
            self.grid_panel_2.visible = False
            self.grid_panel_3.visible = True
            self.grid_panel_4.visible = False
            self.button_submit.visible = False
            self.button_submit_copy.visible = False
            self.button_submit_copy_2.visible = True
            self.button_submit_copy_3.visible = False
            self.selected_radio_button = "spouse"


    def radio_button_4_clicked(self, **event_args):
        """This method is called when this radio button is selected"""
        self.grid_panel_1.visible = False
        self.grid_panel_2.visible = False
        self.grid_panel_3.visible = False
        self.grid_panel_4.visible = True
        self.button_submit.visible = False
        self.button_submit_copy.visible = False
        self.button_submit_copy_2.visible = False
        self.button_submit_copy_3.visible = True
        self.selected_radio_button = "others"

    def collect_details(self):
        # Collect details from the form
        father_name = self.father_name_text.text
        father_dob = self.date_picker_1.date
        father_mbl_no_text = self.father_mbl_no_text.text
        father_mbl_no = int(father_mbl_no_text) if father_mbl_no_text.strip().isdigit() else None
        father_profession = self.father_profession_text.text
        father_address = self.father_address_text.text

        # Mother details
        mother_name = self.mother_name_text_copy.text
        mother_dob = self.date_picker_2.date
        mother_mbl_no_text = self.mother_mbl_no_text.text
        mother_mbl_no = int(mother_mbl_no_text) if mother_mbl_no_text.strip().isdigit() else None
        mother_profession = self.mother_profession_text.text
        mother_address = self.mother_address_text.text

        # Spouse details
        spouse_name = self.spouse_name_text.text
        spouse_dob = self.date_picker_3.date
        spouse_mbl_no_text = self.spouse_mbl_no_text.text
        spouse_mbl_no = int(spouse_mbl_no_text) if spouse_mbl_no_text.strip().isdigit() else None
        spouse_profession = self.spouse_profession_text.text
        spouse_company = self.spouse_companyname_text.text
        anual_earning = self.annual_earning_text.text

        # Related person details
        person_relation = self.related_person_text.text
        related_dob = self.date_picker_3_copy.date
        related_name = self.name_text_copy.text
        related_mob_text = self.mbl_no_text_copy.text
        related_mob = int(related_mob_text) if related_mob_text.strip().isdigit() else None
        related_profession = self.profession_text_copy.text

        # Return the collected details as a dictionary
        return {
            'father_name': father_name,
            'father_dob': father_dob,
            'father_mbl_no': father_mbl_no,
            'father_profession': father_profession,
            'father_address': father_address,

            'mother_name': mother_name,
            'mother_dob': mother_dob,
            'mother_mbl_no': mother_mbl_no,
            'mother_profession': mother_profession,
            'mother_address': mother_address,

            'spouse_name': spouse_name,
            'spouse_dob': spouse_dob,
            'spouse_mbl_no': spouse_mbl_no,
            'spouse_profession': spouse_profession,
            'spouse_company': spouse_company,
            'annual_earning': anual_earning,

            'related_person_relation': person_relation,
            'related_person_dob': related_dob,
            'related_person_name': related_name,
            'related_person_mob': related_mob,
            'related_person_profession': related_profession,
            'another_person': self.selected_radio_button  # Store the selected radio button's name
        }

    def button_submit_click(self, **event_args):
        # Collect details from the form
        details = self.collect_details()

        # Insert details into the data table
        app_tables.fin_guarantor_details.add_row(
            customer_id=self.userId,
            guarantor_name=details['father_name'],
            guarantor_date_of_birth=details['father_dob'],
            guarantor_mobile_no=details['father_mbl_no'],
            guarantor_profession=details['father_profession'],
            guarantor_address=details['father_address'],
            another_person=details['another_person']  # Store the selected radio button's name
        )
       
        open_form('lendor_registration_form.lender_registration_form_4_bank_form_1',user_id = user_id)

    def button_submit_copy_click(self, **event_args):
        """This method is called when the button is clicked"""
        details = self.collect_details()

        # Insert details into the data table
        app_tables.fin_guarantor_details.add_row(
            customer_id=self.userId,
            guarantor_name=details['mother_name'],
            guarantor_date_of_birth=details['mother_dob'],
            guarantor_mobile_no=details['mother_mbl_no'],
            guarantor_profession=details['mother_profession'],
            guarantor_address=details['mother_address'],
            another_person=details['another_person']  # Store the selected radio button's name
        )
        
        open_form('lendor_registration_form.lender_registration_form_4_bank_form_1',user_id = self.userId)

    def button_submit_copy_2_click(self, **event_args):
        """This method is called when the button is clicked"""
        details = self.collect_details()

        # Insert details into the data table
        app_tables.fin_guarantor_details.add_row(
            customer_id=self.userId,
            guarantor_name=details['spouse_name'],
            guarantor_date_of_birth=details['spouse_dob'],
            guarantor_mobile_no=details['spouse_mbl_no'],
            guarantor_profession=details['spouse_profession'],
            guarantor_company_name=details['spouse_company'],
            guarantor_annual_earning=details['annual_earning'],
            another_person=details['another_person']  # Store the selected radio button's name
        )
    
        open_form('lendor_registration_form.lender_registration_form_4_bank_form_1',user_id = self.userId)
      
    def button_submit_copy_3_click(self, **event_args):
        """This method is called when the button is clicked"""
        details = self.collect_details()

        # Insert details into the data table
        app_tables.fin_guarantor_details.add_row(
            customer_id=self.userId,
            guarantor_name=details['related_person_name'],
            guarantor_date_of_birth=details['related_person_dob'],
            guarantor_mobile_no=details['related_person_mob'],
            guarantor_profession=details['related_person_profession'],
            guarantor_person_relation= details['related_person_relation'],
            another_person=details['another_person']  # Store the selected radio button's name
        )
     
        open_form('lendor_registration_form.lender_registration_form_4_bank_form_1',user_id = self.userId)