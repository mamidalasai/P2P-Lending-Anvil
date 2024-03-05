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
import anvil.secrets
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
            borrower_loan_created_timestamp=date_of_apply
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
def calculate_extension_details(loan_id, loan_extension_months):
    # Fetch necessary loan details from the Anvil data tables
    loan_row = app_tables.fin_loan_details.get(loan_id=loan_id)

    if loan_row is not None:
        # Extract loan details
        total_loan_amount = loan_row['total_repayment_amount']
        loan_amount = loan_row['loan_amount']
        tenure = loan_row['tenure']
        interest_rate = loan_row['interest_rate']
        product_id = loan_row['product_id']
        loan_disbursed_timestamp = loan_row['loan_disbursed_timestamp']

        # Fetch the last emi row for the specified loan_id
        last_emi_rows = app_tables.fin_emi_table.search(loan_id=loan_id)
        total_payments_made = 0

        if last_emi_rows:
            # Sort the list of rows based on the 'emi_number' column in reverse order
            last_emi_list = list(last_emi_rows)
            last_emi_list.sort(key=lambda x: x['emi_number'], reverse=True)

            # Extract the 'emi_number' from the first row, which represents the highest 'emi_number'
            total_payments_made = last_emi_list[0]['emi_number']

        # Calculate the monthly interest rate
        monthly_interest_rate = interest_rate / (12 * 100)

        # Calculate the EMI using the formula for EMI calculation
        factor = (1 + monthly_interest_rate) ** tenure
        emi = loan_amount * monthly_interest_rate * factor / (factor - 1)

        # Fetch the extension fee from the product details
        extension_fee = 0
        product_data = tables.app_tables.fin_product_details.search(product_id=product_id)
        for row in product_data:
            extension_fee = row['extension_fee']

        # Calculate the extension amount based on the extension fee
        extension_amount = (extension_fee * loan_amount) / 100

        # Calculate the total amount of EMIs paid
        emi_paid = total_payments_made * emi

        # Calculate the remaining loan amount
        remaining_loan_amount = total_loan_amount - emi_paid

        # Calculate the total extension months
        total_extension_months = tenure + loan_extension_months

        # Calculate the schedule payment date for each EMI
        payment_schedule = []
        for month in range(1, total_extension_months + 1):
            # Calculate the payment date by adding months to the loan disbursed timestamp
            payment_date = loan_disbursed_timestamp + timedelta(days=30 * month)

            # Append the payment date to the schedule
            payment_schedule.append(payment_date)

        # Return the calculated values
        return {
            'total_extension_months': total_extension_months,
            'extension_fee_comp_value': extension_fee,
            'remaining_loan_amount': remaining_loan_amount,
            'extension_amount': extension_amount,
            'emi_paid': emi_paid,
            'emi': emi,
            'payment_schedule': payment_schedule
        }
    else:
        return "Loan details not found"
@anvil.server.callable
def calculate_emi_details(loan_amount, tenure_months, user_id, interest_rate, total_repayment_amount, product_id, membership_type, credit_limit, payment_type):
    payment_details = []
  

    # Monthly interest rate
    monthly_interest_rate = (interest_rate / 100) / 12

    # Calculate EMI (monthly installment)
    emi = (loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** tenure_months)) / (((1 + monthly_interest_rate) ** tenure_months) - 1)

    # Initialize the first beginning balance with the initial loan amount
    beginning_balance = loan_amount
    payment_date_placeholder = "Awaiting update"

    # Calculate payment details for each month up to the tenure
    for month in range(1, tenure_months + 1):
        # Calculate interest amount for the month
        interest_amount = beginning_balance * monthly_interest_rate

        # Calculate principal amount for the month
        principal_amount = emi - interest_amount

        # Update ending balance for the current iteration
        ending_balance = beginning_balance - principal_amount

        # Add payment details to the list
        payment_details.append({
            'PaymentNumber': month,
            'PaymentDate': payment_date_placeholder,
            'ScheduledPayment': f"₹ {emi:.2f}",
            'Principal': f"₹ {principal_amount:.2f}",
            'Interest': f"₹ {interest_amount:.2f}",
            'BeginningBalance': f"₹ {beginning_balance:.2f}",
            'TotalPayment': f"₹ {emi:.2f}",  
            'EndingBalance': f"₹ {ending_balance:.2f}"
        })

        # Update beginning balance for the next iteration
        beginning_balance = ending_balance

    return payment_details
