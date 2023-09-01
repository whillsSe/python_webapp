class BankAccount:
    def __init__(self,accountNumber,owner):
        self.accountNumber = accountNumber
        self.owner = owner
        self.balance = 0
    def getBalance(self):
        return self.balance
    def deposit(self,amount):
        self.balance += amount
    def withdrawal(self,amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            raise ValueError('You are attempting to withdraw more than your balance!')
    def getAccountNumber(self):
        return self.accountNumber
    def getOwner(self):
        return self.owner
class User:
    def __init__(self,name):
        self.name = name
    def getName(self):
        return self.name
class Bank:
    def __init__(self):
        self.accounts = {}
        self.accountCounter = 0
    def createAccount(self,owner):
        accountNumber = self.accountCounter
        account = BankAccount(accountNumber,owner)
        self.accounts[str(accountNumber)] = account
        self.accountCounter += 1
    def closeAccount(self,accountNumber):
        del self.accounts[str(accountNumber)]
    def getAccount(self,accountNumber):
        return self.accounts[str(accountNumber)]
    def transfer(self,user,userAccountNumber,targetAccountNumber,amount):
        if user.getName() != self.accounts[str(userAccountNumber)].getOwner() :
            raise KeyError("invalid user access to account!")
        try:
            userAccount = self.accounts[str(userAccountNumber)]
            targetAccount = self.accounts[str(targetAccountNumber)]
            userAccount.withdrawal(amount)
            targetAccount.deposit(amount)
        except KeyError as e:
            print(e)

bank = Bank()
amI = User("Student am I")
isHe = User("Bob")
bank.createAccount(amI.getName())
bank.createAccount(isHe.getName())

accountAmI = bank.getAccount(0)
accountAmI.deposit(1000)
bank.transfer(amI,0,1,500)

print(bank.getAccount(0).getBalance())
print(bank.getAccount(1).getBalance())