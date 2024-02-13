import anvil.google.auth
import anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.google.auth
import anvil.google.drive
from anvil.tables import app_tables
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
from anvil import DataGrid, alert, open_form
from datetime import datetime, timedelta
import anvil.server
from ._anvil_designer import payment_details_tTemplate

class payment_details_t(payment_details_tTemplate):
    def __init__(self, selected_row=None, entered_values=None, **properties):
        self.selected_row = selected_row
        self.init_components(**properties)

        if selected_row:
            self.load_payment_details(selected_row, entered_values)

    def load_payment_details(self, selected_row, entered_values):
        self.load_entered_values(entered_values)
        payment_details = []

        # Calculate number of payment details based on emi_payment_type
        num_payments = self.calculate_num_payments(selected_row)

        for month in range(1, num_payments + 1):
            payment_date = self.calculate_payment_date(selected_row, month)

            emi, ending_balance = self.calculate_emi_and_balance(selected_row, month)

            # Fetch extra payment from fin_extension_loan table
            extension_row = app_tables.fin_extends_loan.get(
                loan_id=selected_row['loan_id'],
                emi_number=month
            )
            extra_payment = extension_row['extension_amount'] if extension_row else 0

            # Fetch scheduled_payment_made and account_number from the emi_payments table
            emi_row = app_tables.fin_emi_table.get(
                loan_id=selected_row['loan_id'],
                emi_number=month
            )
            scheduled_payment_made = emi_row['scheduled_payment_made'] if emi_row else None
            account_number = emi_row['account_number'] if emi_row else None

            # Update beginning balance for the next iteration
            beginning_balance = selected_row['loan_amount'] if month == 1 else ending_balance

            # Calculate interest and principal amounts
            monthly_interest_rate = (selected_row['interest_rate'] / 100) / 12
            interest_amount = beginning_balance * monthly_interest_rate
            principal_amount = emi - interest_amount
            ending_balance = beginning_balance - principal_amount

            # Determine display values for EMIDate and AccountNumber
            scheduled_payment_made_display = f"{scheduled_payment_made:%Y-%m-%d}" if scheduled_payment_made else "N/A"
            emi_time_display = f"{scheduled_payment_made:%I:%M %p}" if scheduled_payment_made else "N/A"
            account_number_display = account_number if account_number else "N/A"

            # Format payment date
            formatted_payment_date = f"{payment_date:%Y-%m-%d}" if payment_date else "Awaiting Update"

            # Add payment details to the list
            payment_details.append({
                'PaymentNumber': month,
                'PaymentDate': formatted_payment_date,
                'EMIDate': scheduled_payment_made_display,
                'EMITime': emi_time_display,
                'AccountNumber': account_number_display,
                'ScheduledPayment': f"₹ {emi:.2f}",
                'Principal': f"₹ {principal_amount:.2f}",
                'Interest': f"₹ {interest_amount:.2f}",
                'BeginningBalance': f"₹ {beginning_balance:.2f}",
                'ExtraPayment': f"₹ {extra_payment:.2f}" if extra_payment is not None else "N/A",
                'TotalPayment': f"₹ {emi + extra_payment if extra_payment is not None else emi:.2f}",
                'EndingBalance': f"₹ {ending_balance:.2f}"
            })

        # Set the Data Grid's items property to the list of payment details
        self.repeating_panel_1.items = payment_details

    def load_entered_values(self, entered_values):
        if entered_values:
            # Load previously entered values into the form fields
            self.entered_loan_amount = entered_values.get('loan_amount', None)
            self.entered_tenure = entered_values.get('tenure', None)
            self.entered_payment_type = entered_values.get('payment_type', None)

    def calculate_payment_date(self, selected_row, current_month):
        loan_updated_status = selected_row['loan_updated_status'].lower()
        print("Loan Updated Status:", loan_updated_status)

        if loan_updated_status in ['close', 'closed loans', 'disbursed loan', 'foreclosure']:
            try:
                loan_disbursed_timestamp = selected_row['loan_disbursed_timestamp']
                emi_payment_type = selected_row['emi_payment_type']

                if loan_disbursed_timestamp:
                    print("Loan Disbursed Timestamp:", loan_disbursed_timestamp)

                    if emi_payment_type == 'Monthly':
                        # Add months based on current month
                        payment_date = loan_disbursed_timestamp + timedelta(days=current_month * 30)
                    elif emi_payment_type == 'One Time':
                        # Payment date is set for the first month only
                        payment_date = loan_disbursed_timestamp + timedelta(days=365)
                    elif emi_payment_type == 'Three Month':
                        # Add 3 months to the loan disbursal date
                        payment_date = loan_disbursed_timestamp + timedelta(days=current_month * 90)
                    elif emi_payment_type == 'Six Month':
                        # Add 6 months to the loan disbursal date
                        payment_date = loan_disbursed_timestamp + timedelta(days=current_month * 180)
                    else:
                        payment_date = None

                    return payment_date
                else:
                    print("Loan Disbursed Timestamp is None")
                    return None
            except Exception as e:
                print(f"Error in calculate_payment_date: {e}")
                return None
        else:
            print("Loan Updated Status not in expected list")
            return None

    def calculate_emi_and_balance(self, selected_row, current_month):
        emi = 0
        ending_balance = 0

        if selected_row['emi_payment_type'] == 'Monthly':
            # For monthly payments, calculate EMI and ending balance
            emi = self.calculate_emi(selected_row, current_month)
            ending_balance = selected_row['loan_amount'] - (emi * current_month)
        elif selected_row['emi_payment_type'] == 'One Time':
            # For one-time payment, calculate EMI and ending balance for the full tenure
            emi = self.calculate_emi(selected_row)
            ending_balance = selected_row['loan_amount'] - (emi * selected_row['tenure'])
        elif selected_row['emi_payment_type'] == 'Three Month':
            # For three-month payment, calculate EMI and ending balance for each 3-month period
            emi = self.calculate_emi(selected_row, current_month * 3)
            ending_balance = selected_row['loan_amount'] - (emi * current_month)
        elif selected_row['emi_payment_type'] == 'Six Month':
            # For six-month payment, calculate EMI and ending balance for each 6-month period
            emi = self.calculate_emi(selected_row, current_month * 6)
            ending_balance = selected_row['loan_amount'] - (emi * current_month)

        return emi, ending_balance

    def calculate_emi(self, selected_row, tenure=None):
        tenure = selected_row['tenure'] if tenure is None else tenure
        monthly_interest_rate = (selected_row['interest_rate'] / 100) / 12
        emi = (selected_row['loan_amount'] * monthly_interest_rate * ((1 + monthly_interest_rate) ** tenure)) / (
                ((1 + monthly_interest_rate) ** tenure) - 1)
        return emi

    def calculate_num_payments(self, selected_row):
        if selected_row['emi_payment_type'] == 'Monthly':
            return selected_row['tenure']
        elif selected_row['emi_payment_type'] == 'One Time':
            return 1
        elif selected_row['emi_payment_type'] == 'Three Month':
            return selected_row['tenure'] // 3
        elif selected_row['emi_payment_type'] == 'Six Month':
            return selected_row['tenure'] // 6
        else:
            return 0

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('borrower_registration_form.dashboard')

    def button_2_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('borrower_registration_form.dashboard.today_dues', selected_row=self.selected_row)
