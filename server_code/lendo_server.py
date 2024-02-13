import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
from datetime import datetime, timezone

# @anvil.server.callable
# def add_lendor_frist_form(name,gender,date_of_birth,user_id):
#   row = app_tables.fin_user_profile.search(customer_id = user_id)
#   if row:
#     row[0]['full_name'] = name
#     row[0]['gender'] = gender
#     row[0]['date_of_birth'] = date_of_birth
#     row[0]['form_count'] = 0

# @anvil.server.callable
# def add_lendor_second_form(mobile,email,photo,user_id):
#   row = app_tables.fin_user_profile.search(customer_id = user_id)
#   if row:
#     #row[0]['investment'] = investment
#     row[0]['mobile'] = mobile
#     row[0]['another_email'] = email
#     row[0]['user_photo'] = photo
#     row[0]['form_count'] = 1

@anvil.server.callable
def add_lendor_education_form(qualification,certificate,user_id):
  row = app_tables.fin_user_profile.search(customer_id = user_id)
  if row:
    
    row[0]['qualification'] = qualification
    row[0]['education_certificate'] = certificate
    

# @anvil.server.callable
# def add_lendor_third_form(aadhaar_photo, pan_card, pan_id,aadhaar_card,user_id):
#   row = app_tables.fin_user_profile.search(customer_id = user_id)
#   if row:
#     row[0]['pan_photo'] = pan_id
#     row[0]['pan_number'] = pan_card
#     row[0]['aadhaar_no'] = aadhaar_card
#     row[0]['aadhaar_photo'] = aadhaar_photo

# @anvil.server.callable
# def add_lendor_four_form(street_adress_1,street_address_2,city,user_id):
#   row = app_tables.fin_user_profile.search(customer_id = user_id)
#   if row:
#     row[0]['street_adress_1'] = street_adress_1
#     row[0]['street_address_2'] = street_address_2
#     row[0]['city'] = city
                          
# @anvil.server.callable
# def add_lendor_five_form(pincode,state,country,user_id):
#   row = app_tables.fin_user_profile.search(customer_id = user_id)
#   if row:
#     row[0]['state'] = state
#     row[0]['country'] = country
#     row[0]['pincode'] = pincode



@anvil.server.callable
def add_lendor_six_form(lending_type, investment,lending_period, user_id):
  row = app_tables.fin_lender.add_row(investment=investment, lending_type=lending_type,lending_period=lending_period,customer_id = user_id)
    
@anvil.server.callable
def update_another_person(user_id, selected_person):
  user_profile = app_tables.fin_user_profile.get(customer_id=user_id)
  user_profile['another_person'] = selected_person
  user_profile.save()

@anvil.server.callable
def add_lendor_individual_form_1(company_name,org_type,emp_type,user_id):
  row = app_tables.fin_user_profile.search(customer_id = user_id)
  if row:
    row[0]['company_name']=company_name
    row[0]['organization_type']=org_type
    row[0]['employment_type']=emp_type

    

@anvil.server.callable
def add_lendor_individual_form_2(comp_address,landmark,business_phone_number,user_id):
  row = app_tables.fin_user_profile.search(customer_id = user_id)
  if row:
    row[0]['company_address']=comp_address
    row[0]['company_landmark']=landmark
    row[0]['business_no']=business_phone_number
    
          


@anvil.server.callable
def add_lendor_individual_form_3(annual_salary, designation,emp_id_proof,last_six_month,user_id):
  row = app_tables.fin_user_profile.search(customer_id = user_id)
  if row:
    row [0]['annual_salary']=annual_salary
    row[0]['designation'] = designation
    row[0]['emp_id_proof']=emp_id_proof
    row[0]['last_six_month_bank_proof']=last_six_month

@anvil.server.callable
def add_lendor_institutional_form_1(business_name,business_location,business_add,user_id):
  row = app_tables.fin_user_profile.search(customer_id = user_id)
  if row:
    row[0]['business_name'] = branch_name
    row[0]['business_location'] = business_location
    row[0]['business_add'] = business_add

