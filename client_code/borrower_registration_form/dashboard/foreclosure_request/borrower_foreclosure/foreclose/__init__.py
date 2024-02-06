# # from ._anvil_designer import forecloseTemplate
# # from anvil import *
# # import anvil.server
# # import anvil.google.auth, anvil.google.drive
# # from anvil.google.drive import app_files
# # import anvil.users
# # import anvil.tables as tables
# # import anvil.tables.query as q
# # from anvil.tables import app_tables
# # from datetime import datetime

# # class foreclose(forecloseTemplate):
# #   def __init__(self, selected_row, **properties):
# #     # Set Form properties and Data Bindings.
# #     self.init_components(**properties)
# #     self.selected_row = selected_row 
# #     # Any code you write here will run before the form opens.
# #     loan_amount = int(selected_row['loan_amount'])
# #     total_payments_made = selected_row['total_payments_made']
# #     tenure = selected_row['tenure']  # Assuming tenure is given in months
# #     tenure = int(tenure)
# #     monthly_interest_rate = selected_row['interest_rate'] / (12 * 100)  # Assuming interest rate is in percentage
# #     factor = (1 + monthly_interest_rate) ** tenure  # Calculate (1 + r)^t without using pow
# #     emi = loan_amount * monthly_interest_rate * factor / (factor - 1)
# #     emi = int(emi)
# #     print("emi", emi)
# #     monthly_installment = loan_amount / tenure
# #     monthly_installment=int(monthly_installment)
# #     print(total_payments_made)
# #     paid_amount = emi * total_payments_made
# #     print("paid amount", paid_amount)
# #     paid_amount = int(paid_amount)
# #     monthly_interest_amount=emi-monthly_installment
# #     monthly_interest_amount=int( monthly_interest_amount)

# #     outstanding_amount= loan_amount - (monthly_installment*total_payments_made)
# #     outstanding_amount = int(outstanding_amount)
# #     oustanding_month = tenure-total_payments_made
# #     outstanding_amount_i_amount = monthly_interest_amount*oustanding_month
# #     outstanding_amount_i_amount = int(outstanding_amount_i_amount)
# #     total_outstanding_amount = outstanding_amount+outstanding_amount_i_amount
    
# #     product_id_to_search = selected_row['product_id']
# #     data = tables.app_tables.product_details.search(product_id=product_id_to_search)
    
# #     if data and len(data) > 0:
# #         # Fetch the first row (assuming there's only one row for the given product_id)
# #         first_row = data[0]
        
# #         foreclosure_fee = first_row['foreclosure_fee']
# #         self.foreclose_fee.text = str(foreclosure_fee)
        
# #         if foreclosure_fee == 0:
# #             Notification("Foreclosure not available for this loan").show()
        
# #         foreclose_fee = float(foreclosure_fee)
# #         foreclose_amount = outstanding_amount * (foreclose_fee / 100)
# #         total_due_amount = outstanding_amount + foreclose_amount
# #         total_due_amount = float(total_due_amount)
# #     else:
# #         Notification("Foreclosure fee information not available")
# #         foreclose_fee = 0
# #         foreclose_amount = 0

# #     self.ra_label.text = f"{outstanding_amount}"
# #     self.tda_label.text = f"{total_due_amount}"
# #     self.emi_label.text = f"{emi}"
# #     self.pa_label.text = f"{foreclose_amount}"
# #     self.paid_label.text = f"{paid_amount}"
# #     self.mi_label.text = f"{monthly_installment}"
# #     self.fir_label.text = f"{monthly_interest_amount}"
# #     self.label_20.text = f"{monthly_installment}"
# #     self.label_8.text = f"{outstanding_amount_i_amount}"
# #     self.label_18.text = f"{total_outstanding_amount} "
# #     self.label_17.text = f"{outstanding_amount}"
# #     self.label_23.text = f"({total_payments_made} months)"
# #     self.label_24.text = f"({oustanding_month} months)"
    
# #   def button_1_click(self, **event_args):
# #     """This method is called when the button is clicked"""
# #     open_form('bank_users.borrower_dashboard')

# #   def button_2_click(self, **event_args):
# #     """This method is called when the button is clicked"""
# #     open_form('bank_users.borrower_dashboard.borrower_foreclosure_request.borrower_foreclosure', selected_row= self.selected_row)

