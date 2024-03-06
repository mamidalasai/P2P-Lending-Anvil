# import anvil.google.auth
# import anvil.google.drive
# from anvil.google.drive import app_files
# import anvil.tables as tables
# import anvil.tables.query as q
# from anvil.tables import app_tables
# import anvil.google.auth
# import anvil.google.drive
# from anvil.tables import app_tables
# from anvil.google.drive import app_files
# import anvil.users
# import anvil.tables as tables
# from anvil import DataGrid, alert, open_form
# from datetime import datetime, timedelta
# import anvil.server
# from ._anvil_designer import payment_details_extensionTemplate

# class payment_details_extension(payment_details_extensionTemplate):
#     def __init__(self, selected_row=None, entered_values=None,loan_extension_months=None, extension_fee=None, **properties):
#         self.selected_row = selected_row
#         self.loan_extension_months = loan_extension_months
#         self.extension_fee = extension_fee
#         self.init_components(**properties)

#         if selected_row:
#             self.load_payment_details(selected_row, entered_values)

#     def load_payment_details(self, selected_row, entered_values):
#       self.load_entered_values(entered_values)
#       payment_details = []
  
#       # Calculate number of payment details based on emi_payment_type
#       num_payments = self.calculate_num_payments(selected_row)
  
#       # Initialize beginning_balance to the loan amount
#       beginning_balance = selected_row['total_repayment_amount']
#       beginning_loan_amount_balance = selected_row['loan_amount']

#       extension_fee_percentage = self.extension_fee if self.extension_fee is not None else selected_row.get('extension_fee', 0)
#       extension_fee_amount = (extension_fee_percentage / 100) * selected_row['loan_amount']

#       last_paid_emi_records = app_tables.fin_emi_table.search(loan_id=selected_row['loan_id'], scheduled_payment_made=q.not_(None))
#       last_paid_emi_number = max([record['emi_number'] for record in last_paid_emi_records], default=0)
#       # last_paid_emi_ending_balance = selected_row['loan_amount']
  
#       for month in range(1, num_payments + 1):
#           payment_date = self.calculate_payment_date(selected_row, month)
  
#           # Call the appropriate calculation method based on emi_payment_type
#           if selected_row['emi_payment_type'] == 'Monthly':
#               emi, interest_amount, ending_balance, ending_loan_amount_balance,processing_fee_per_month = self.calculate_monthly_emi_and_balance(selected_row, month)
#           elif selected_row['emi_payment_type'] == 'Three Month':
#               emi, interest_amount, ending_balance, ending_loan_amount_balance,processing_fee_per_month = self.calculate_three_month_emi_and_balance(selected_row, month)
#           elif selected_row['emi_payment_type'] == 'Six Month':
#               emi, interest_amount, ending_balance, ending_loan_amount_balance,processing_fee_per_month = self.calculate_six_month_emi_and_balance(selected_row, month)
#           elif selected_row['emi_payment_type'] == 'One Time':
#               emi, interest_amount, ending_balance, ending_loan_amount_balance,processing_fee_per_month = self.calculate_one_time_emi_and_balance(selected_row, month)
#           else:
#               # Handle unsupported payment types
#               emi, interest_amount, ending_balance, ending_loan_amount_balance,processing_fee_per_month = 0, 0, 0
  
#           # Fetch extra payment from fin_extension_loan table
#           extension_row = app_tables.fin_extends_loan.get(
#               loan_id=selected_row['loan_id'],
#               emi_number=month
#           )
#           extra_payment = extension_row['extension_amount'] if extension_row else 0
  
#           # Add extension amount to beginning balance
#           beginning_balance += extra_payment or 0
  
#           # Fetch scheduled_payment_made and account_number from the emi_payments table
#           emi_row = app_tables.fin_emi_table.get(
#               loan_id=selected_row['loan_id'],
#               emi_number=month
#           )
#           scheduled_payment_made = emi_row['scheduled_payment_made'] if emi_row else None
#           account_number = emi_row['account_number'] if emi_row else None
  
#           # Determine display values for EMIDate and AccountNumber
#           scheduled_payment_made_display = f"{scheduled_payment_made:%Y-%m-%d}" if scheduled_payment_made else "N/A"
#           emi_time_display = f"{scheduled_payment_made:%I:%M %p}" if scheduled_payment_made else "N/A"
#           account_number_display = account_number if account_number else "N/A"
  
