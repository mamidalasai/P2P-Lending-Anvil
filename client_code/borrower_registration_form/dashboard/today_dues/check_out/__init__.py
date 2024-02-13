from ._anvil_designer import check_outTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta
from .. import main_form_module as main_form_module
from datetime import date

class check_out(check_outTemplate):
    def __init__(self, selected_row, **properties):
        self.selected_row = selected_row
        self.user_id = main_form_module.userId
        self.init_components(**properties)
  
        loan_id = selected_row['loan_id']
        extension_amount = self.get_extension_amount(loan_id, selected_row['emi_number'])
  
        loan_amount = selected_row['loan_amount']
        tenure = selected_row['tenure']
        interest_rate = selected_row['interest_rate']
        emi_payment_type = selected_row['emi_payment_type']
  
        monthly_interest_rate = interest_rate / 12 / 100
        total_payments = tenure * 12
  
        if emi_payment_type == 'One Time':
            emi = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** 12) / ((1 + monthly_interest_rate) ** 12 - 1)
            total_emi = emi + extension_amount  # Add extension amount to 12-month EMI total
        elif emi_payment_type == 'Monthly':
            # Calculate monthly EMI amount
            emi = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** total_payments) / ((1 + monthly_interest_rate) ** total_payments - 1)
            total_emi = emi + extension_amount  # Add extension amount to monthly EMI
        elif emi_payment_type == 'Three Month':
            # Calculate EMI amount for 3 months
            emi = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** 3) / ((1 + monthly_interest_rate) ** 3 - 1)
            total_emi = emi + extension_amount  # Add extension amount to 3-month EMI
        elif emi_payment_type == 'Six Month':
            # Calculate EMI amount for 6 months
            emi = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** 6) / ((1 + monthly_interest_rate) ** 6 - 1)
            total_emi = emi + extension_amount  # Add extension amount to 6-month EMI
        else:
            # Default to monthly calculation
            emi = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** total_payments) / ((1 + monthly_interest_rate) ** total_payments - 1)
            total_emi = emi + extension_amount  # Add extension amount to monthly EMI
  
        # Display the calculated EMI amount in the EMI amount label
        self.emi_amount_label.text = "{:.2f}".format(emi)  # Show only the EMI amount without extension
  
        # Update labels based on the presence of extension amount
        if extension_amount > 0:
            self.total_emi_amount_label.text = "{:.2f}".format(total_emi)
            self.extension_amount_label.text = "{:.2f}".format(extension_amount)
            self.total_emi_amount_label.visible = True
            self.extension_amount_label.visible = True
            self.label_6.visible = True
            self.label_3.visible = True
        else:
            self.total_emi_amount_label.visible = False
            self.extension_amount_label.visible = False
            self.label_6.visible = False
            self.label_3.visible = False
  
        # Update other labels
        self.loan_id_label.text = str(selected_row['loan_id'])
        self.loan_amount_label.text = str(loan_amount)
        self.interest_label.text = str(interest_rate)
        self.tenure_label.text = str(tenure)
        self.account_no_label.text = str(selected_row['account_number'])
  
        # Display total EMI amount including extension amount
        self.update_total_emi_amount(total_emi)

    def get_extension_amount(self, loan_id, emi_number):
        extension_row = app_tables.fin_extends_loan.get(
            loan_id=loan_id,
            emi_number=emi_number
        )
        if extension_row is not None:
            extension_amount = extension_row['extension_amount']
            if extension_amount is not None:
                return extension_amount
        return 0

    def update_total_emi_amount(self, total_emi):
        self.total_emi_amount_label.text = "{:.2f}".format(total_emi)

    def get_first_payment_due_date(self, loan_id):
        loan_row = app_tables.fin_loan_details.get(loan_id=loan_id)
        if loan_row is not None:
            return loan_row['first_emi_payment_due_date']
        else:
            return None  # or handle the case where the loan ID is not found

    def pay_now_click(self, **event_args):
        total_emi_amount = float(self.total_emi_amount_label.text)  # Fetch total EMI amount including extra payment
        borrower_wallet = app_tables.fin_wallet.get(customer_id=self.user_id)

        if borrower_wallet is not None:
            wallet_balance = borrower_wallet['wallet_amount']

            if wallet_balance >= total_emi_amount:
                updated_balance = wallet_balance - total_emi_amount
                borrower_wallet['wallet_amount'] = updated_balance
                borrower_wallet.update()

                # Retrieve lender's wallet based on lender_customer_id
                lender_wallet = app_tables.fin_wallet.get(customer_id=self.selected_row['lender_customer_id'])
                if lender_wallet is not None:
                    lender_balance = lender_wallet['wallet_amount']

                    # If lender_balance is None, treat it as zero
                    if lender_balance is None:
                        lender_balance = 0

                    lender_balance += total_emi_amount  # Add deducted amount to lender's wallet
                    lender_wallet['wallet_amount'] = lender_balance
                    lender_wallet.update()

                    loan_id = self.selected_row['loan_id']
                    current_emi_number = int(self.selected_row['emi_number'])
                    account_number = self.selected_row['account_number']
                    emi_payment_type = self.selected_row['emi_payment_type']
                    tenure = self.selected_row['tenure']

                    prev_scheduled_payment = self.selected_row['scheduled_payment']
                    prev_next_payment = self.selected_row['next_payment']

                    # # Check if the current scheduled payment is the same as the first payment due date
                    # is_first_payment_due_date = (prev_scheduled_payment == self.get_first_payment_due_date(loan_id=loan_id))

                    # Calculate next scheduled payment based on emi_payment_type
                    if emi_payment_type in ['One Time', 'Monthly', 'Three Month', 'Six Month']:
                        
                        if emi_payment_type == 'Monthly':
                            next_scheduled_payment = prev_scheduled_payment + timedelta(days=30)
                            next_next_payment = prev_next_payment + timedelta(days=30)
                        elif emi_payment_type == 'Three Month':
                            next_scheduled_payment = prev_scheduled_payment + timedelta(days=90)
                            next_next_payment = prev_next_payment + timedelta(days=90)
                            # Reduce the scheduled payment by 3 months
                            # next_scheduled_payment -= timedelta(days=90)
                        elif emi_payment_type == 'Six Month':
                            next_scheduled_payment = prev_scheduled_payment + timedelta(days=180)
                            next_next_payment = prev_next_payment + timedelta(days=180)
                        elif emi_payment_type == 'One Time':
                          if tenure:
                            next_scheduled_payment = prev_scheduled_payment + timedelta(days=30 * tenure)
                            next_next_payment = self.selected_row['next_payment'] + timedelta(days=30 * tenure)                
                    else:
                        # Default to monthly calculation
                        next_scheduled_payment = prev_scheduled_payment + timedelta(days=30)
                        next_next_payment = prev_next_payment + timedelta(days=30)

                    # Add a new row to fin_emi_table
                    new_emi_row = app_tables.fin_emi_table.add_row(
                        loan_id=loan_id,
                        emi_number=current_emi_number + 1,
                        account_number=account_number,
                        scheduled_payment_made=datetime.now(),
                        scheduled_payment=next_scheduled_payment,
                        next_payment=next_next_payment
                    )

                    # Update the emi_number and next_payment in the selected_row
                    self.selected_row['emi_number'] = current_emi_number + 1
                    self.selected_row['next_payment'] = next_next_payment
                    self.selected_row.update()

                    self.status_label.text = "Payment successfully done..."
                    self.button_1_copy_3.visible = False
                else:
                    self.status_label.text = "Lender's wallet not found."
            else:
                alert("Insufficient funds in wallet. Please deposit more funds to continue.")
                open_form('wallet.wallet')
        else:
            self.status_label.text = "Wallet record not found."

    def button_1_copy_2_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('borrower_registration_form.dashboard.today_dues')