# #   def link_1_click(self, **event_args):
# #     """This method is called when the link is clicked"""
# #     alert('Submitting a foreclosure request implies acknowledgment and acceptance of financial and legal consequences, adhering to established timelines and communication protocols.')

# #   def button_3_click(self, **event_args):
# #     """This method is called when the button is clicked"""
# #     if self.f_checkbox.checked:
# #         # Get the reason entered by the user
# #         reason = self.reason_textbox.text.strip()

# #         if reason:
# #                 app_tables.foreclosure.add_row(
# #                     loan_id=self.selected_row['loan_id'],
# #                     borrower_name=self.selected_row['borrower_full_name'],
# #                     loan_amount=self.selected_row['loan_amount'],
# #                     outstanding_amount=self.ra_label.text,
# #                     total_due_amount=self.tda_label.text,
# #                     emi_amount=self.emi_label.text,
# #                     paid_amount=self.paid_label.text,
# #                     foreclose_amount=self.pa_label.text,
# #                     requested_on=datetime.now(),
# #                     reason=reason,
# #                     foreclose_fee= self.foreclose_fee,
# #                     interest_rate=self.interest_rate,
# #                     status="under process"
# #                 )

# #                 alert("The Foreclosure Statement will be processed within 15 working days from the date of request. Please place this request to know the principal amount outstanding for closure of loan and applicable charges. If you have provided your mobile number or email, we will inform you about the closure of your request by SMS or email respectively. Providing the mobile number or email here will not result in an update of your mobile number or email as recorded with us. KOTAK Bank does not take any responsibility, and will also not be liable, for your claims if the details provided by you are incorrect/incomplete.")

# #                 open_form('bank_users.borrower_dashboard.borrower_foreclosure_request')
# #         else:
# #             alert('Please enter a reason for foreclosure.')
# #     else:
# #         alert('Please accept the Terms and Conditions.')

# from ._anvil_designer import forecloseTemplate
# from anvil import *
# import anvil.server
# import anvil.google.auth, anvil.google.drive
# from anvil.google.drive import app_files
# import anvil.users
# import anvil.tables as tables
# import anvil.tables.query as q
# from anvil.tables import app_tables
# from datetime import datetime

# class foreclose(forecloseTemplate):
#   def __init__(self,selected_row, total_payments_made, **properties):
#     # Set Form properties and Data Bindings.
#     self.init_components(**properties)
#     self.selected_row = selected_row 
#     self.total_payments_made = total_payments_made
#         # Any code you write here will run before the form opens.
#     loan_amount = int(selected_row['loan_amount'])
#     # total_payments_made = selected_row['total_payments_made']
#     tenure = selected_row['tenure']  # Assuming tenure is given in months
#     tenure = int(tenure)
#     self.interest_rate = selected_row['interest_rate']
#     monthly_interest_rate = selected_row['interest_rate'] / (12 * 100)  # Assuming interest rate is in percentage
#     factor = (1 + monthly_interest_rate) ** tenure  # Calculate (1 + r)^t without using pow
#     emi = loan_amount * monthly_interest_rate * factor / (factor - 1)
#     emi = int(emi)
#     monthly_installment = loan_amount / tenure
#     monthly_installment = int(monthly_installment)
#     print(f"loan_amount: {loan_amount}")
#     print(f"emi: {emi}")
#     print(f"factor: {factor}")
#     # print(f"total payments made: {total_payments_made}")
#     paid_amount = emi * self.total_payments_made
#     print(f"emi: {emi}")
#     paid_amount = int(paid_amount)
#     monthly_interest_amount=emi-monthly_installment
#     monthly_interest_amount=int( monthly_interest_amount)

#     outstanding_amount= loan_amount - (monthly_installment*self.total_payments_made)
#     outstanding_amount = int(outstanding_amount)
#     oustanding_month = tenure-self.total_payments_made
#     outstanding_amount_i_amount = monthly_interest_amount*oustanding_month
#     outstanding_amount_i_amount = int(outstanding_amount_i_amount)
#     total_outstanding_amount = outstanding_amount+outstanding_amount_i_amount
    
#     product_id_to_search = selected_row['product_id']
#     data = tables.app_tables.fin_product_details.search(product_id=product_id_to_search)
#     self.foreclosure_fee_lst = []    
#     for i in data:
#         self.foreclosure_fee_lst.append(i['foreclosure_fee'])
      
