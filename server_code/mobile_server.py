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
  wallet = tables.app_tables.fin_wallet.search()
  wallet_amount = 0
  id_w = []
  for i in wallet:
      id_w.append(i['wallet_id'])

  if len(id_w) >= 1:
      wallet_id = 'WI' + str(int(id_w[-1][2:]) + 1)
  else:
      wallet_id = 'WI' + str(1000)
  print(wallet_id)
  tables.app_tables.users.add_row(email=email, password_hash=password, enabled=enable)
  tables.app_tables.fin_user_profile.add_row(customer_id=customer_id, email_user=email, full_name=name, mobile=number)
  tables.app_tables.fin_wallet.add_row(customer_id=customer_id, user_email=email, user_name=name, wallet_id=wallet_id, wallet_amount=wallet_amount)

@anvil.server.callable
def wallet_data():
  data = tables.app_tables.fin_wallet.search()
  return data

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
            borrower_full_name=customer_name,
            loan_id=loan_id,
            loan_amount=float(loan_amount),
            tenure=float(loan_tenure),
            loan_updated_status = "under process",
            total_repayment_amount=float(total_repayment),
            interest_rate=float(roi),
            borrower_loan_created_timestamp=date_of_apply,
            borrower_email_id=email
        )

        # You can also return the loan ID if needed
        return loan_id
    except Exception as e:
        # Handle exceptions appropriately
        raise anvil.server.NoServerFunctionError(f"Anvil error: {e}")

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
        counter = 1000

    # Return the new loan ID
    return f"LA{counter}"


@anvil.server.callable
def get_product_groups():
    try:
        product_groups = [product['product_group'] for product in app_tables.fin_product_details.search()]
        return product_groups
    except Exception as e:
        print(f"Error in get_product_groups: {e}")
        return []

@anvil.server.callable
def get_product_categories(product_group):
    try:
        # Check if the provided product_group is empty or invalid
        if not product_group or product_group not in {entry['product_group'] for entry in app_tables.fin_product_details.search()}:
            raise ValueError("Empty or invalid product_group")

        # Fetch product categories for the selected product group
        categories = [entry['product_categories'] for entry in app_tables.fin_product_details.search() if entry['product_group'] == product_group]

        # Return the result as a dictionary
        return {'product_categories': categories}

    except Exception as e:
        # Log the error and return an appropriate response
        print(f"Error in get_product_categories: {e}")
        return {'error': str(e)}

@anvil.server.callable
def get_product_names(product_group, product_category):
    try:
        # Check if the provided product_group and product_category are valid
        if not product_group or not product_category:
            raise ValueError("Empty or invalid product_group or product_category")

        # Fetch product names for the selected product group and category
        names = [entry['product_name'] for entry in app_tables.fin_product_details.search(
            product_group=product_group,
            product_categories=product_category
        )]

        # Return the result as a dictionary
        return {'product_name': names}

    except Exception as e:
        # Log the error and return an appropriate response
        print(f"Error in get_product_names: {e}")
        return {'error': str(e)}

@anvil.server.callable
def add_loan(product_id, product_name):
    try:
        # Assuming 'fin_loan_details' is the name of your Anvil table
        data = app_tables.fin_loan_details.add_row(
            product_id=str(product_id),
            product_name=product_name
        )

        # You can also return the loan ID if needed
        return data
        
            
    except Exception as e:
        # Handle other exceptions appropriately
        raise anvil.server.NoServerFunctionError(f"Anvil error: {e}")
@anvil.server.callable
def get_product():
    try:
        # Fetch all rows with the specified customer_id
        data = app_tables.fin_product_details.search()

        # If there is data for the specified product_id
        product = data[0]['product_id'] if data else None
        return product
    except Exception as e:
        # Handle exceptions gracefully (log or print the error)
        print(f"An error occurred in get_credit_limit: {e}")
        return None
      
@anvil.server.callable
def get_credit_limit():
    try:
        data = app_tables.fin_borrower.search()

        # If there is data for the specified product_id
        product = data[0]['credit_limit'] if data else None
        
        return product
    except Exception as e:
        # Handle exceptions gracefully (log or print the error)
        print(f"An error occurred in get_credit_limit: {e}")
        return None