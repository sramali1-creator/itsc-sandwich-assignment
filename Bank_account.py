class BankAccount:
    bank_title = "Niner National Bank"

    def __init__(self, customer_name, current_balance, minimum_balance):
        self.customer_name = customer_name
        self.current_balance = current_balance
        self.minimum_balance = minimum_balance

    def deposit(self, amount):
        self.current_balance += amount

    def withdraw(self, amount):
        if self.current_balance - amount < self.minimum_balance:
            print("Withdrawal denied: insufficient funds to maintain minimum balance.")
        else:
            self.current_balance -= amount

    def print_customer_information(self):
        print(f"Bank: {self.bank_title}")
        print(f"Customer: {self.customer_name}")
        print(f"Balance: ${self.current_balance}")


account1 = BankAccount("Alex Kim", 500, 100)
account1.deposit(200)
account1.withdraw(50)
account1.print_customer_information()

print()

account2 = BankAccount("Jordan Lee", 1000, 200)
account2.withdraw(900)
account2.print_customer_information()