import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


# user data 

# this function is force push to total points in bessem table
def final_points_update_bessem_table(user_id):
  id = user_id
  final_points = loan_points(id)+loan_and_trust_user_model(id)+occupation_point_and_government_id_model(id)
  # general_check = fake_detection(id)
  if general_check:
    if final_points<= 1000:
      return final_points
    else:
      fake_control(id)
  else:
    block_user(id)



# caluculate from user_profile table for this function if all values is true menas the user get 300 points 
# def general_points(id):
#     users = app_tables.fin_user_profile.search(customer_id=id)
#     if users:
#         user = users[0]
#         martial_status = user['marital_status']
#         age = user['user_age']
#         qualification = user['qualification']
        
#         points = 0
        
#         # this code is for martial_status
#         if martial_status == "Single":
#             points += 100
#         elif martial_status == "Married":
#             points += 200
        
#         # this code is for age
#         if age <= 30:
#             points += 50
#         elif 30 < age <= 50:
#             points += 100
#         elif age > 50:
#             points += 150
        
#         # this code is for qulifications
#         if qualification == "High School":
#             points += 50
#         elif qualification == "Undergraduate":
#             points += 100
#         elif qualification == "Postgraduate":
#             points += 150
        
#         # all pointa in range of  total points to 300
#         points = min(points, 300)
        
#         return points
#     else:
#         return 0








# # this function is working on underwriting 
# def loan_points(id):
#   return 100

# # this function is working on underwriting
# def loan_and_trust_user_model(id):
#   return 200

# # this function have to check by admin
# def occupation_point_and_government_id_model(id):
  
#   return 400

# # this function goes to be create


# def fake_control(id):
#   return 500


# def fake_detection(id):
  
#   return True


# def block_user(id):
#   pass
#   # if this function is call the is going to be block

# outer call function