#     foreclosure_fee_str = ', '.join(map(str, self.foreclosure_fee_lst))
#     self.foreclose_fee_component.text = foreclosure_fee_str
#     self.foreclose_fee = float(self.foreclose_fee_component.text)
#     foreclose_amount = outstanding_amount * (self.foreclose_fee/100)
#     foreclose_amount = float(foreclose_amount)
#     total_due_amount = outstanding_amount + foreclose_amount
#     total_due_amount = float(total_due_amount)

#     self.ra_label.text = f"{outstanding_amount}"
#     self.tda_label.text = f"{total_due_amount}"
#     self.emi_label.text = f"{emi}"
#     self.pa_label.text = f"{foreclose_amount}"
#     self.paid_label.text = f"{paid_amount}"
#     self.mi_label.text = f"{monthly_installment}"
#     self.fir_label.text = f"{monthly_interest_amount}"
#     self.label_20.text = f"{monthly_installment}"
#     self.label_8.text = f"{outstanding_amount_i_amount}"
#     self.label_18.text = f"{total_outstanding_amount} "
#     self.label_17.text = f"{outstanding_amount}"
#     self.label_23.text = f"({total_payments_made} months)"
#     self.label_24.text = f"({oustanding_month} months)"
    
#   def button_1_click(self, **event_args):
#     """This method is called when the button is clicked"""
#     open_form('borrower_registration_form.dashboard')

#   def button_2_click(self, **event_args):
#     """This method is called when the button is clicked"""
#     open_form('borrower_registration_form.dashboard.foreclosure_request.borrower_foreclosure', selected_row= self.selected_row)

#   def link_1_click(self, **event_args):
#     """This method is called when the link is clicked"""
#     alert('Submitting a foreclosure request implies acknowledgment and acceptance of financial and legal consequences, adhering to established timelines and communication protocols.')

#   def button_3_click(self, **event_args):
    
#     """This method is called when the button is clicked"""
#     if self.f_checkbox.checked:
#         # Get the reason entered by the user
#         reason = self.reason_textbox.text.strip()

#         if reason:           
#                 app_tables.fin_foreclosure.add_row(
#                     loan_id=self.selected_row['loan_id'],
#                     borrower_name=self.selected_row['borrower_full_name'],
#                     loan_amount=self.selected_row['loan_amount'],
#                     outstanding_amount=self.ra_label.text,
#                     total_due_amount=self.tda_label.text,
#                     emi_amount=self.emi_label.text,
#                     paid_amount=self.paid_label.text,
#                     foreclose_amount=self.pa_label.text,
#                     requested_on=datetime.now(),
#                     reason=reason,
#                     foreclose_fee = self.foreclose_fee,
#                     interest_rate = self.interest_rate,
#                     status="under process"
#                 )

#                 alert("The Foreclosure Statement will be processed within 15 working days from the date of request. Please place this request to know the principal amount outstanding for closure of loan and applicable charges. If you have provided your mobile number or email, we will inform you about the closure of your request by SMS or email respectively. Providing the mobile number or email here will not result in an update of your mobile number or email as recorded with us. KOTAK Bank does not take any responsibility, and will also not be liable, for your claims if the details provided by you are incorrect/incomplete.")

#                 open_form('borrower_registration_form.dashboard.foreclosure_request')
#         else:
#             alert('Please enter a reason for foreclosure.')
#     else:
#         alert('Please accept the Terms and Conditions.')


from ._anvil_designer import forecloseTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime

