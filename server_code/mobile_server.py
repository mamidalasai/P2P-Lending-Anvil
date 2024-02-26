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
import os  # Import the os module for file existence che
from anvil import *
import anvil.media
from anvil import Media

@anvil.server.callable()
def get_table_data():
    data = tables.app_tables.fin_loan_details.search()
    return data

@anvil.server.callable
def add_data(customer_id, email, password, name, number, enable):
  tables.app_tables.users.add_row(email=email, password_hash=password, enabled=enable)
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
    
    return email_user

@anvil.server.callable
def another_method():
    # Get the email_user list from app_session
    email_user = anvil.server.session.get('email_user', None)
    return email_user


@anvil.server.callable
def save_media_content(file_content, file_name):
    # Access the MediaTable Data Table
    media_table = anvil.server.get_table('fin_user_profile')
    
    # Create a new row in the Data Table
    new_row = media_table.add_row()
    
    # Set the value of the media column to the file content and file name
    new_row['pan_photo'] = Media(file_content, file_name)
    
    # Return the ID of the new row
    return new_row['fin_user_profile']
  
@anvil.server.callable
def get_foreclose_data( outstading_amount, forecloser_fee, forecloser_amount):
    tables.app_tables.fin_foreclosure.add_row(outstanding_amount=outstading_amount,foreclose_fee=forecloser_fee,foreclose_amount=forecloser_amount)



@anvil.server.callable
def get_credit_limit(customer_id):
    try:
        # Fetch all rows with the specified customer_id
        data = app_tables.fin_borrower.search(customer_id=customer_id)

        # If there is data for the specified customer_id, extract the 'credit_limit'
        credit_limit = data[0]['credit_limit'] if data else None

        return credit_limit
    except Exception as e:
        # Handle exceptions gracefully (log or print the error)
        print(f"An error occurred in get_credit_limit: {e}")
        return None

@anvil.server.callable
def get_max_tenure(selected_category):
    try:
        # Fetch all rows with the specified product_categories
        data = app_tables.fin_product_details.search(product_categories=selected_category)

        if data and len(data) > 0:
            # 'selected_category' is present in the 'product_categories' column
            max_tenure = data[0]['max_tenure']
            
            return max_tenure
        else:
            # 'selected_category' is not present in the 'product_categories' column
            
            return None
    except Exception as e:
        # Handle exceptions gracefully (log or print the error)
        print(f"An error occurred in get_max_tenure: {e}")
        return None

@anvil.server.callable
def get_details(selected_category):
    try:
        # Fetch all rows with the specified product_categories
        data = app_tables.fin_product_details.search(product_categories=selected_category)

        if data and len(data) > 0:
            # 'selected_category' is present in the 'product_categories' column
            processing_fee = data[0]['processing_fee']
            roi = data[0]['roi']
            
            return {'processing_fee':processing_fee, 'roi': roi}
        else:
            # 'selected_category' is not present in the 'product_categories' column
            
            return None
    except Exception as e:
        # Handle exceptions gracefully (log or print the error)
        print(f"An error occurred in get_details: {e}")
        return None

@anvil.server.callable
def calculate_emi(selected_category, loan_amount, loan_tenure):
    try:
        # Retrieve roi from the Anvil database
        fin_product_details = app_tables.fin_product_details.search(product_categories=selected_category)
        if fin_product_details:
            roi = fin_product_details[0]['roi']
            roi = float(roi)
        else:
            return "ROI not found for the selected category"

        # Convert loan_amount and loan_tenure to float
        loan_amount = float(loan_amount)
        loan_tenure=float(loan_tenure)
       

        if loan_tenure > 0:
            # Monthly Interest Rate
            monthly_interest_rate = (roi / 100) / 12

            # Number of Monthly Installments
            num_installments = loan_tenure

            # Calculate EMI using the formula
            emi = (loan_amount * monthly_interest_rate * pow(1 + monthly_interest_rate, num_installments)) / \
                  (pow(1 + monthly_interest_rate, num_installments) - 1)

            # Return the calculated EMI
            return emi

        else:
            return "Invalid tenure"

    except ValueError as e:
        print(f"An error occurred in calculate_emi: {e}")
        return "Error calculating EMI"

@anvil.server.callable
def calculate_total_repayment(selected_category, loan_amount, loan_tenure):
    try:
        # Retrieve roi from the Anvil database
        fin_product_details = app_tables.fin_product_details.search(product_categories=selected_category)
        if fin_product_details:
            roi = fin_product_details[0]['roi']
            roi = float(roi)
        else:
            return "ROI not found for the selected category"

        # Convert loan_amount and loan_tenure to float
        loan_amount = float(loan_amount)
        loan_tenure = float(loan_tenure)

       

        if loan_tenure > 0:
            # Monthly Interest Rate
            monthly_interest_rate = (roi / 100) / 12

            # Number of Monthly Installments
            num_installments = loan_tenure

            # Calculate EMI using the formula
            emi = (loan_amount * monthly_interest_rate * pow(1 + monthly_interest_rate, num_installments)) / \
                  (pow(1 + monthly_interest_rate, num_installments) - 1)

            # Calculate Total Repayment
            total_repayment = emi * num_installments

            # Return the calculated Total Repayment
            return total_repayment

        else:
            return "Invalid tenure"

    except ValueError as e:
        print(f"An error occurred in calculate_total_repayment: {e}")
        return "Error calculating Total Repayment"

@anvil.server.callable
def generate_loan_id():
    # Query the latest loan ID from the data table
    latest_loan = app_tables.fin_loan_details.search(tables.order_by("loan_id", ascending=False))

    if latest_loan and len(latest_loan) > 0:
        # If there are existing loans, increment the last loan ID
        last_loan_id = latest_loan[0]['loan_id']
        counter = int(last_loan_id[2:]) + 1
    else:
        # If there are no existing loans, start the counter at 100001
        counter = 1000001

    # Return the new loan ID
    return f"LA{counter}"

@anvil.server.callable
def add_loan_data(loan_amount, loan_tenure, roi, total_repayment, date_of_apply):
    try:
        # Assuming 'fin_loan_details' is the name of your Anvil table
        email = another_method()
        data = profile()
        email_list = []
        customer_id_list = []
        borrower_name_list = []
        for i in data:
          email_list.append(i['email_user'])
          customer_id_list.append(i['customer_id'])
          borrower_name_list.append(i['full_name'])
          
        if email in email_list:
          index = email_list.index(email)
        else:
          print("email not there")
        customer_id = customer_id_list[index]
        customer_name = borrower_name_list[index]
        loan_id = generate_loan_id()
        app_tables.fin_loan_details.add_row(
            borrower_customer_id=customer_id,
            borrower_full_name=borrower_name,
            loan_id=loan_id,
            loan_amount=float(loan_amount),
            tenure=float(loan_tenure),
            loan_updated_status = "under process",
            total_repayment_amount=float(total_repayment),
            interest_rate=float(roi),
        )

        # You can also return the loan ID if needed
        return loan_id
    except Exception as e:
        # Handle exceptions appropriately
        raise anvil.server.NoServerFunctionError(f"Anvil error: {e}")