@anvil.server.callable
def calc_total_payments_made(loan_id):
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

    # Return the total payments made
    return total_payments_made


@anvil.server.callable
def calculate_foreclosure(loan_amount, tenure, interest_rate, total_payments_made, product_id):
    loan_amount = float(loan_amount)
    tenure = float(tenure)  # Assuming tenure is given in months
    interest_rate = float(interest_rate)

    # Calculate EMIs
    monthly_interest_rate = interest_rate / (12 * 100)  # Assuming interest rate is in percentage
    factor = (1 + monthly_interest_rate) ** tenure  
    emi = loan_amount * monthly_interest_rate * factor / (factor - 1)
    emi = float(emi)
    monthly_installment = loan_amount / tenure
    monthly_installment = float(monthly_installment)

    # Calculate payments made
    paid_amount = emi * total_payments_made
    paid_amount = float(paid_amount)
    monthly_interest_amount = emi - monthly_installment
    monthly_interest_amount = float(monthly_interest_amount)

    # Calculate outstanding amount
    outstanding_amount = loan_amount - (monthly_installment * total_payments_made)
    oustanding_month = tenure - total_payments_made
    outstanding_amount_i_amount = monthly_interest_amount * oustanding_month
    total_outstanding_amount = outstanding_amount + outstanding_amount_i_amount

    # Fetch product details and foreclosure fees
    data = app_tables.fin_product_details.search(product_id=product_id)
    foreclosure_fee_lst = [i['foreclosure_fee'] for i in data]
    foreclosure_fee_str = ', '.join(map(str, foreclosure_fee_lst))

    # Calculate foreclosure amount
    foreclose_fee = float(foreclosure_fee_str)
    foreclose_amount = outstanding_amount * (foreclose_fee / 100)
    foreclose_amount = float(foreclose_amount)

    # Calculate total due amount
    total_due_amount = outstanding_amount + foreclose_amount
    total_due_amount = float(total_due_amount)

    return {
        "outstanding_amount": outstanding_amount,
        "total_outstanding_amount": total_outstanding_amount,
        "emi": emi,
        "foreclose_amount": foreclose_amount,
        "paid_amount": paid_amount,
        "monthly_installment": monthly_installment,
        "monthly_interest_amount": monthly_interest_amount,
        "outstanding_interest_amount": outstanding_amount_i_amount,
        "remaining_months": oustanding_month,
        "foreclosure_fee_str": foreclosure_fee_str,
        "total_due_amount": total_due_amount
    }


# this method is use for calulating the loan 
@anvil.server.callable
def calculate_extension_details(loan_id, loan_extension_months):
    loan_row = app_tables.fin_loan_details.get(loan_id=loan_id)

    if loan_row is not None:
        total_loan_amount = loan_row['total_repayment_amount']
        loan_amount = loan_row['loan_amount']
        tenure = loan_row['tenure']
        interest_rate = loan_row['interest_rate']
        product_id = loan_row['product_id']
        loan_disbursed_timestamp = loan_row['loan_disbursed_timestamp']

        last_emi_rows = app_tables.fin_emi_table.search(loan_id=loan_id)
        total_payments_made = 0

        if last_emi_rows:
            last_emi_list = list(last_emi_rows)
            last_emi_list.sort(key=lambda x: x['emi_number'], reverse=True)
            total_payments_made = last_emi_list[0]['emi_number']

        monthly_interest_rate = interest_rate / (12 * 100)

        factor = (1 + monthly_interest_rate) ** tenure
        emi = loan_amount * monthly_interest_rate * factor / (factor - 1)
        extension_fee = 0
        product_data = tables.app_tables.fin_product_details.search(product_id=product_id)
        for row in product_data:
            extension_fee = row['extension_fee']
        extension_amount = (extension_fee * loan_amount) / 100
        emi_paid = total_payments_made * emi
        remaining_loan_amount = total_loan_amount - emi_paid
        total_extension_months = tenure + loan_extension_months
        payment_schedule = []
        for month in range(1, total_extension_months + 1):
           
            payment_date = loan_disbursed_timestamp + timedelta(days=30 * month)

            payment_schedule.append(payment_date)
        
        return {
            'total_extension_months': total_extension_months,
            'extension_fee_comp_value': extension_fee,
            'remaining_loan_amount': remaining_loan_amount,
            'extension_amount': extension_amount,
            'emi_paid': emi_paid,
            'emi': emi,
            'payment_schedule': payment_schedule
        }
    else:
        return "Loan details not found"