@anvil.server.callable
def add_lendor_institutional_form_2(nearest_loc,business_type,empolyees_working,year_estd,user_id):
  row = app_tables.fin_user_profile.search(customer_id = user_id)
  if row:
    row[0]['nearest_location'] = nearest_loc
    row[0]['business_type'] = business_type
    row[0]['employees_working'] = empolyees_working
    row[0]['year_estd'] = year_estd

@anvil.server.callable
def add_lendor_institutional_form_3(industry_type,six_monthturnover,last_six_statments,user_id):
  row = app_tables.fin_user_profile.search(customer_id = user_id)
  if row:
    row[0]['industry_type'] = industry_type
    row[0]['six_month_turnover'] = six_monthturnover
    row[0]['last_six_month_bank_proof'] = last_six_statments

@anvil.server.callable
def add_lendor_institutional_form_4(director_name,director_no,din,cin,user_id):
  row = app_tables.fin_user_profile.search(customer_id = user_id)
  if row:
    row[0]['director_name'] = director_name
    row[0]['director_no'] = director_no
    row[0]['din'] = din
    row[0]['cin'] = cin

@anvil.server.callable
def add_lendor_institutional_form_5(reg_office_add,off_add_proof,proof_verification,user_id):
  row = app_tables.fin_user_profile.search(customer_id = user_id)
  if row:
    row[0]['registered_off_add'] = reg_office_add
    row[0]['off_add_proof'] = off_add_proof
    row[0]['proof_verification'] = proof_verification

@anvil.server.callable
def add_lendor_marital(marital_status,user_id):
  row = app_tables.fin_user_profile.search(customer_id=user_id)
  if row:
    row[0]['marital_status']=marital_status
    # row[0]['form_count']=6

@anvil.server.callable
def add_education_tenth(tenth_class,user_id):
  row = app_tables.fin_user_profile.search(customer_id=user_id)
  if row:
    row[0]['tenth_class']=tenth_class

@anvil.server.callable
def add_education_int(tenth_class,intermediate,user_id):
  row = app_tables.fin_user_profile.search(customer_id=user_id)
  if row:
    row[0]['tenth_class']=tenth_class
    row[0]['intermediate']=intermediate

@anvil.server.callable
def add_education_btech(tenth_class,intermediate,user_id):
  row = app_tables.fin_user_profile.search(customer_id=user_id)
  if row:
    row[0]['tenth_class']=tenth_class
    row[0]['intermediate']=intermediate
    row[0]['btech']=btech

@anvil.server.callable
def add_education_mtech(tenth_class,intermediate,btech,mtech,user_id):
  row = app_tables.fin_user_profile.search(customer_id=user_id)
  if row:
    row[0]['tenth_class']=tenth_class
    row[0]['intermediate']=intermediate
    row[0]['btech']=btech
    row[0]['mtech']=mtech

@anvil.server.callable
def add_education_phd(tenth_class,intermediate,btech,mtech,phd,user_id):
  row = app_tables.fin_user_profile.search(customer_id=user_id)
  if row:
    row[0]['tenth_class']=tenth_class
    row[0]['intermediate']=intermediate
    row[0]['btech']=btech
    row[0]['mtech']=mtech
    row[0]['phd']=phd

@anvil.server.callable
def add_lendor_married(another_person,user_id):
  row = app_tables.fin_user_profile.search(customer_id=user_id)
  if row:
    row[0]['another_person']=another_person
    # row[0]['form_count']=6

@anvil.server.callable
def add_lendor_bank_details_form_1(account_name, account_type,account_number,bank_name, user_id):
  row = app_tables.fin_user_profile.search(customer_id = user_id)
  if row:
    row[0]['account_name'] = account_name
    row[0]['account_type'] = account_type
    row[0]['account_number'] = account_number
    row[0]['bank_name'] = bank_name


