import anvil
from ._anvil_designer import Borr_loan_requestTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables
from anvil import open_form
from datetime import datetime
from ... import lendor_main_form_module as main_form_1
from .....bank_users.main_form import main_form_module
from datetime import timedelta


# In Borr_loan_request class

class Borr_loan_request(Borr_loan_requestTemplate):
    def __init__(self, selected_row, **properties):
       # Set Form properties and Data Bindings.
        self.selected_row = selected_row
        self.init_components(**properties)
        self.user_id=main_form_1.userId
        use_id = self.user_id

        self.email=main_form_module.email
        email = self.email

        # self.entered_loan_id = entered_loan_id
        
        
        # Populate labels with the selected row details
        self.label_user_id.text = f"{selected_row['borrower_customer_id']}"
        self.label_name.text = f"{selected_row['borrower_full_name']}"
        self.label_loan_amount_applied.text = f"{selected_row['loan_amount']}"
        self.label_loan_id.text = f"{selected_row['loan_id']}"
        self.label_beseem_score.text = f"{selected_row['beseem_score']}"
        self.label_loan_tenure.text = f"{selected_row['tenure']}"
        self.label_credit_limit.text = f"{selected_row['credit_limit']}"
        self.label_interest_rate.text = f"{selected_row['interest_rate']}"
        self.update_ui_based_on_status()
        
        # Fetch additional details from the 'borrower' table
        try:
            user_request = app_tables.fin_borrower.get(customer_id=str(selected_row['borrower_customer_id']))
            if user_request is not None:
                # Assuming 'bank_acc_details' is a valid column name in the 'borrower' table
                bank_acc_details = user_request['bank_acc_details']
                borrower_approve_date = user_request['borrower_approve_date']
                self.label_member_since.text = f"{borrower_approve_date}"
                self.label_bank_acc_details.text = f"{bank_acc_details}"
                
                # Fetch additional details from the 'loan_details' table
                try:
                    #loan_details = app_tables.loan_details.get(loan_id=int(selected_row['loan_id']))
                    loan_details = app_tables.fin_loan_details.get(loan_id=str(selected_row['loan_id']))
                    if loan_details is not None:
                        # Assuming 'interest_rate' and 'min_amount' are valid column names in the 'loan_details' table
                        interest_rate = loan_details['interest_rate']
                        min_amount_text = loan_details['loan_amount']
                        
                        # Calculate and display ROM in amount format
                        rom_amount = self.calculate_rom(interest_rate,min_amount_text)
                        self.label_member_rom.text = f"{rom_amount:.2f}"
                    else:
                        self.label_member_rom.text = "No data for loan_id in loan_details"
                except anvil.tables.TableError as e:
                    self.label_member_rom.text = f"Error fetching loan details: {e}"
            else:
                self.label_bank_acc_details.text = "No data for bank_acc_details in user_request"
        except anvil.tables.TableError as e:
            self.label_bank_acc_details.text = f"Error fetching user details: {e}"
           
        loan_id = self.label_loan_id.text
        self.entered_loan_id = loan_id
        borrower_customer_id = self.label_user_id.text
        self.entered_borrower_customer_id = borrower_customer_id
      
    def calculate_rom(self, interest_rate, min_amount_text):
        # Calculate ROM based on your business logic
        try:
            # Convert min_amount_text to a numeric value (assuming it's a string representing a number)
            min_amount = float(min_amount_text)

            earnings = interest_rate * min_amount

            return earnings
        except ValueError as e:
            print(f"Error converting min_amount_text to numeric: {e}")
            return 0

    

    def button_1_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('lendor_registration_form.dashboard.view_borrower_loan_request')
   
  
    def update_ui_based_on_status(self):
        # Check the value of 'loan_updated_status' in the database
        loan_status = self.selected_row['loan_updated_status']

        if loan_status == 'accepted':
            # Set the text of the Output Label with blue color
            self.output_label1.text = "This Borrower Loan is Accepted"
            self.output_label1.foreground = '#0000FF'  # Blue color
            self.output_label1.visible = True
            # Disable the "Accept" button
            self.accepted_btn.enabled = False
            self.accepted_btn.visible = False
            self.rejected_btn.visible = False
        elif loan_status == 'rejected':
            # Set the text of the Output Label with red color
            self.output_label1.text = "This Borrower Loan is Rejected"
            self.output_label1.foreground = '#FF0000'  # Red color
            self.output_label1.visible = True
            # Disable the "Reject" button
            self.rejected_btn.enabled = False
            self.accepted_btn.visible = False
            self.rejected_btn.visible = False
        
    def accepted_btn_click(self, **event_args):
        """This method is called when the button is clicked"""
        
        self.accepted_btn.visible = True
        self.rejected_btn.visible = False
        self.loan_disbursment_btn.visible = False
      
        self.accepted_btn.visible = False
        # Set the text of the Output Label with blue color
        self.output_label1.text = "This Borrower Loan is Rejected"
        self.output_label1.foreground = '#0000FF'  # Blue color
        self.output_label1.visible = True
        # Update the 'loan_updated_status' column in the 'loan_details' table to 'accepted'
        self.selected_row['loan_updated_status'] = 'accepted'
        self.selected_row['lender_accepted_timestamp'] = datetime.now()
        # Save changes to the table
        self.selected_row.update()
        # Update UI based on the new status
        Notification("Borrower will get notified").show()
        self.update_ui_based_on_status()
        self.loan_disbursment_btn.visible = True
        

        # Close the form after deletion
        # open_form("lendor_registration_form.dashboard.vblr")

    def rejected_btn_click(self, **event_args):
        """This method is called when the button is clicked"""
        
        self.accepted_btn.visible = False
        self.rejected_btn.visible = True
        self.loan_disbursment_btn.visible = False
      
        self.rejected_btn.visible = False
        # Set the text of the Output Label with blue color
        self.output_label1.text = "This Borrower Loan is Rejected"
        self.output_label1.foreground = '#FF0000'  # Red color
        self.output_label1.visible = True
        # Update the 'loan_updated_status' column in the 'loan_details' table to 'Rejected'
        self.selected_row['loan_updated_status'] = 'rejected'
        # Save changes to the table
        self.selected_row.update()
        # Update UI based on the new status
        self.update_ui_based_on_status()
        

        # Close the form after deletion
        open_form("lendor_registration_form.dashboard.view_borrower_loan_request")

    def open_wallet_form(self):
        # Call the server-side function to get the signal
        signal = anvil.server.call('open_wallet_form')

    def calculate_first_emi_due_date(self, emi_payment_type, loan_disbursed_timestamp, tenure):
      if emi_payment_type == "Monthly":
        first_emi_due_date = (loan_disbursed_timestamp + timedelta(days=30)).date()
      elif emi_payment_type == "Three Month":
        first_emi_due_date = (loan_disbursed_timestamp + timedelta(days=90)).date()
      elif emi_payment_type == "Six Month":
        first_emi_due_date = (loan_disbursed_timestamp + timedelta(days=180)).date()
      elif emi_payment_type == "One Time":
        if tenure:
            # Add the tenure in months to the loan_disbursed_timestamp
            first_emi_due_date = (loan_disbursed_timestamp + timedelta(days=30 * tenure)).date()
        else:
            # Handle the case where tenure is not provided (raise an exception or set to None)
            first_emi_due_date = None
      else:
        # Handle other cases or raise an exception as needed
        first_emi_due_date = None

      return first_emi_due_date

    def loan_disbursment_btn_click(self, **event_args):
        """This method is called when the button is clicked"""
        
        # Assuming 'selected_row' is the selected row from the loan_details table
        selected_row = self.selected_row  
        email = main_form_module.email
        entered_loan_id = self.entered_loan_id
        entered_borrower_customer_id = self.entered_borrower_customer_id
      
        tenure = selected_row['tenure']
      
        # Call the server-side function
        signal = anvil.server.call('loan_disbursement_action', selected_row, email)

        # Check the signal and perform actions accordingly
        if signal == "insufficient_balance":
            alert("Warning: Your account balance is insufficient. Please deposit amount into your wallet. If not done within the next 2 minutes, the opportunity may be lost")
            open_form("wallet.wallet_deposit", entered_loan_id=entered_loan_id,entered_borrower_customer_id=entered_borrower_customer_id)
        elif signal == "Time_out":
            alert("The designated time has passed. The loan has moved to the 'Lost Opportunities' status.")
            open_form("wallet.wallet") 
        elif signal == "pay_to_borrower":
            alert("Pay to Borrower")
            self.selected_row['loan_disbursed_timestamp'] = datetime.now()
            emi_payment_type = self.selected_row['emi_payment_type']

            # Calculate and set the first EMI payment due date (only date portion)
            loan_disbursed_timestamp = self.selected_row['loan_disbursed_timestamp']
            first_emi_due_date = self.calculate_first_emi_due_date(emi_payment_type, loan_disbursed_timestamp, tenure)
            
            self.selected_row['first_emi_payment_due_date'] = first_emi_due_date

            entered_borrower_customer_id = self.entered_borrower_customer_id
            # Convert entered_borrower_customer_id to integer
            try:
              entered_borrower_customer_id = int(entered_borrower_customer_id)
            except ValueError:
              alert("Please enter a valid customer ID.")
              return
            # Search for the row in fin_wallet table
            wallet_add = app_tables.fin_wallet.get(customer_id=entered_borrower_customer_id)
            if wallet_add:
              entered_loan_id = self.entered_loan_id
              loan_row = app_tables.fin_loan_details.get(loan_id=entered_loan_id)
              if loan_row:
                loan_amount = loan_row['loan_amount']
              wallet_add['wallet_amount'] += loan_amount
              wallet_add.update()

              # You may want to update the loan_updated_status here if needed
              updated_loan_status = 'disbursed loan'
              loan_row['loan_updated_status'] = updated_loan_status
              # Save the changes to the loan_row
              loan_row.update()

            # # Update 'loan_updated_status' column
            # selected_row['loan_updated_status'] = 'disbursed loan'
            # selected_row.update()

            open_form("wallet.wallet")

    def link_1_click(self, **event_args):
      open_form('lendor_registration_form.dashboard.view_borrower_loan_request.payment_details_view_loan_request', selected_row=self.selected_row)
