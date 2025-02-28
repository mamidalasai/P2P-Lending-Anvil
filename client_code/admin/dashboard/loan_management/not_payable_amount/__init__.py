from ._anvil_designer import not_payable_amountTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class not_payable_amount(not_payable_amountTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.data = tables.app_tables.fin_loan_details.search()

    a = -1
    self.list_1 = []
    self.list_2 = []
    self.list_3 = []
    self.list_4 = []
    self.list_5 = []
    self.list_6 = []
    self.list_7 = []
    self.list_8 = []
    self.list_9 = []
    self.list_10 = []
    
    
    for i in self.data:
      a+=1
      self.list_1.append(i['loan_id'])
      self.list_2.append(i['borrower_customer_id'])
      self.list_3.append(i['borrower_full_name'])
      self.list_4.append(i['loan_updated_status'])
      self.list_5.append(i['lender_full_name'])
      self.list_6.append(i['lender_customer_id'])
      self.list_7.append(i['interest_rate'])
      self.list_8.append(i['tenure'])
      self.list_9.append(i['loan_amount'])
      self.list_10.append(i['lender_accepted_timestamp'])
    print(a)

    self.result = []
    self.index = []
    if a == -1:
      alert("No Data Available Here!")
    else:
      b = -1
      for i in self.list_4:
        b+=1
        if i == 'NPA' or i == 'Not Payable Amount':
          self.index.append(b)
          
      for i in self.index:
        self.result.append({'loan_id' : self.list_1[i], 'coustmer_id' : self.list_2[i], 'full_name' : self.list_3[i], 'loan_status' : self.list_4[i],'lendor_full_name' : self.list_5[i],'lender_customer_id':self.list_6[i],'interest_rate':self.list_7[i],'tenure':self.list_8[i],'loan_amount':self.list_9[i],'lender_timestamp':self.list_10[i]})

      self.repeating_panel_2.items = self.result

  def button_1_copy_click(self, **event_args):
    open_form('admin.dashboard.loan_management')
