import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


# this function is force push to total points in bessem table
def final_points_update_bessem_table(user_id):
  
    user_points = get_user_points(user_id)
    group_points = get_group_points()

    if user_points is not None and group_points is not None and group_points != 0:
        # Calculate final_points as a percentage
        final_points = (user_points / group_points) * 100
        return final_points

    return None

def get_user_points(id):
    users = app_tables.fin_user_profile.search(customer_id=id)

    if users:
        user = users[0]
        gender = user['gender']
        qualification = user['qualification']
        marrital_status = user['marital_status']

        def search_category(group_name, sub_category):
            return app_tables.fin_admin_beseem_categories.search(
                group_name=group_name, sub_category=sub_category
            )

        # Initialize user_points to 0
        user_points = 0

        gender_category_rows = search_category('gender', gender)
        if gender_category_rows:
            user_points += gender_category_rows[0]['min_points']

        qualification_category_rows = search_category('qualification', qualification)
        if qualification_category_rows:
            user_points += qualification_category_rows[0]['min_points']

        marital_status_category_rows = search_category('marrital_status', marrital_status)
        if marital_status_category_rows:
            user_points += marital_status_category_rows[0]['min_points']

        # Return the total user_points
        return user_points

    # Handle the case where no user with the specified id is found or no matching row is found
    return None
        
def get_group_points():
    groups = app_tables.fin_admin_beseem_groups.search()

    if groups:
        group_points = 0

        for group_row in groups:
            group_points += group_row['max_points']

        return group_points
    return None
