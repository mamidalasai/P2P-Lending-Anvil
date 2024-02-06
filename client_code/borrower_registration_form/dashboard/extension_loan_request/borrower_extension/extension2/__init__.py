from ._anvil_designer import extension2Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta

# class extension2(extension2Template):
#     def __init__(self, selected_row,loan_extension_months, new_emi, **properties):
#         # Set Form properties and Data Bindings.
#         self.init_components(**properties)
#         self.selected_row = selected_row
#         self.extension_months = loan_extension_months
#         self.new_emi = new_emi
#         self.label_23.text = f"{selected_row['loan_id']}"
#         self.mi_label.text = f"{selected_row['loan_amount']}"
#         total_payments_made = selected_row['total_payments_made']
#         print(total_payments_made)
#         total_loan_amount = selected_row['total_repayment_amount']
#         loan_amount = int(self.mi_label.text)

#         # Additional initialization code
#         tenure = selected_row['tenure']
#         tenure = int(tenure)
#         self.interest_rate = selected_row['interest_rate']
#         monthly_interest_rate = selected_row['interest_rate'] / (12 * 100)
#         factor = (1 + monthly_interest_rate) ** tenure
#         emi = loan_amount * monthly_interest_rate * factor / (factor - 1)
#         emi = int(emi)
#         monthly_installment = loan_amount / tenure
#         monthly_installment = int(monthly_installment)
#         print(f"loan_amount: {loan_amount}")
#         print(f"emi: {emi}")
#         print(f"monthly installment: {monthly_installment}")

#         product_id_to_search = selected_row['product_id']
#         data = tables.app_tables.fin_product_details.search(product_id=product_id_to_search)
#         self.extension_fee_lst = []
#         for i in data:
#             self.extension_fee_lst.append(i['extension_fee'])

#         self.extension_fee.text = self.extension_fee_lst[0]
#         extension_fee = int(self.extension_fee.text)
#         loan_amount = int(self.mi_label.text)
#         extension_amount = (extension_fee * loan_amount) / 100
#         print('extension_amount', extension_amount)
#         self.extension_amountt.text = extension_amount
#         emi_paid = total_payments_made * emi
#         print('emi_paid', emi_paid)
#         remaining_loan_amount = total_loan_amount - emi_paid
#         print('remaining_loan_amount', remaining_loan_amount)
#         outstanding_months = tenure - total_payments_made
#         print(outstanding_months)
#         # extension_months = selected_row['loan_extension_months']

#         # Calculate the new EMI amount for the extended period
#         total_extension_months = tenure + self.extension_months   # Including the current month
#         # new_emi_amount = (remaining_loan_amount ) / total_extension_months
#         # new_emi_amount += extension_amount

#         # Save the calculated values as instance variables for later use
#         self.total_extension_months = total_extension_months
#         # self.new_emi_amount = new_emi_amount
#         self.extension_fee_comp_value = extension_fee
#         self.remaining_loan_amount = remaining_loan_amount
#         self.total_extension_months = total_extension_months
#         self.final_repayment.text = f"₹ {remaining_loan_amount:.2f}"

#     def button_3_click(self, **event_args):
#         """This method is called when the button is clicked"""
#         if self.f_checkbox.checked:
#             # Get the reason entered by the user
#             reason = self.reason_textbox.text.strip()

#             if reason:
#                 app_tables.fin_extends_loan.add_row(
#                     loan_id=self.selected_row['loan_id'],
#                     borrower_full_name=self.selected_row['borrower_full_name'],
#                     loan_amount=self.selected_row['loan_amount'],
#                     extend_fee = self.extension_fee_comp_value,
#                     final_repayment_amount = self.remaining_loan_amount,
#                     extension_amount = self.extension_amountt.text,
#                     new_emi = self.new_emi,
#                     total_extension_months = self.total_extension_months,
#                     reason=reason,
#                     status='under process',
#                     extension_request_date = datetime.now()
#                 )
#                 alert("Extension request submitted successfully!", title="Success")
#                 open_form('borrower_registration_form.dashboard.extension_loan_request')
#             else:
#                 alert('Please enter a reason for extension.')
#         else:
#             alert('Please accept the Terms and Conditions.')

#     def button_1_click(self, **event_args):
#       """This method is called when the button is clicked"""
#       open_form('borrower_registration_form.dashboard')

#     def button_2_click(self, **event_args):
#       """This method is called when the button is clicked"""
#       open_form('borrower_registration_form.dashboard.extension_loan_request.borrower_extension', selected_row = self.selected_row)