#           # Format payment date
#           formatted_payment_date = f"{payment_date:%Y-%m-%d}" if payment_date else "Awaiting Update"
  
#           # Add payment details to the list
#           payment_details.append({
#               'PaymentNumber': month,
#               'PaymentDate': formatted_payment_date,
#               'EMIDate': scheduled_payment_made_display,
#               'EMITime': emi_time_display,
#               'AccountNumber': account_number_display,
#               'ScheduledPayment': f"₹ {emi:.2f}",
#               'Principal': f"₹ {(emi - interest_amount):.2f}",
#               'Interest': f"₹ {interest_amount:.2f}",
#               'BeginningBalance': f"₹ {beginning_balance:.2f}",
#               'ExtraPayment': f"₹ {extra_payment:.2f}" if extra_payment is not None else "N/A",
#               'TotalPayment': f"₹ {emi + extra_payment if extra_payment is not None else emi:.2f}",
#               'EndingBalance': f"₹ {ending_balance:.2f}",
#               'ProcessingFee': f"₹ {processing_fee_per_month:.2f}",
#               'beginning_loan_amount_balance': f"₹ {beginning_loan_amount_balance:.2f}",
#               'ending_loan_amount_balance': f"₹ {ending_loan_amount_balance:.2f}"
#           })
  
#           # Update beginning balance for the next iteration
#           beginning_balance = ending_balance
#           beginning_loan_amount_balance = ending_loan_amount_balance
  
#       # If there are remaining months and the last payment type is 'Three Month' or 'Six Month'
#       remaining_months = selected_row['tenure'] % 3 if selected_row['emi_payment_type'] == 'Three Month' else selected_row['tenure'] % 6
#       beginning_balance = ending_balance  # Use the total repayment amount

    
# # Check if there are remaining months
#       if remaining_months and selected_row['emi_payment_type'] in ['Three Month', 'Six Month']:
#           # Calculate EMI for the remaining month(s)
#           remaining_emi = self.calculate_emi_1(beginning_balance, remaining_months,selected_row['interest_rate'])
          
#           # Calculate interest amount for the remaining months
#           interest_amount = self.calculate_interest(beginning_balance, selected_row['interest_rate'], remaining_months)
        
#           extension_row = app_tables.fin_extends_loan.get(
#           loan_id=selected_row['loan_id'],
#           emi_number=num_payments + 1  # Assuming num_payments is the last paid EMIs count
#              )
#           extra_payment = extension_row['extension_amount'] if extension_row else 0

#           if selected_row['total_processing_fee_amount'] is not None:
#               # Ensure processing fee is considered monthly
#               processing_fee = selected_row['total_processing_fee_amount'] / selected_row['tenure']
#               # If remaining months are less than tenure, add processing fee for each remaining month
#               if remaining_months < selected_row['tenure']:
#                   processing_fee_per_month = processing_fee * remaining_months
#               else:
#                   processing_fee_per_month = selected_row['total_processing_fee_amount']
#           else:
#               processing_fee_per_month = 0
            
#           account_number_display = account_number_display
        
#           emi_row_remaining = app_tables.fin_emi_table.search(
#               loan_id=selected_row['loan_id'],
#           )
#           latest_scheduled_payment = None
#           for row in emi_row_remaining:
#               if row['emi_number'] > num_payments:
#                   # This payment is within the remaining months
#                   if row['scheduled_payment_made'] is not None:
#                       if latest_scheduled_payment is None or row['scheduled_payment_made'] > latest_scheduled_payment:
#                           latest_scheduled_payment = row['scheduled_payment_made']
#           if latest_scheduled_payment:
#               scheduled_payment_made_display = f"{latest_scheduled_payment:%Y-%m-%d}"
#               emi_time_display = f"{latest_scheduled_payment:%I:%M %p}"
        
#           loan_updated_status = selected_row['loan_updated_status'].lower() if selected_row['loan_updated_status'] else None
#           # Checking if loan_updated_status is 'close' before proceeding with date manipulation
#           if loan_updated_status in ['close', 'closed loans', 'disbursed loan', 'foreclosure']:
#               formatted_payment_date_datetime = datetime.strptime(formatted_payment_date, '%Y-%m-%d')
          
