from multiprocessing import connection
import mysql.connector as connect
from entities import entity
from app_database import DBConnect
import constant

class Bank:

    def __init__(self):
        self.mainop = DBConnect(host = constant.DATABASE_HOST
                                , user = constant.DATABASE_USER, 
                                password = constant.DATABASE_PASSWORD) 

    def createUser(self, user):

        if(user.amount >= 5000):
            connection = self.mainop.getConnection()
            self.mainop.insertNewUser(connection, user)
        else:
            print("Minimum amount should be 5000.")


    def printUsers(self):
        connection = self.mainop.getConnection()
        userList = self.mainop.printAllUsers(connection)
        for user in userList:
            for record in user.fetchall():
                print(record)

    def addAmount(self, account_no, amount):
        connection = self.mainop.getConnection()
        self.mainop.addAllAmount(connection, account_no, amount)

    def checkBalance(self, amount):
        connection = self.mainop.getConnection()
        amount = self.mainop.printAmount(connection, amount)
        for row in amount:
            print(row)


    def withdraw(self, amount, account_no):
        connection = self.mainop.getConnection()
        self.mainop.withdrawAmount(connection, amount, account_no)

    def accountStatement(self, choice):
        connection = self.mainop.getConnection()
        records = self.mainop.getAccountStatement(connection)
        for row in records:
            print(row)

    def accountStatementForInterval(self, from_date, to_date):
        connection = self.mainop.getConnection()
        records = self.mainop.getAccountStatementForInterval(connection=connection, from_date=from_date, to_date=to_date)
        for row in records:
            print(row)
        



if __name__ == '__main__':
    
    print("1. Create User")
    print("2. Print all Users")
    print("3. Check Balance")
    print("4. Add Amount")
    print("5. Withdraw Amount")
    print("6. Check Account Statement")

    inp = int(input("Enter choice: "))
    bank = Bank()

    if(inp == 1):
        
        user = entity.user(str(input("User's name: ")),
                        str(input("User's DOB (in yyyy-mm-dd): ")),
                        str(input("User's Email: ")),
                        str(input("Bank Account Number: ")),
                        int(input("Amount (Min 5000/-): "))
                        )
        bank.createUser(user)

    elif(inp == 2):
        bank.printUsers()
    
    elif(inp == 3):
        amount = input("Bank Account Number: ")
        bank.checkBalance(amount)

    elif(inp == 4):
        acc_no = input("Bank Account Number: ")
        amount = input("Amount: ")
        bank.addAmount(acc_no, amount)

    elif(inp == 5):
        acc_no = input("Bank Account Number: ")
        amount = input("Amount: ")
        bank.withdraw(amount=amount, account_no=acc_no)

    elif(inp == 6):
        acc_no = input("Bank Account Number: ")
        print("1. From specific time interval")
        print("2. Print All")
        choice = int(input("Choice: "))
        if(choice == 2):
            bank.accountStatement(choice)
