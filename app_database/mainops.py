import mysql.connector as connect
from mysql.connector.connection import MySQLConnection
import constant

class DBConnect:
    
    def __init__(self, host: 'Hostname', user: 'Username', password: 'User_password') -> None:
        self.host = host
        self.user = user
        self.passwd = password


    def getConnection(self) -> MySQLConnection:
        try:
            connection = connect.connect(host=self.host, user=self.user, passwd=self.passwd)

            return connection
        except Exception as e:
            print("Exception occured: ", e)

    def insertNewUser(self, connection, user):
        try:

            cursor = connection.cursor()
            query = 'insert into '+ constant.DATABASE_NAME +'.'+ constant.USER_TABLE +'(user_name, user_dob, user_email, \
                        user_created_date) values("' + user.user_name +'", "'+ user.user_dob +'", "'+ user.user_email +'", curdate())'

            userId = self.insertUser(query, connection)

            bank_query = f'insert into {constant.DATABASE_NAME}.{constant.BANK_ACCOUNT_TABLE}(user_id, bank_account_number, amount) \
                            values({userId}, "{user.bank_account_number}", {user.amount})'

            cursor.execute(bank_query)

            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            print("Exception occured: ", e)

    def insertUser(self, userQuery, connection) -> int:

        cursor = connection.cursor()
        cursor.execute(userQuery)
        connection.commit()

        cursor.close()
        return cursor.lastrowid

    def printAllUsers(self, connection):
        
        try:
    
            cursor = connection.cursor()
            cursor.execute(f"use {constant.DATABASE_NAME}")
            users = cursor.callproc('print_users')

            cursor.close()
            connection.close()
            return cursor.stored_results()

        except Exception as e:
            print("Exception occured: ", e)

    def printAmount(self, connection, amount):

        try:
            cursor = connection.cursor()
            cursor.execute(f"use {constant.DATABASE_NAME}")
            args = [amount]
            cursor.callproc('check_balance', [amount])

            for result in cursor.stored_results():
                details = result.fetchall()

            cursor.close()
            connection.close()
            return details

        except Exception as e:
            print("Exception occured: ", e)



    def addAllAmount(self, connection, account_no, amount):
        try:
            cursor = connection.cursor()
            cursor.execute(f"use {constant.DATABASE_NAME}")
            # check if the user is active or not. Only then we will perform query
            activeCheckQuery = f"select is_user_active from {constant.DATABASE_NAME}.{constant.BANK_ACCOUNT_TABLE} where bank_account_number={account_no}"
            
            cursor.execute(activeCheckQuery)
            for res in cursor.fetchall():
                result = int(res[0])

            if(result == 1):
                query = f'update {constant.BANK_ACCOUNT_TABLE} set amount+{amount}' 
                cursor.execute(query)

            elif(result == 0):
                print("Error: Current bank account is deactivated.")

            cursor.close()
            connection.close()

        except Exception as e:
            print("Exception occured: ", e)
        

    def getAccountStatement(self, connection):
        try:
            cursor = connection.cursor()
            cursor.execute(f"use {constant.DATABASE_NAME}")

            query = f"select Transaction_date, withdrawn_amount from {constant.TRANSACTION_TABLE}"
            cursor.execute(query)
            
            return cursor.fetchall()
                

        except Exception as e:
            print("Exception occured: ", e)

    
    def getAccountStatementForInterval(self, connection, from_date, to_date):
        try:
            cursor = connection.cursor()
            cursor.execute(f"use {constant.DATABASE_NAME}")

            query = f"select Transaction_date, withdrawn_amount from {constant.TRANSACTION_TABLE} where \
                        Transaction_date>= {from_date} and Transaction_date<={to_date}"

            cursor.execute(query)
            for row in cursor.fetchall():
                print(row)
        except Exception as e:
            print("Exception occured: ", e)
        


    def withdrawAmount(self, connection, amount, account_no):
        try:
            
            cursor = connection.cursor()
            cursor.execute(f"use {constant.DATABASE_NAME}")
            args = (amount, account_no, 0)

            cursor.execute(f"select is_user_active from {constant.BANK_ACCOUNT_TABLE} where bank_account_number={account_no}")
            for row in cursor.fetchall():
                active = int(row[0])

            if(active == 1):    
                
                transactionQuery_1 = f"select amount from {constant.BANK_ACCOUNT_TABLE} where \
                                    bank_account_number={account_no}"
                
                # to check at the end if amount is withdrawn or not
                cursor.execute(transactionQuery_1)

                for row in cursor.fetchall():
                    present_amt = row[0]
                
                rec = cursor.callproc('withdraw_amount', args)

                transactionQuery = f"select user_id, bank_account_id, amount from {constant.BANK_ACCOUNT_TABLE} where \
                                    bank_account_number={account_no}"
                cursor.execute(transactionQuery)
                for row in cursor.fetchall():
                    rowResult = row

                if(present_amt == rowResult[2]):
                    if(present_amt < 5000):
                        print("Minimum balance 5000 should be maintained")
                    elif(int(amount) > rowResult[2]):
                        print("No Sufficient Balance.")
                    else:
                        transactionInsertionQuery = f"insert into transaction(Transaction_date, user_id, bank_account_id, withdrawn_amount) \
                                                values(curdate(), {rowResult[0]}, {rowResult[1]}, {amount})"
                        cursor.execute(transactionInsertionQuery)
                        connection.commit()

                cursor.close()
                connection.close()

            elif(active == 0):
                print("Error: Current bank account is deactivated.")







            cursor.close()
            connection.close()
        except Exception as e:
            print("Exception occured: ", e)
        


