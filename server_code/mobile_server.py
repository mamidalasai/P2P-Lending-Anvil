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

@anvil.server.callable
def upload_media(file_path, user_data):
    # Upload media and update user data
    data = tables.app_tables.fin_user_profile.search()
    with open(file_path, 'rb') as file:
        # Upload media to Anvil's media storage
        media_url = anvil.server._anvil_designer_media_upload(file.read(), 'image/jpeg')
    data[user_data]['aadhaar_photo'] = media_url


@anvil.server.callable
def add_media_to_user_profile(media_file):
    # Get the current user
    user = anvil.users.get_user()
    
    # Check if the user is authenticated
    if user:
        # Access the user's profile
        profile = app_tables.user_profile.get(user=user)
        
        # Check if the user profile exists
        if profile:
            # Add the media file to the "media" column in the user profile
            profile['media'] = media_file
            profile.save()
            
            return "Media file added to user profile successfully."
        else:
            raise Exception("User profile not found.")
    else:
        raise Exception("User not authenticated.")