class extension2(extension2Template):
    def __init__(self, selected_row,loan_extension_months, new_emi, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.selected_row = selected_row
        self.extension_months = loan_extension_months
        self.new_emi = new_emi
        self.label_23.text = f"{selected_row['loan_id']}"
        self.mi_label.text = f"{selected_row['loan_amount']}"

        loan_id = selected_row['loan_id']
        # Fetching the last row data for the specified loan_id from the fin_emi_table
        last_emi_rows = app_tables.fin_emi_table.search(loan_id=loan_id)
        if last_emi_rows:
            # Convert LiveObjectProxy to list
            last_emi_list = list(last_emi_rows)
        
            # Sort the list of rows based on the 'emi_number' column in reverse order
            last_emi_list.sort(key=lambda x: x['emi_number'], reverse=True)
        
            # Extract the 'emi_number' from the first row, which represents the highest 'emi_number'
            total_payments_made = last_emi_list[0]['emi_number']
        else:
            total_payments_made = 0

        print("total payment made", total_payments_made)
        total_loan_amount = selected_row['total_repayment_amount']
        loan_amount = int(self.mi_label.text)

        # Additional initialization code
        tenure = selected_row['tenure']
        tenure = int(tenure)
        self.interest_rate = selected_row['interest_rate']
        monthly_interest_rate = selected_row['interest_rate'] / (12 * 100)
        factor = (1 + monthly_interest_rate) ** tenure
        emi = loan_amount * monthly_interest_rate * factor / (factor - 1)
        emi = int(emi)
        monthly_installment = loan_amount / tenure
        monthly_installment = int(monthly_installment)
        print(f"loan_amount: {loan_amount}")
        print(f"emi: {emi}")
        print(f"monthly installment: {monthly_installment}")

        product_id_to_search = selected_row['product_id']
        data = tables.app_tables.fin_product_details.search(product_id=product_id_to_search)
        self.extension_fee_lst = []
        for i in data:
            self.extension_fee_lst.append(i['extension_fee'])

        self.extension_fee.text = self.extension_fee_lst[0]
        extension_fee = int(self.extension_fee.text)
        loan_amount = int(self.mi_label.text)
        extension_amount = (extension_fee * loan_amount) / 100
        print('extension_amount', extension_amount)
        self.extension_amountt.text = extension_amount
        emi_paid = total_payments_made * emi
        print('emi_paid', emi_paid)
        remaining_loan_amount = total_loan_amount - emi_paid
        print('remaining_loan_amount', remaining_loan_amount)
        outstanding_months = tenure - total_payments_made
        print(outstanding_months)
        # extension_months = selected_row['loan_extension_months']

        # Calculate the new EMI amount for the extended period
        total_extension_months = tenure + self.extension_months   # Including the current month
        # new_emi_amount = (remaining_loan_amount ) / total_extension_months
        # new_emi_amount += extension_amount

        # Save the calculated values as instance variables for later use
        self.total_extension_months = total_extension_months
        # self.new_emi_amount = new_emi_amount
        self.extension_fee_comp_value = extension_fee
        self.remaining_loan_amount = remaining_loan_amount
        self.total_extension_months = total_extension_months
        self.final_repayment.text = f" {remaining_loan_amount:.2f}"
        self.new_emii.text = f" {new_emi:.2f}"

    def button_3_click(self, **event_args):
        """This method is called when the button is clicked"""
        if self.f_checkbox.checked:
            # Get the reason entered by the user
            reason = self.reason_textbox.text.strip()

            if reason:
                app_tables.fin_extends_loan.add_row(
                    loan_id=self.selected_row['loan_id'],
                    borrower_full_name=self.selected_row['borrower_full_name'],
                    loan_amount=self.selected_row['loan_amount'],
                    borrower_customer_id = str(self.selected_row['borrower_customer_id']),
                    borrower_email_id = str(self.selected_row['borrower_email_id']),
                    extend_fee = self.extension_fee_comp_value,
                    final_repayment_amount = float(self.final_repayment.text),
                    extension_amount = self.extension_amountt.text,
                    new_emi = float(self.new_emii.text),
                    total_extension_months = self.total_extension_months,
                    reason=reason,
                    status='under process',
                    extension_request_date = datetime.now()
                )
                alert("Extension request submitted successfully!", title="Success")
                open_form('borrower_registration_form.dashboard.extension_loan_request')
            else:
                alert('Please enter a reason for extension.')
        else:
            alert('Please accept the Terms and Conditions.')

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('borrower_registration_form.dashboard')

    def button_2_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('borrower_registration_form.dashboard.extension_loan_request.borrower_extension', selected_row = self.selected_row)
