import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime  

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#


@anvil.server.callable
def create_wallet_entry(email, customer_id, full_name, user_type):
    # Generate unique wallet_id and account_id
    wallet_id = generate_wallet_id()
    account_id = generate_account_id()
    
    existing_wallets = app_tables.fin_wallet.search(user_email=email)
    print(existing_wallets)
    
    if len(existing_wallets) == 0:
        app_tables.fin_wallet.add_row(
            user_email=email,
            wallet_id=wallet_id,
            account_id=account_id,
            customer_id=customer_id,
            user_name=full_name,
            user_type=user_type
        )
        return f"Wallet entry created successfully for {email}"
    else:
        return f"Wallet entry already exists for {email}. Multiple entries found."

@anvil.server.callable
def fetch_user_profiles():
    user_profiles = app_tables.fin_user_profile.search()
    print(user_profiles)
    return user_profiles

def generate_wallet_id():
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
        counter = 1  # Start the counter from 1 if no existing wallets

    return f"WA{counter:04d}"

def generate_account_id():
    existing_accounts = app_tables.fin_wallet.search(tables.order_by("account_id", ascending=False))

    if existing_accounts and len(existing_accounts) > 0:
        new_account_id = existing_accounts[0]['account_id']
        if new_account_id:
            try:
                counter = int(new_account_id[1:]) + 1
            except Exception as e:
                print(f"Error converting counter: {e}")
                counter = 1
        else:
            counter = 1
    else:
        counter = 1  # Start the counter from 1 if no existing accounts

    return f"A{counter:04d}"


# code for wallet_transactions
def generate_transaction_id():
    latest_transaction = app_tables.fin_wallet_transactions.search(
        tables.order_by("transaction_id", ascending=False)
    )

    if latest_transaction and len(latest_transaction) > 0:
        last_transaction_id = latest_transaction[0]['transaction_id']
        counter = int(last_transaction_id[2:]) + 1
    else:
        counter = 1

    return f"TA{counter:04d}"

@anvil.server.callable
def deposit_money(email, deposit_amount, customer_id):
    transaction_id = generate_transaction_id()
    
    try:
        # Fetch user_email and wallet_id based on customer_id
        wallet_row = app_tables.fin_wallet.get(user_email=email)
        
        if wallet_row is None:
            # Create a new row in the wallet table if the user does not exist
            wallet_row = app_tables.fin_wallet.add_row(user_email=email, wallet_amount=0)
        elif wallet_row['wallet_amount'] is None:
            # Set default value for wallet_amount if it's None
            wallet_row['wallet_amount'] = 0
        
        user_email = wallet_row['user_email']
        wallet_id = wallet_row['wallet_id']
        
        # Add a row to wallet_transactions table with transaction timestamp
        new_transaction = app_tables.fin_wallet_transactions.add_row(
            user_email=str(user_email),
            wallet_id=str(wallet_id),
            customer_id=customer_id,
            transaction_id=transaction_id,
            amount=deposit_amount,
            transaction_type='deposit',
            transaction_time_stamp=datetime.now(),
            status='success' 
        )
        
        # Retrieve the deposit status from the added row in wallet_transactions
        deposit_status = new_transaction['status']
        
        # Update wallet_amount only if the deposit status is 'success'
        if deposit_status == 'success':
            wallet_row['wallet_amount'] += deposit_amount
            wallet_row.update()
            return True
        else:
            print("Deposit status not successful. Wallet amount not updated.")
            return False
    
    except Exception as e:
        print(f"Deposit failed: {e}")
        app_tables.fin_wallet_transactions.add_row(
            customer_id=customer_id,
            transaction_id=transaction_id,
            amount=deposit_amount,
            transaction_type='deposit',
            transaction_time_stamp=datetime.now(),  
            status='fail'
        )
        return False

@anvil.server.callable
def withdraw_money(email, withdraw_amount, customer_id):
    transaction_id = generate_transaction_id()

    try:
        # Fetch user_email and wallet_id based on customer_id
        wallet_row = app_tables.fin_wallet.get(user_email=email)
        
        if wallet_row is None:
            # Create a new row in the wallet table if the user does not exist
            wallet_row = app_tables.fin_wallet.add_row(user_email=email, wallet_amount=0)

        if wallet_row['wallet_amount'] is not None and wallet_row['wallet_amount'] >= withdraw_amount:
        
        # Assign user_email and wallet_id outside the condition
          user_email = wallet_row['user_email']
          wallet_id = wallet_row['wallet_id']

        # Check if sufficient funds are available for withdrawal
        if wallet_row['wallet_amount'] >= withdraw_amount:
            # Add a row to wallet_transactions table with transaction timestamp
            new_transaction = app_tables.fin_wallet_transactions.add_row(
                user_email=str(user_email),
                wallet_id=str(wallet_id),
                customer_id=customer_id,
                transaction_id=transaction_id,
                amount=withdraw_amount,  
                transaction_type='withdraw',
                transaction_time_stamp=datetime.now(),
                status='success'
            )
            
            # Retrieve the withdrawal status from the added row in wallet_transactions
            withdraw_status = new_transaction['status']

            # Update wallet_amount only if the withdrawal status is 'success'
            if withdraw_status == 'success':
                wallet_row['wallet_amount'] -= withdraw_amount
                wallet_row.update() 
                return True
            else:
                print("Withdrawal failed.")
                return False
        else:
            print("Insufficient funds for withdrawal.")
            return False

    except Exception as e:
        print(f"Withdrawal failed: {e}")
        app_tables.fin_wallet_transactions.add_row(
            customer_id=customer_id,
            transaction_id=transaction_id,
            amount=withdraw_amount,
            transaction_type='withdraw',
            transaction_time_stamp=datetime.now(),
            status='fail'
        )
        return False



@anvil.server.callable
def fetch_profile_data_and_insert(email, customer_id):
    try:
        # Fetch user profile based on customer_id
        profile = app_tables.fin_user_profile.get(email_user=email)
        
        if profile is not None:
            # Fetch wallet data based on customer_id
            wallet_data = app_tables.fin_wallet.get(user_email=email)
            
            if wallet_data is not None:
                wallet_id = wallet_data['wallet_id']
                account_id = wallet_data['account_id']
                
                # Check if account_number is a string before converting to number
                account_number_value = int(profile['account_number']) if isinstance(profile['account_number'], str) else profile['account_number']
                
                # Check if a row with the same user_email already exists in wallet_bank_account_table
                existing_row = app_tables.fin_wallet_bank_account_table.get(user_email=profile['email_user'])
                
                if existing_row is None:
                    # Add a new row to wallet_bank_account_table
                    app_tables.fin_wallet_bank_account_table.add_row(
                        user_email=profile['email_user'], 
                        account_name=profile['account_name'],
                        account_number=account_number_value,
                        bank_name=profile['select_bank'],  
                        branch_name=profile['account_bank_branch'],  
                        ifsc_code=profile['ifsc_code'],
                        account_type=profile['account_type'],
                        wallet_id=wallet_id,
                        account_id=account_id
                    )
                    
                    return True
                else:
                    print("Row with the same user_email already exists in wallet_bank_account_table.")
                    return False
            else:
                print("Wallet data not found for the provided customer_id.")
                return False
        else:
            print("Profile not found for the provided customer_id.")
            return False
    except Exception as e:
        print(f"Error occurred: {e}")
        return False
      