#               if selected_row['emi_payment_type'] == 'Three Month':
#                   # For 'Three Month', add 90 days and update to the next boundary
#                   payment_date = formatted_payment_date_datetime + timedelta(days=90)
#               elif selected_row['emi_payment_type'] == 'Six Month':
#                   # For 'Six Month', add 180 days
#                   payment_date = formatted_payment_date_datetime + timedelta(days=180)
#               else:
#                   # Assuming payment date is None for other payment types
#                   payment_date = None
          
#               # Concatenate only the date component if payment_date is not None
#               formatted_payment_date = payment_date.strftime('%Y-%m-%d') if payment_date else "Awaiting Update"  # Indicate that this is for the remaining month(s)
#           else:
#               formatted_payment_date = "Awaiting Update"
#           beginning_balance = ending_balance  # Use the total repayment amount
          
#           # Add the details for the remaining month(s)
#           payment_details.append({
#               'PaymentNumber': num_payments + 1,
#               'PaymentDate': formatted_payment_date,
#               'EMIDate': scheduled_payment_made_display,
#               'EMITime': emi_time_display,
#               'AccountNumber': account_number_display,
#               'ScheduledPayment': f"₹ {remaining_emi:.2f}",
#               'Principal': f"₹ {(remaining_emi - interest_amount):.2f}",
#               'Interest': f"₹ {interest_amount:.2f}",
#               'BeginningBalance': f"₹ {beginning_balance + extra_payment:.2f}",
#               'ProcessingFee': f"₹ {processing_fee_per_month:.2f}",
#               'ExtraPayment': f"₹ {extra_payment:.2f}" if extra_payment is not None else "N/A",
#               'TotalPayment': f"₹ {remaining_emi + extra_payment:.2f}",
#               'EndingBalance': f"₹ 0.00",  # Ending balance is assumed to be 0 for the final month(s)
#               'beginning_loan_amount_balance': f"₹ {ending_loan_amount_balance}",  # Assuming the loan is fully paid off
#               'ending_loan_amount_balance': f"₹ 0.00"  # Assuming the loan is fully paid off
#           })
      
#       # Set the Data Grid's items property to the list of payment details
#       self.repeating_panel_1.items = payment_details

#     def calculate_interest(self, beginning_balance, interest_rate, remaining_months):
#     # Calculate the interest amount based on the remaining balance and the annual interest rate
#         monthly_interest_rate = interest_rate / 12 / 100
#         interest_amount = beginning_balance * monthly_interest_rate * remaining_months
#         return interest_amount

#     def calculate_emi_1(self, beginning_balance, remaining_months, interest_rate):
#         monthly_interest_rate = interest_rate / 12 / 100
#         emi = (beginning_balance * monthly_interest_rate * ((1 + monthly_interest_rate) ** remaining_months)) / (((1 + monthly_interest_rate) ** remaining_months) - 1)
#         return emi
      
#     def load_entered_values(self, entered_values):
#         if entered_values:
#             # Load previously entered values into the form fields
#             self.entered_loan_amount = entered_values.get('loan_amount', None)
#             self.entered_tenure = entered_values.get('tenure', None)
#             self.entered_payment_type = entered_values.get('payment_type', None)

#     def calculate_payment_date(self, selected_row, current_month):
#         loan_updated_status = selected_row['loan_updated_status'].lower()
#         print("Loan Updated Status:", loan_updated_status)

#         if loan_updated_status in ['close', 'closed loans', 'disbursed loan', 'foreclosure']:
#             try:
#                 loan_disbursed_timestamp = selected_row['loan_disbursed_timestamp']
#                 emi_payment_type = selected_row['emi_payment_type']

#                 if loan_disbursed_timestamp:
#                     print("Loan Disbursed Timestamp:", loan_disbursed_timestamp)

#                     if emi_payment_type == 'Monthly':
#                         # Add months based on current month
#                         payment_date = loan_disbursed_timestamp + timedelta(days=current_month * 30)
#                     elif emi_payment_type == 'One Time':
#                         # Payment date is set for the first month only
#                         payment_date = loan_disbursed_timestamp + timedelta(days=30)  # Assuming 30 days per month
#                     elif emi_payment_type == 'Three Month':
#                         # Add 3 months to the loan disbursal date
#                         payment_date = loan_disbursed_timestamp + timedelta(days=current_month * 90)
#                     elif emi_payment_type == 'Six Month':
#                         # Add 6 months to the loan disbursal date
#                         payment_date = loan_disbursed_timestamp + timedelta(days=current_month * 180)
#                     else:
#                         payment_date = None

