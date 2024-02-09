import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
import base64
import os  # Import the os module for file existence check


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

@anvil.server.callable
def foreclosure_data():
  data = tables.app_tables.fin_foreclosure.search()
  return data

@anvil.server.callable
def share_email(email):
    # Get the existing email_user list from app_session or create a new one
    email_user = anvil.server.session.get('email_user', None)
    
    # Append the new email
    email_user = email
    
    # Save the updated email_user list to app_session
    anvil.server.session['email_user'] = email_user
    
    print(f"Received email: {email_user}, {email}")
    return email_user

@anvil.server.callable
def another_method():
    # Get the email_user list from app_session
    email_user = anvil.server.session.get('email_user', None)
    print(email_user)
    return email_user


import anvil.server

@anvil.server.callable
def save_file_to_database(file_path):
    with open(file_path, 'rb') as file:
        file_content = file.read()

    # Create an Anvil Media object
    media_object = anvil.server.Media(content_type="image/png", content=file_content)

    # Get the reference to your Anvil Data Table
    my_data_table = app_tables.fin_user_profile

    # Create a new row in the data table and set the media column
    new_row = my_data_table.add_row(aadhaar_photo=media_object)

    # Save the changes to the database
    anvil.server.session_data.tables.save_all()

    return new_row


