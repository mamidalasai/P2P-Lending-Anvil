import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


@anvil.server.callable()
def get_table_data():
    data = tables.app_tables.fin_loan_details.search()
    return data

@anvil.server.callable
def add_data(customer_id, email, password, name, number):
  tables.app_tables.users.add_row(email=email, password_hash=password)
  tables.app_tables.fin_user_profile.add_row(customer_id=customer_id, email_user=email, full_name=name, mobile=number)

@anvil.server.callable
def lender(name, gender, date_of_birth):
  tables.app_tables.fin_user_profile.add_row(full_name=name, gender=gender,date_of_birth=date_of_birth)
  
@anvil.server.callable
def login_data():
  data = tables.app_tables.users.search()
  return data
@anvil.server.callable
def profile():
  data = tables.app_tables.fin_user_profile.search()
  return data

@anvil.server.callable
def get_extension_data():
    data = tables.app_tables.fin_extends_loan.search()
    return data

@anvil.server.callable
def get_today_data():
  data=tables.app_tables.fin_emi_table.search()
  return data



email_user = []

@anvil.server.callable
def share_email(email):
    global email_user
    email_user.append(email)
    print(f"Received email: {email_user}, {email}")
    return email_user

@anvil.server.callable
def another_method():
    # Use the global variable directly
    print(email_user)