#                     return payment_date
#                 else:
#                     print("Loan Disbursed Timestamp is None")
#                     return None
#             except Exception as e:
#                 print(f"Error in calculate_payment_date: {e}")
#                 return None
#         else:
#             print("Loan Updated Status not in expected list")
#             return None

#     def calculate_monthly_emi_and_balance(self, selected_row, current_month):
#       emi = self.calculate_emi(selected_row)
#       beginning_balance = selected_row['total_repayment_amount']
  
#       # Initialize Total Repayment Beginning Balance (TRBB) and Total Repayment Ending Balance (TREB)
#       beginning_loan_amount_balance = selected_row['loan_amount']
#       processing_fee = selected_row['total_processing_fee_amount'] / selected_row['tenure'] if selected_row['total_processing_fee_amount'] is not None else 0
#       # For monthly payments, calculate ending balance
#       for month in range(1, current_month + 1):
#           interest_amount = beginning_loan_amount_balance * (selected_row['interest_rate'] / 100) / 12
#           principal_amount = emi - interest_amount
#           beginning_loan_amount_balance -= principal_amount  # Update TRBB for the next iteration
#           ending_loan_amount_balance = beginning_loan_amount_balance
#           beginning_balance -= emi + processing_fee # Update beginning balance for the next iteration
#           processing_fee_per_month = (selected_row['total_processing_fee_amount'] / selected_row['tenure']) 
#       ending_balance = beginning_balance

#       return emi, interest_amount, ending_balance, ending_loan_amount_balance,processing_fee_per_month

#     def calculate_three_month_emi_and_balance(self, selected_row, current_month):
#       emi = self.calculate_emi(selected_row)
#       emi = emi * 3
#       beginning_balance = selected_row['total_repayment_amount']
  
#       # Initialize Total Repayment Beginning Balance (TRBB) and Total Repayment Ending Balance (TREB)
#       beginning_loan_amount_balance = selected_row['loan_amount']
#       ending_loan_amount_balance = beginning_loan_amount_balance
  
#       # Since processing fee is a one-time charge, apply it only at the beginning
#       processing_fee = selected_row['total_processing_fee_amount'] if selected_row['total_processing_fee_amount'] is not None else 0
  
#       # Subtract processing fee from the total repayment amount at the beginning
#       beginning_balance -= processing_fee
  
#       # Calculate ending balance for the current month
#       for period in range(1, current_month + 1):
#           interest_amount = beginning_loan_amount_balance * (selected_row['interest_rate'] / 100) / (12 * 3)
#           principal_amount = emi - interest_amount
#           beginning_loan_amount_balance -= principal_amount  # Update TRBB for the next iteration
#           ending_loan_amount_balance = beginning_loan_amount_balance
#           beginning_balance -= emi  # Update beginning balance for the next iteration
#           processing_fee_per_month  = selected_row['total_processing_fee_amount'] / (selected_row['tenure'] // 3)
#       ending_balance = beginning_balance
#       return emi, interest_amount, ending_balance, ending_loan_amount_balance,processing_fee_per_month
        
#     def calculate_six_month_emi_and_balance(self, selected_row, current_month):
#       emi = self.calculate_emi(selected_row)
#       emi = emi * 6
#       beginning_balance = selected_row['total_repayment_amount']
  
#       # Initialize Total Repayment Beginning Balance (TRBB) and Total Repayment Ending Balance (TREB)
#       beginning_loan_amount_balance = selected_row['loan_amount']
#       ending_loan_amount_balance = beginning_loan_amount_balance
  
#       # Since processing fee is a one-time charge, apply it only at the beginning
#       processing_fee = selected_row['total_processing_fee_amount'] if selected_row['total_processing_fee_amount'] is not None else 0
  
#       # Subtract processing fee from the total repayment amount at the beginning
#       beginning_balance -= processing_fee
  
