from collections import namedtuple


user = namedtuple('User', ['user_name', 'user_dob', 'user_email', 'bank_account_number', 'amount'])

# we can set "is_user_active" by default as True
bank_account = namedtuple('Bank_Account', ['user_id', 'bank_account_number', "is_user_active", 'amount'])

transaction = namedtuple('Transaction', ['withdrawn_amount'])