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


# In your server-side code

import anvil.server

@anvil.server.callable
def update_table_with_file(file_path, other_data):
    # Update your Anvil data table with the file path and other data
    # Replace 'YourDataTable' with the actual name of your data table

    # Example: assuming you have a data table called 'FileData'
    file_data = app_tables.fin_user_profile.get(aadhaar_photo=file_path)

    if file_data is not None:
        # Update existing record
        file_data['pan_photo'] = other_data
        file_data.save()
    else:
        # Create a new record
        app_tables.fin_user_profile.add_row(aadhaar_photo=file_path, pan_photo=other_data)

@anvil.server.callable
def handle_file_upload(file):
    # Specify the path where you want to save the file
    file_path = '/path/to/save/' + file.name

    with open(file_path, 'wb') as f:
        f.write(file.get_bytes())

    # Update the Anvil data table with the file path and any other relevant data
    update_table_with_file(file_path, "Additional Data")