#       # For six-month payments, calculate ending balance for each 6-month period
#       for period in range(1, current_month + 1):
#           interest_amount = beginning_loan_amount_balance * (selected_row['interest_rate'] / 100) / (12 * 6)
#           principal_amount = emi - interest_amount
#           beginning_loan_amount_balance -= principal_amount  # Update TRBB for the next iteration
#           ending_loan_amount_balance = beginning_loan_amount_balance
#           beginning_balance -= emi   # Update beginning balance for the next iteration
#           processing_fee_per_month  = selected_row['total_processing_fee_amount'] / (selected_row['tenure'] // 6)
#       ending_balance = beginning_balance
#       return emi, interest_amount, ending_balance, ending_loan_amount_balance,processing_fee_per_month
  
  
#     def calculate_one_time_emi_and_balance(self, selected_row, current_month):
#         emi = self.calculate_emi(selected_row)
#         beginning_balance = selected_row['total_repayment_amount']
    
#         # Initialize Total Repayment Beginning Balance (TRBB) and Total Repayment Ending Balance (TREB)
#         beginning_loan_amount_balance = selected_row['loan_amount']
#         ending_loan_amount_balance = beginning_loan_amount_balance
    
#         # For one-time payment, calculate ending balance for the single payment
#         interest_amount = beginning_loan_amount_balance * (selected_row['interest_rate'] / 100) / 12
#         principal_amount = emi - interest_amount
#         beginning_loan_amount_balance -= principal_amount  # Update TRBB for the next iteration
#         ending_loan_amount_balance = beginning_loan_amount_balance
#         beginning_balance -= emi  # Update beginning balance for the next iteration
#         processing_fee_per_month = selected_row['total_processing_fee_amount']
#         ending_balance = beginning_balance
#         return emi, interest_amount, ending_balance, ending_loan_amount_balance,processing_fee_per_month
        
#     def calculate_num_payments(self, selected_row):
#       tenure = selected_row['tenure']
#       payment_type = selected_row['emi_payment_type']
  
#       if payment_type == 'One Time':
#           return 1
#       elif payment_type == 'Monthly':
#           return tenure
#       elif payment_type == 'Three Month':
#           num_payments = tenure // 3
#           return num_payments
#       elif payment_type == 'Six Month':
#           num_payments = tenure // 6
#           return num_payments
#       else:
#           return 0

#     def calculate_emi(self, selected_row, tenure=None, repayment_amount=None):
#         tenure = selected_row['tenure'] if tenure is None else tenure
#         monthly_interest_rate = (selected_row['interest_rate'] / 100) / 12
#         loan_amount = selected_row['loan_amount'] - repayment_amount if repayment_amount else selected_row['loan_amount']
    
#         if selected_row['emi_payment_type'] == 'Monthly':
#             emi = (loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** tenure)) / (((1 + monthly_interest_rate) ** tenure) - 1)
#         elif selected_row['emi_payment_type'] == 'One Time':
#             emi = selected_row['total_repayment_amount']
#         elif selected_row['emi_payment_type'] == 'Three Month':
#             monthly_interest_rate = (selected_row['interest_rate'] / 100) / (12)  # Convert annual interest rate to monthly
#             emi = (loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** (tenure ))) / (((1 + monthly_interest_rate) ** (tenure)) - 1)
#         elif selected_row['emi_payment_type'] == 'Six Month':
#             monthly_interest_rate = (selected_row['interest_rate'] / 100) / (12 )  # Corrected calculation for 6 months
#             emi = (loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** (tenure ))) / (((1 + monthly_interest_rate) ** (tenure )) - 1)
#         else:
#             emi = 0  # Handle unsupported payment types
    
#         return emi

#     def button_1_click(self, **event_args):
#         """This method is called when the button is clicked"""
#         open_form('borrower_registration_form.dashboard')

#     def button_2_click(self, **event_args):
#         """This method is called when the button is clicked"""
#         open_form('borrower_registration_form.dashboard.today_dues', selected_row=self.selected_row)



from ._anvil_designer import payment_details_extensionTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import timedelta

