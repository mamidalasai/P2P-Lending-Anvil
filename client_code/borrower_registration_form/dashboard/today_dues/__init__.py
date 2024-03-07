from ._anvil_designer import today_duesTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timezone,timedelta
from .. import main_form_module as main_form_module

class today_dues(today_duesTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.user_id = main_form_module.userId
        self.init_components(**properties)
        
        today_date = datetime.now(timezone.utc).date()
        loan_details = []
        # Fetch all loan details from fin_emi_table where next_payment matches today's date
        all_loans = list(app_tables.fin_emi_table.search(
            next_payment=q.less_than_or_equal_to(today_date)
        ))

        # Sort the list of loans in descending order based on next_payment date
        all_loans.sort(key=lambda x: x['next_payment'], reverse=True)
        # Check if any loans were found
        if all_loans:
            latest_loan = all_loans[0]
            
            # Fetch details for the latest loan
            loan_id = latest_loan['loan_id']
            loan_details_row = app_tables.fin_loan_details.get(loan_id=loan_id)
            if loan_details_row is not None:
                loan_amount = loan_details_row['loan_amount']
                scheduled_payment = latest_loan['scheduled_payment']
                next_payment = latest_loan['next_payment']
                days_left = (today_date - scheduled_payment).days
                emi_number = latest_loan['emi_number']
                account_number = latest_loan['account_number']
                tenure = loan_details_row['tenure']
                interest_rate = loan_details_row['interest_rate']
                borrower_loan_created_timestamp = loan_details_row['borrower_loan_created_timestamp']
                loan_updated_status = loan_details_row['loan_updated_status']
                loan_disbursed_timestamp = loan_details_row['loan_disbursed_timestamp']
                emi_payment_type = loan_details_row['emi_payment_type']
                lender_customer_id = loan_details_row['lender_customer_id']
                first_emi_payment_due_date = loan_details_row['first_emi_payment_due_date']
                total_repayment_amount = loan_details_row['total_repayment_amount']
                total_processing_fee_amount = loan_details_row['total_processing_fee_amount']

                # Populate loan details
                loan_details = [{
                    'loan_id': loan_id,
                    'loan_amount': loan_amount,
                    'scheduled_payment': scheduled_payment,
                    'days_left': days_left,
                    'tenure': tenure,
                    'interest_rate': interest_rate,
                    'borrower_loan_created_timestamp': borrower_loan_created_timestamp,
                    'emi_number': emi_number,
                    'account_number': account_number,
                    'loan_updated_status': loan_updated_status,
                    'loan_disbursed_timestamp': loan_disbursed_timestamp,
                    'next_payment': next_payment,
                    'emi_payment_type': emi_payment_type,
                    'lender_customer_id': lender_customer_id,
                    'first_emi_payment_due_date': first_emi_payment_due_date,
                    'total_repayment_amount':total_repayment_amount,
                    'total_processing_fee_amount' : total_processing_fee_amount
                }]
                
                # Now you can use loan_details list containing details of the latest loan
                print(loan_details)
        else:
            # Handle case where no loans are found for today's date
            print("No loans due today.")
          
        # If no loans are found with next_payment date matching today's date,
        # fetch the loan details based on the first_payment_due_date
        if not loan_details:
          all_loans_due = app_tables.fin_loan_details.search(
              first_emi_payment_due_date=q.less_than_or_equal_to(today_date)
          )
      
          for loan_due in all_loans_due:
              loan_id = loan_due['loan_id']
              loan_amount = loan_due['loan_amount']
              first_emi_payment_due_date = loan_due['first_emi_payment_due_date']
              days_left = (today_date - first_emi_payment_due_date).days
              # Fetch account number from user profile table based on customer_id
              user_profile = app_tables.fin_user_profile.get(customer_id=self.user_id)
              if user_profile is not None:
                  account_number = user_profile['account_number']
              else:
                  account_number = "N/A"
              
              # Set emi_number to 0
              emi_number = 0
              
              tenure = loan_due['tenure']
              interest_rate = loan_due['interest_rate']
              borrower_loan_created_timestamp = loan_due['borrower_loan_created_timestamp']
              loan_updated_status = loan_due['loan_updated_status']
              loan_disbursed_timestamp = loan_due['loan_disbursed_timestamp']
              emi_payment_type = loan_due['emi_payment_type']
              lender_customer_id = loan_due['lender_customer_id']
              total_repayment_amount = loan_due['total_repayment_amount']
              total_processing_fee_amount = loan_due['total_processing_fee_amount']
              
              # Calculate next_payment based on first_payment_due_date
              if emi_payment_type == 'One Time':
                if tenure:
                  next_payment = loan_disbursed_timestamp.date() + timedelta(days=30 * tenure)
              elif emi_payment_type == 'Monthly':
                  # For monthly payment, set next_payment to a month after first_payment_due_date
                  next_payment = loan_disbursed_timestamp.date() + timedelta(days=30)
              elif emi_payment_type == 'Three Month':
                  # For three-month payment, set next_payment to three months after first_payment_due_date
                  next_payment = loan_disbursed_timestamp.date() + timedelta(days=90)
              elif emi_payment_type == 'Six Month':
                  # For six-month payment, set next_payment  six months after first_payment_due_date
                  next_payment = loan_disbursed_timestamp.date() + timedelta(days=180)
              else:
                  # Default to monthly calculation if emi_payment_type is not recognized
                  next_payment = loan_disbursed_timestamp.date() + timedelta(days=30)
              
              loan_details.append({
                  'loan_id': loan_id,
                  'loan_amount': loan_amount,
                  'scheduled_payment':first_emi_payment_due_date,   # Set scheduled_payment to first_payment_due_date first_emi_payment_due_date
                  'next_payment': next_payment,
                  'days_left': days_left,
                  'tenure': tenure,
                  'interest_rate': interest_rate,
                  'borrower_loan_created_timestamp': borrower_loan_created_timestamp,
                  'loan_updated_status': loan_updated_status,
                  'loan_disbursed_timestamp': loan_disbursed_timestamp,
                  'emi_number': emi_number,
                  'account_number': account_number,
                  'emi_payment_type': emi_payment_type,
                  'lender_customer_id': lender_customer_id,
                  'total_repayment_amount':total_repayment_amount,
                  # 'first_payment_due_date': first_payment_due_date
                  'total_processing_fee_amount':total_processing_fee_amount
              })
        self.repeating_panel_2.items = loan_details
        for loan_detail in loan_details:
            print("Processing loan:", loan_detail)
            if loan_detail['days_left'] >= 6 and loan_detail['days_left'] < 8:
                print("Updating status to 'lapsed loan'")
                loan_detail['loan_updated_status'] = 'lapsed loan'
                loan_row = app_tables.fin_loan_details.get(loan_id=loan_detail['loan_id'])
                if loan_row is not None:
                    loan_row['loan_updated_status'] = 'lapsed loan'
                    loan_row.update()
            elif loan_detail['days_left'] >= 8 and loan_detail['days_left'] < 98:
                print("Updating status to 'default loan'")
                loan_detail['loan_updated_status'] = 'default loan'
                loan_row = app_tables.fin_loan_details.get(loan_id=loan_detail['loan_id'])
                if loan_row is not None:
                    loan_row['loan_updated_status'] = 'default loan'
                    loan_row.update()
            elif loan_detail['days_left'] >= 98:
                print("Updating status to 'default loan'")
                loan_detail['loan_updated_status'] = 'NPA'
                loan_row = app_tables.fin_loan_details.get(loan_id=loan_detail['loan_id'])
                if loan_row is not None:
                    loan_row['loan_updated_status'] = 'NPA'
                    loan_row.update()

                  
    def home_borrower_registration_form_copy_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('borrower_registration_form.dashboard')