@anvil.server.callable
def add_lendor_bank_details_form_2(bank_id,branch_name, user_id):
  row = app_tables.fin_user_profile.search(customer_id = user_id)
  if row:
    row[0]['bank_id'] = bank_id
    row[0]['branch_name'] = branch_name
    row[0]['usertype'] = 'lender'
    row[0]['last_confirm'] = True



#--- lender reg was completed ---#



# this one for dashboard start 

# code for rta 
@anvil.server.callable
def add_rtr_form(final_rta, available_balance):
  #row = app_tables.lender.search()
  row = app_tables.fin_lender.search(tables.order_by("lender_accepted_timestamp", ascending=False))
  if row:
    row[0]['final_rta'] = final_rta
    row[0]['available_balance'] = available_balance

@anvil.server.callable
def add_top_up_amount(top_up):
  row= app_tables.top_up.search()
  if row:
    top_up = int(top_up)
    row[0]['top_up_amount'] = top_up



#code for foreclose request

@anvil.server.callable
def search_user(query):
  result=app_tables.fin_foreclose.search()
  if query:
    result=[
    x for x in result
    if query in x["customer_id"]
    ]
  return result

  
# In your Anvil server module (e.g., server_module.py)

import anvil.server
from anvil.tables import app_tables

@anvil.server.callable
def get_user_data(user_id):
    user = app_tables.fin_user_profile.get(customer_id = user_id)
    if user:
        return {
            'full_name': user['full_name'],
            'gender': user['gender'],
            'date_of_birth': user['date_of_birth'],
            'mobile': user['mobile'],
            'another_email': user['another_email'],
            'aadhaar_no': user['aadhaar_no'],
            'pan_number' : user['pan_number'],
            'qualification': user['qualification'],
            'street_adress_1': user['street_adress_1'],
            'street_address_2': user['street_address_2'],
            'city': user['city'],
            'pincode': user['pincode'],
            'state': user['state'],
            'country': user['country'],
            #'lending_type': user['lending_type'],
            #'investment': user['investment'],
            #'lending_period': user['lending_period'],
            'employment_type': user['employment_type'],
            'organization_type': user['organization_type'],
            'company_name': user['company_name'],
            'business_no': user['business_no'],
            'company_landmark': user['company_landmark'],
            'company_address': user['company_address'],
            'business_name': user['business_name'],
            'business_add': user['business_add'],
            'business_location': user['business_location'],
            'branch_name': user['branch_name'],
            'nearest_location': user['nearest_location'],
            'business_type': user['business_type'],
            'employees_working': user['employees_working'],
            'year_estd': user['year_estd'],
            'industry_type': user['industry_type'],
            'six_month_turnover': user['six_month_turnover'],
            'director_name': user['director_name'],
            'director_no': user['director_no'],
            'din': user['din'],
            'cin': user['cin'],
            'registered_off_add': user['registered_off_add'],
            'off_add_proof': user['off_add_proof'],
            'account_name': user['account_name'],
            'account_type': user['account_type'],
            'account_number': user['account_number'],
            'bank_name': user['bank_name'],
            'bank_id': user['bank_id'],
            # 'salary_type': user['salary_type'],
            'branch_name': user['branch_name'],
            # 'net_bank': user['net_bank']
          
            
        }
    else:
        return None
      
@anvil.server.callable
def add_guarantor_details(g_full_name, g_dob,g_mobile_no,g_address,g_profession,g_company_name,g_annual_earning,user_id):
  row = app_tables.fin_guarantor_details.search(customer_id=user_id)
  if row:
    row[0]['guarantor_name'] = g_full_name
    row[0]['guarantor_date_of_birth'] = g_dob
    row[0]['guarantor_mobile_no'] = g_mobile_no
    row[0]['guarantor_address'] = g_address
    row[0]['guarantor_profession'] = g_profession
    row[0]['guarantor_company_name'] = g_company_name
    row[0]['guarantor_annual_earning'] = g_annual_earning