class foreclose(forecloseTemplate):
  def __init__(self,selected_row, total_payments_made, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.selected_row = selected_row 
    self.total_payments_made = total_payments_made
        # Any code you write here will run before the form opens.
    loan_amount = int(selected_row['loan_amount'])
    # total_payments_made = selected_row['total_payments_made']
    tenure = selected_row['tenure']  # Assuming tenure is given in months
    tenure = int(tenure)
    self.interest_rate = selected_row['interest_rate']
    monthly_interest_rate = selected_row['interest_rate'] / (12 * 100)  # Assuming interest rate is in percentage
    factor = (1 + monthly_interest_rate) ** tenure  # Calculate (1 + r)^t without using pow
    emi = loan_amount * monthly_interest_rate * factor / (factor - 1)
    emi = int(emi)
    monthly_installment = loan_amount / tenure
    monthly_installment = int(monthly_installment)
    print(f"loan_amount: {loan_amount}")
    print(f"emi: {emi}")
    print(f"factor: {factor}")
    # print(f"total payments made: {total_payments_made}")
    paid_amount = emi * self.total_payments_made
    print(f"emi: {emi}")
    paid_amount = int(paid_amount)
    monthly_interest_amount=emi-monthly_installment
    monthly_interest_amount=int( monthly_interest_amount)

    outstanding_amount= loan_amount - (monthly_installment*self.total_payments_made)
    outstanding_amount = int(outstanding_amount)
    oustanding_month = tenure-self.total_payments_made
    outstanding_amount_i_amount = monthly_interest_amount*oustanding_month
    outstanding_amount_i_amount = int(outstanding_amount_i_amount)
    total_outstanding_amount = outstanding_amount+outstanding_amount_i_amount
    
    product_id_to_search = selected_row['product_id']
    data = tables.app_tables.fin_product_details.search(product_id=product_id_to_search)
    self.foreclosure_fee_lst = []    
    for i in data:
        self.foreclosure_fee_lst.append(i['foreclosure_fee'])
      
    foreclosure_fee_str = ', '.join(map(str, self.foreclosure_fee_lst))
    self.foreclose_fee_component.text = foreclosure_fee_str
    self.foreclose_fee = float(self.foreclose_fee_component.text)
    foreclose_amount = outstanding_amount * (self.foreclose_fee/100)
    foreclose_amount = float(foreclose_amount)
    total_due_amount = outstanding_amount + foreclose_amount
    total_due_amount = float(total_due_amount)

    self.ra_label.text = f"{outstanding_amount}"
    self.tda_label.text = f"{total_due_amount}"
    self.emi_label.text = f"{emi}"
    self.pa_label.text = f"{foreclose_amount}"
    self.paid_label.text = f"{paid_amount}"
    self.mi_label.text = f"{monthly_installment}"
    self.fir_label.text = f"{monthly_interest_amount}"
    self.label_20.text = f"{monthly_installment}"
    self.label_8.text = f"{outstanding_amount_i_amount}"
    self.label_18.text = f"{total_outstanding_amount} "
    self.label_17.text = f"{outstanding_amount}"
    self.label_23.text = f"({total_payments_made} months)"
    self.label_24.text = f"({oustanding_month} months)"
    
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('borrower_registration_form.dashboard')

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('borrower_registration_form.dashboard.foreclosure_request.borrower_foreclosure', selected_row= self.selected_row)

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert('Submitting a foreclosure request implies acknowledgment and acceptance of financial and legal consequences, adhering to established timelines and communication protocols.')

  def button_3_click(self, **event_args):
    
    """This method is called when the button is clicked"""
    if self.f_checkbox.checked:
        # Get the reason entered by the user
        reason = self.reason_textbox.text.strip()

        if reason:           
                app_tables.fin_foreclosure.add_row(
                    loan_id=self.selected_row['loan_id'],
                    borrower_name=self.selected_row['borrower_full_name'],
                    loan_amount=self.selected_row['loan_amount'],
                    outstanding_amount = float(self.ra_label.text),
                    total_due_amount = float(self.tda_label.text),
                    emi_amount = float(self.emi_label.text),
                    paid_amount = float(self.paid_label.text),
                    foreclose_amount = float(self.pa_label.text),
                    requested_on=datetime.now(),
                    reason=reason,
                    foreclose_fee = float(self.foreclose_fee),
                    interest_rate = float(self.interest_rate),
                    status="under process"
                )

                alert("The Foreclosure Statement will be processed within 15 working days from the date of request. Please place this request to know the principal amount outstanding for closure of loan and applicable charges. If you have provided your mobile number or email, we will inform you about the closure of your request by SMS or email respectively. Providing the mobile number or email here will not result in an update of your mobile number or email as recorded with us. KOTAK Bank does not take any responsibility, and will also not be liable, for your claims if the details provided by you are incorrect/incomplete.")
                alert("Your Foreclosure request is submitted.")
                open_form('borrower_registration_form.dashboard.foreclosure_request')
        else:
            alert('Please enter a reason for foreclosure.')
    else:
        alert('Please accept the Terms and Conditions.')
