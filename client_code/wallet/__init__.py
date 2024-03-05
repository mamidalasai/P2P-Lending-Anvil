import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables



def create_wallet_id():
  existing_wallets = app_tables.fin_wallet.search(tables.order_by("wallet_id", ascending=False))
  if existing_wallets and len(existing_wallets) > 0:
    new_wallet_id = existing_wallets[0]['wallet_id']
    if new_wallet_id:
      try:
        counter = int(new_wallet_id[2:]) + 1
      except Exception as e:
        print(f"Error converting counter: {e}")
        counter = 1
    else:
      counter = 1
  else:
    counter = 1  
  return f"WA{counter:04d}"



def find_user_update_type(user_id, user_name, user_type):
  user = app_tables.fin_wallet.search(customer_id=user_id)
  if user:
    user[0]['user_name'] = user_name
    user[0]['user_type'] = user_type
    user[0]['status'] = True