class payment_details_extension(payment_details_extensionTemplate):
    def __init__(self, selected_row=None, loan_extension_months=None, extension_fee=None, **properties):
        self.selected_row = selected_row
        self.loan_extension_months = loan_extension_months
        self.extension_fee = extension_fee
        self.init_components(**properties)

        if selected_row:
            self.load_payment_details(selected_row)

    def load_payment_details(self, selected_row):
        self.load_entered_values()
        payment_details = []
        
        entered_extension_months = self.loan_extension_months
        total_tenure = selected_row['tenure'] + entered_extension_months
        
        monthly_interest_rate = (selected_row['interest_rate'] / 100) / 12
        
        beginning_balance = selected_row['loan_amount']
        
        extension_fee_percentage = self.extension_fee if self.extension_fee is not None else selected_row.get('extension_fee', 0)
        extension_fee_amount = (extension_fee_percentage / 100) * selected_row['loan_amount']
        
        # Find the last paid EMI number for the specific loan
        last_paid_emi_records = app_tables.fin_emi_table.search(loan_id=selected_row['loan_id'], scheduled_payment_made=q.not_(None))
        last_paid_emi_number = max([record['emi_number'] for record in last_paid_emi_records], default=0)
        print("last_paid_emi_number", last_paid_emi_number)
        last_paid_emi_ending_balance = selected_row['loan_amount']
        
        # Counter for payment number
        # payment_number_counter = last_paid_emi_number + 1
        payment_number_counter =   1
        
        # Adjust the total tenure to include extension months
        for month in range(1, total_tenure + 1):
            emi = 0  # Assign a default value
            payment_date = self.calculate_payment_date(selected_row, month)
            loan_id = selected_row['loan_id']
            emi_number = payment_number_counter
            emi_row = app_tables.fin_emi_table.get(loan_id=loan_id, emi_number=emi_number)
        
            if emi_row is not None:
                scheduled_payment_made = emi_row['scheduled_payment_made']
                account_number = emi_row['account_number']
            else:
                scheduled_payment_made = None
                account_number = None
        
            formatted_payment_date = f"{payment_date:%Y-%m-%d}" if payment_date else "Awaiting Update"
        
            if month <= last_paid_emi_number:
                # emi = self.calculate_scheduled_payment(selected_row['loan_amount'], monthly_interest_rate, selected_row['tenure'])
                # total_payment = emi  
                if selected_row['emi_payment_type'] == 'Monthly':
                    emi = self.calculate_scheduled_payment(selected_row['loan_amount'], monthly_interest_rate, selected_row['tenure'])
                elif selected_row['emi_payment_type'] == 'One Time':
                    pass
                elif selected_row['emi_payment_type'] == 'Three Month':
                    
                    emi = self.calculate_scheduled_payment(selected_row['loan_amount'], monthly_interest_rate, (selected_row['tenure']/3))
                elif selected_row['emi_payment_type'] == 'Six Month':
                  
                    emi = self.calculate_scheduled_payment(selected_row['loan_amount'], monthly_interest_rate, (selected_row['tenure']/6))
                total_payment = emi              
            else:
                if selected_row['emi_payment_type'] == 'Monthly':
                    emi = self.calculate_scheduled_payment(selected_row['loan_amount'], monthly_interest_rate, selected_row['tenure'])
                elif selected_row['emi_payment_type'] == 'One Time':
                    pass
                elif selected_row['emi_payment_type'] == 'Three Month':
                    if (month - last_paid_emi_number) % 3 == 0:
                        emi = self.calculate_scheduled_payment(selected_row['loan_amount'], monthly_interest_rate, (total_tenure/3))
                elif selected_row['emi_payment_type'] == 'Six Month':
                    if (month - last_paid_emi_number) % 6 == 0:
                        emi = self.calculate_scheduled_payment(selected_row['loan_amount'], monthly_interest_rate, (total_tenure/6))
        
            # If the calculated emi is non-zero, calculate principal and other details
            if emi != 0:  
                total_payment = emi + extension_fee_amount if payment_number_counter == (last_paid_emi_number + 1) else emi
                # last_paid_emi_ending_balance += extension_fee_amount
                interest_amount = last_paid_emi_ending_balance * monthly_interest_rate
                principal_amount = emi - interest_amount
                ending_balance = last_paid_emi_ending_balance - principal_amount 
               
                payment_details.append({
                    'PaymentNumber': payment_number_counter,
                    'PaymentDate': formatted_payment_date,
                    'EMIDate': f"{scheduled_payment_made:%Y-%m-%d}" if scheduled_payment_made else "N/A",
                    'EMITime': f"{scheduled_payment_made:%I:%M %p}" if scheduled_payment_made else "N/A",
                    'AccountNumber': account_number if account_number else "N/A",
                    'ScheduledPayment': f"₹ {emi:.2f}",
                    'Principal': f"₹ {principal_amount:.2f}",
                    'Interest': f"₹ {interest_amount:.2f}",
                    'BeginningBalance': f"₹ {last_paid_emi_ending_balance :.2f}" if last_paid_emi_ending_balance else "N/A",
                    'ExtensionFee': f"₹ {extension_fee_amount:.2f}"  if payment_number_counter == (last_paid_emi_number + 1) else "₹ 0.00",
                    'TotalPayment': f"₹ {total_payment:.2f}",
                    'EndingBalance': f"₹ {ending_balance:.2f}"
                })
        
                last_paid_emi_ending_balance = ending_balance
                payment_number_counter += 1  # Increment payment number
        
        self.repeating_panel_1.items = payment_details


    def load_entered_values(self):
        self.entered_loan_amount = self.selected_row['loan_amount']
        self.entered_tenure = self.selected_row['tenure']
        self.entered_extension_months = self.loan_extension_months


    def calculate_payment_date(self, selected_row, current_month):
        loan_updated_status = selected_row['loan_updated_status'].lower()
    
        if loan_updated_status in ['close', 'closed loans', 'disbursed loan', 'foreclosure']:
            loan_disbursed_timestamp = selected_row['loan_disbursed_timestamp']
            loan_id = selected_row['loan_id']
    
            # Search for the row in fin_emi_table based on the loan_id
            rows = app_tables.fin_emi_table.search(loan_id=loan_id)
    
            if rows:
                # Find the last paid EMI number
                last_paid_emi_number = max([record['emi_number'] for record in rows if record['scheduled_payment_made'] is not None], default=0)
    
                # Calculate the month difference from the last paid EMI
                months_difference = current_month - last_paid_emi_number
    
                if loan_disbursed_timestamp:
                    emi_payment_type = selected_row['emi_payment_type']
    
                    if emi_payment_type == 'Monthly':
                        payment_date = loan_disbursed_timestamp + timedelta(days=30 * current_month)
                    elif emi_payment_type == 'Three Month':
                        payment_date = loan_disbursed_timestamp + timedelta(days=90 * (months_difference // 3))
                    elif emi_payment_type == 'Six Month':
                        payment_date = loan_disbursed_timestamp + timedelta(days=180 * (months_difference // 6))
                    else:
                        payment_date = None
    
                    return payment_date
                else:
                    return None
            else:
                return None
        else:
            return None


    def calculate_scheduled_payment(self, loan_amount, monthly_interest_rate, remaining_tenure):
        emi = (loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** remaining_tenure)) / (
                ((1 + monthly_interest_rate) ** remaining_tenure) - 1)

        return emi

    # def calculate_emi(self, selected_row, tenure=None, repayment_amount=None):
    #     tenure = selected_row['tenure'] if tenure is None else tenure
    #     monthly_interest_rate = (selected_row['interest_rate'] / 100) / 12
    #     loan_amount = selected_row['loan_amount'] - repayment_amount if repayment_amount else selected_row['loan_amount']
    
    #     if selected_row['emi_payment_type'] == 'Monthly':
    #         emi = (loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** tenure)) / (((1 + monthly_interest_rate) ** tenure) - 1)
    #       # elif selected_row['emi_payment_type'] == 'One Time':
    #       #     emi = selected_row['total_repayment_amount']
    #     elif selected_row['emi_payment_type'] == 'Three Month':
    #         monthly_interest_rate = (selected_row['interest_rate'] / 100) / (12)  # Convert annual interest rate to monthly
    #         emi = (loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** (tenure ))) / (((1 + monthly_interest_rate) ** (tenure)) - 1)
    #     elif selected_row['emi_payment_type'] == 'Six Month':
    #         monthly_interest_rate = (selected_row['interest_rate'] / 100) / (12 )  # Corrected calculation for 6 months
    #         emi = (loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** (tenure ))) / (((1 + monthly_interest_rate) ** (tenure )) - 1)
    #     else:
    #         emi = 0  # Handle unsupported payment types
    
    #     return emi

    def button_1_click(self, **event_args):
        open_form('borrower_registration_form.dashboard.extension_loan_request.borrower_extension.extension2',
                  selected_row=self.selected_row, loan_extension_months=self.loan_extension_months, new_emi = self.emi)

    def button_2_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('borrower_registration_form.dashboard.extension_loan_request.borrower_extension', selected_row = self.selected_row)
