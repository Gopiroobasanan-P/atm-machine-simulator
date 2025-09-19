import mysql.connector
from datetime import datetime

# ------------------ MySQL Connection ------------------ 

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          
        password="Bala@2002",
        database="atm"         
    )

# ------------------ Account Class ------------------ 
class Account:
    def __init__(self, acc_no, acc_holder, pin, balance=0):
        self.acc_no = acc_no
        self.acc_holder = acc_holder
        self.pin = pin
        self.balance = balance
    
    def Deposit(self, amount):
        if amount < 0:
            print("Invalid Deposit Amount...!")
        else:
            self.balance += amount
            print(f"{amount} Successfully Deposited...$")
    
    def Withdraw(self, amount):
        if self.balance < amount:
            print("Insufficient Balance...!")
        elif amount < 0:
            print("Invalid Withdrawal Amount...!")
        else:
            self.balance -= amount
            print(f"{amount} Successfully Withdrawn...$")

    def check_balance(self):
        print(f"Available Balance  :  {self.balance}")

# ------------------ ATM CLASS ------------------ 

class ATM:
    def __init__(self):
        pass

    # Fetch account from DB
    def authenticate(self, acc_no, pin):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM accounts WHERE acc_no=%s AND pin=%s", (acc_no, pin))
        account = cursor.fetchone()
        conn.close()

        if account:
            print(f"\nWelcome {account['Acc_holder']}...!")
            return Account(account["Acc_no"], account["Acc_holder"], account["Pin"], account["Balance"])
        else:
            print("Authentication Failed..! Incorrect Acc_no Or Pin")
            return None

    # Update balance in DB
    def update_balance(self, account):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET balance=%s WHERE acc_no=%s", (account.balance, account.acc_no))
        conn.commit()
        conn.close()

    # Generate Slip
    def generate_slip(self, account):
        try:
            now = datetime.now()
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")

            with open("Atm_Slip.txt", "a") as f:
                f.write("\n--------ATM SLIP--------\n")
                f.write(f"DATE & TIME : {date_time}\n")
                f.write(f"ACC NUMBER  : {account.acc_no}\n")
                f.write(f"ACC HOLDER  : {account.acc_holder}\n")
                f.write(f"BALANCE     : {account.balance}\n")
                f.write("------------------------\n")
            print("Slip generated and saved to Atm_Slip.txt successfully....")
        except Exception as e:
            print("Error while writing a slip..", e)

    # ATM Simulator
    
    def start(self):
        print("-----ATM MACHINE SIMULATOR-----")
        account = None
        while not account:
            try:
                acc_no = int(input("Enter the Account Number : "))
                pin = int(input("Enter the Pin : "))
                account = self.authenticate(acc_no, pin)
            except ValueError:
                print("Please Enter Numeric values for Acc_no and Pin....!")
            
        while True:
            print("\n----MENU-----")
            print("1. Check Balance")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Generate Slip")
            print("5. Exit")
            
            try:
                choice = input("Enter Your Choice : ")
                if choice == "1":
                    account.check_balance()

                elif choice == "2":
                    try:
                        amount = float(input("Enter The Deposit Amount : "))
                        account.Deposit(amount)
                        self.update_balance(account)
                    except ValueError:
                        print("*Enter a valid numeric amount")

                elif choice == "3":
                    try:
                        amount = float(input("Enter The Withdraw Amount : "))
                        account.Withdraw(amount)
                        self.update_balance(account)
                    except ValueError:
                        print("*Enter a valid numeric amount")

                elif choice == "4":
                    self.generate_slip(account)

                elif choice == "5":
                    print("Thank you for using ATM")
                    break
                else:
                    print("Invalid Choice...Try Again..!")
            except Exception as e:
                print("Error:", e)


# ---------------------------------- 

atm = ATM()
atm.start()