# code for view borr loan
@anvil.server.callable
def transfer_user_profile_to_loan_details(email,user_id):
    print(f"Fetching data for email: {email}")

    # Fetch distinct loan_id values for the given email from the loan_details table
    distinct_loan_ids = app_tables.fin_loan_details.search()

    # Fetch lender data from user_profile table
    lender_row = app_tables.fin_user_profile.get(email_user=email)
    if lender_row:
        lender_customer_id = lender_row['customer_id']
        lender_email_id = lender_row['email_user']
        lender_full_name = lender_row['full_name']

        # Iterate over each distinct loan_id and call the server function
        for row in distinct_loan_ids:
            unique_loan_id = row['loan_id']

            # Call the server function to transfer data to loan_details table
            add_loan_details_data(unique_loan_id, lender_customer_id, lender_email_id, lender_full_name)


@anvil.server.callable
def add_loan_details_data(loan_id, lender_customer_id, lender_email_id, lender_full_name):

    # Check if a row with the given loan_id already exists
    existing_row = app_tables.fin_loan_details.get(loan_id=loan_id)

    if existing_row:
        print("Row already exists. Updating existing row.")
        # Update the existing row with new data
        existing_row.update(
            lender_customer_id=lender_customer_id,
            lender_email_id=lender_email_id,
            lender_full_name=lender_full_name
        )
    else:
        print("No row exists. Adding a new row.")
        # Add a new row to the loan_details table
        app_tables.fin_loan_details.add_row(
            loan_id=loan_id,
            lender_customer_id=lender_customer_id,
            lender_email_id=lender_email_id,
            lender_full_name=lender_full_name
        )

# # Function to determine membership type based on investment
# def determine_membership_type(investment):
#     investment_value = investment['investment']  # Assuming 'investment' is the column name
    
#     if investment_value <= 500000:
#         return 'Silver'
#     elif investment_value <= 1000000:
#         return 'Gold'
#     else:
#         return 'Platinum'

# # Function to fetch loan details based on membership type and status
# @anvil.server.callable
# def fetch_loan_details():
#     # Fetch lender's investment from lender table
#     lender_investment = app_tables.lender.search()[0]  # Assuming it returns a single row
#     membership_type_result = determine_membership_type(lender_investment)
    
#     # Fetch loan details based on membership type and status
#     if membership_type_result == 'Silver':
#         return app_tables.loan_details.search(
#             loan_updated_status='under_process', 
#             membership_type='Silver'
#         )
#     elif membership_type_result == 'Gold':
#         # Fetch loan details for 'Silver' and 'Gold' membership types
#         silver_gold_loan_details = [
#             row for row in app_tables.loan_details.search(loan_updated_status='under_process')
#             if row['membership_type'] in ['Silver', 'Gold']
#         ]
#         return silver_gold_loan_details
#     else:  # Platinum can fetch all membership types
#         return app_tables.loan_details.search(loan_updated_status='under_process')

# # Function to determine membership type based on investment
# def determine_membership_type(investment):
#     if investment <= 500000:
#         return 'Silver'
#     elif investment <= 1000000:
#         return 'Gold'
#     else:
#         return 'Platinum'

# @anvil.server.callable
# def fetch_loan_details():
#     try:
#         # Assuming lender table has only one row, modify accordingly if needed
#         lender_investment = app_tables.lender.search()[0]['investment']
#         membership_type_result = determine_membership_type(lender_investment)

#         # Print statements for debugging
#         print("Lender Investment:", lender_investment)
#         print("Membership Type Result:", membership_type_result)

#         # Fetch loan details based on conditions
#         loan_details_result = []
#         if membership_type_result == 'Silver':
#             loan_details_result = app_tables.loan_details.search(
#                 loan_updated_status='under process',
#                 membership_type='Silver'
#             )
#         elif membership_type_result == 'Gold':
#             loan_details_result = app_tables.loan_details.search(
#                 loan_updated_status='under process',
#                 membership_type=['Silver', 'Gold']
#             )
#         else:
#             loan_details_result = app_tables.loan_details.search(loan_updated_status='under process')

