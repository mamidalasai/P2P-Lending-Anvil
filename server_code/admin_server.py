import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server



@anvil.server.callable
def product_details(product_id, product_name, product_group,product_discription, product_categories,processing_fee,  extension_fee, membership_type, interest_type, max_amount, min_amount, min_tenure, max_tenure, roi, foreclose_type, foreclosure_fee, extension_allowed, emi_payment, first_emi_payment, min_months, discount_coupons):
  row = app_tables.fin_product_details.add_row(product_id=product_id,
                                           product_name = product_name,
                                           product_group=product_group,
                                           product_discription = product_discription,
                                           product_categories = product_categories,
                                           processing_fee=processing_fee,   
                                           extension_fee=extension_fee,
                                           membership_type=membership_type,
                                           interest_type= interest_type,
                                           # late_fee = late_fee,
                                           max_amount = max_amount,
                                           min_amount=min_amount,
                                           # tenure = tenure,
                                           min_tenure = min_tenure,
                                           max_tenure = max_tenure,
                                           roi = roi,
                                           foreclose_type=foreclose_type,
                                           foreclosure_fee = foreclosure_fee,
                                           extension_allowed=extension_allowed,
                                           # lapsed_status=lapsed_status,
                                           emi_payment = emi_payment,
                                           first_emi_payment=first_emi_payment,
                                           min_months=min_months,                                           
                                           discount_coupons = discount_coupons
                                          )



@anvil.server.callable
def manage_products(groups,category):
  row = app_tables.fin_product_categories.add_row(product_group=groups,product_category=category)


@anvil.server.callable
def user_issues_bugreports(user_issues, specific_issue, user_discription, image, feedback_form, email_user,coustmer_id):
 row = app_tables.fin_user_issues_bugreports.add_row(user_issues=user_issues,
                                                 user_discription=user_discription,
                                                 specific_issue=specific_issue,
                                                 image=image,
                                                 feedback_form=feedback_form,
                                                 email_user=email_user,
                                                 customer_id=coustmer_id)

# code for basic details
@anvil.server.callable
def add_basic_details(full_name, gender, dob, mobile_no, user_photo, alternate_email, aadhar, aadhar_card, pan, pan_card, street_adress_1, street_address_2, city, pincode, state, country, user_id):
  row = app_tables.fin_user_profile.search(customer_id=user_id)
  if row:
    row[0]['full_name'] = full_name
    row[0]['gender'] = gender
    row[0]['date_of_birth'] = dob
    row[0]['mobile']=mobile_no
    row[0]['user_photo']=user_photo
    row[0]['another_email']= alternate_email
    row[0]['aadhaar_no']=aadhar
    row[0]['aadhaar_photo']=aadhar_card
    row[0]['pan_number']=pan
    row[0]['pan_photo']=pan_card
    row[0]['street_adress_1'] = street_adress_1
    row[0]['street_address_2'] = street_address_2
    row[0]['city'] = city
    row[0]['state'] = state
    row[0]['country'] = country
    row[0]['pincode'] = pincode




@anvil.server.callable()
def get_table_data():
    # Fetch and return data from Anvil table
    # For example, fetch data from Anvil table 'my_data'
    data = tables.app_tables.fin_loan_details.search()
    return data

@anvil.server.callable
def add_data(customer_id, email, password, name, number):
  tables.app_tables.users.add_row(email=email, password_hash=password)
  tables.app_tables.fin_user_profile.add_row(customer_id=customer_id, email_user=email, full_name=name, mobile=number)

@anvil.server.callable
def login_data():
  data = tables.app_tables.users.search()
  return data

def lender_data(name, gender, date_of_birth):
  tables.app_tables.fin_user_profile.add_row(full_name=name, gender=gender, date_of_birth=date_of_birth)
  profile = tables.app_tables.fin_user_profile.search()
  return profile

@anvil.server.callable
def get_extension_data():
    data = tables.app_tables.fin_extends_loan.search()
    return data