#         # Print the count of fetched loan details for debugging
#         print("Fetched loan details count:", len(list(loan_details_result)))

#         return loan_details_result
#     except Exception as e:
#         # Print any exceptions for debugging
#         print("Error fetching loan details:", str(e))
#         return []


## Code for loan disbusement
@anvil.server.callable
def loan_disbursement_action(selected_row, email):
    # Assuming 'selected_row' is the row from the loan_details table
    loan_amount = selected_row['loan_amount']
    print("Loan amount:", loan_amount)
    lender_accepted_timestamp = selected_row['lender_accepted_timestamp']
    print("lender_accepted_timestamp timezone:", lender_accepted_timestamp.tzinfo)

    # Convert lender_accepted_timestamp to UTC if it's not already
    if lender_accepted_timestamp.tzinfo is None:
        lender_accepted_timestamp = lender_accepted_timestamp.replace(tzinfo=timezone.utc)
        print("lender_accepted_timestamp converted to UTC")
  
    # Retrieve the rows from the wallet table based on the user's email
    wallet_rows = app_tables.fin_wallet.search(user_email=email)
    
    if wallet_rows and len(wallet_rows) > 0:
        # Assuming you want to use the first matching row
        wallet_row = wallet_rows[0]
        
        wallet_amount = wallet_row['wallet_amount']
        print("Wallet amount:", wallet_amount)
      
        # Get the current time in the same timezone as lender_accepted_timestamp
        current_time = datetime.now(timezone.utc)
        print("current_time:", current_time)
      
        if loan_amount > wallet_amount:
            # Check if 5 minutes have passed since lender_accepted_timestamp
            time_difference = current_time - lender_accepted_timestamp
            print("time_difference:", time_difference)
            if time_difference.total_seconds() > 120:  # 300 seconds = 5 minutes # 120 seconds = 2 minutes
                # Update loan status based on the comparison of wallet_amount and loan_amount
                if loan_amount > wallet_amount:
                 # Update loan status to 'lost opportunities'
                 selected_row['loan_updated_status'] = 'lost opportunities'
                 selected_row.update()
                 print("loan_updated_status as lost opportunities")
                 return "Time_out"
                else:
                  print("2 minutes have not passed yet")
                  # 2 minutes have not passed yet
                  selected_row['loan_updated_status'] = 'accepted'
                  selected_row.update()
                  return "insufficient_balance"    
            else:
                # Update loan status to 'under process'
                selected_row['loan_updated_status'] = 'accepted'
                selected_row.update()
                return "insufficient_balance"
        else:
           wallet_amount -= loan_amount
           wallet_row['wallet_amount'] = wallet_amount
           wallet_row.update()
           
           # Signal the client to pay to the borrower
           return "pay_to_borrower"
    else:
        # Handle the case where the wallet row is not found
        print("wallet_not_found")
        return "wallet_not_found" 


@anvil.server.background_task
def check_loan_timeout(selected_row, lender_accepted_timestamp, email):
    # Record the start time
    start_time = datetime.now()

    # Wait for 2 minutes
    while datetime.now() < start_time + timedelta(minutes=2):
        anvil.server.sleep(10)  # Sleep for 10 seconds

    # After 2 minutes, check wallet_amount again
    wallet_rows = app_tables.fin_wallet.search(user_email=email)
    if wallet_rows and len(wallet_rows) > 0:
        wallet_row = wallet_rows[0]
        wallet_amount = wallet_row['wallet_amount']
        
        if loan_amount > wallet_amount:
            # Update loan status to 'lost opportunities'
            selected_row['loan_updated_status'] = 'lost opportunities'
            selected_row.update()
            return "Time_out"
          