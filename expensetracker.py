from typing import List
import datetime
import csv
import os

expenses: List = []
total_expense: int = 0
file_name: str = ""
budgetedAmount: int = 0
ABSOLUTE_PATH: str = os.getcwd()
FIELD_NAMES: List = ["date", "category", "amount", "description"]
MENU: dict = {'1':'Add Expense', '2':'View expenses', '3':'Track budget', '4':'Save Expenses', '5':'Exit'}

def userInput():
    dateOfExpense = input("Enter the date for the expense (YYYY-MM-DD): ") or datetime.datetime.now().date()
    expenseCategory = input("Enter the expense category (e.g. Food, Travel etc.): ")
    spentAmt = input("Enter the amount spent: ")
    expenseDesc = input("Enter the desciption of the expense: ")

    expense = {'date': dateOfExpense, 'category': expenseCategory, 'amount': spentAmt, 'description': expenseDesc}
    return expense

def inputExpenses():
    expense = userInput()
    invalidFlag = validateExpenses(expense)
    if not invalidFlag:
        expenses.append(expense)
    return expenses

def readStoredExpenses(expenses):
    for expense in expenses:
        if expense.get('missing_info') == None:
            print("Date of Expense : ", expense["date"])
            print("Expense Category: ", expense["category"])
            print("Amount Spent: ", expense["amount"])
            print("Expense Description: ", expense["description"])
        

def validateExpenses(expense):
    invalidFlag = False
    if not expense["category"] or not expense["amount"]:
        expense["missing_info"] = True
        invalidFlag = True
        while invalidFlag:
            print(f"Record missing mandatory info, flagged as such {expense}, please re-enter")
            inputExpenses()
            break
    return invalidFlag

def setMonthlyBudget():
    budget = input("Enter the total amount you want to budget for the month: ")
    return budget

def calculateExpenses():
    global total_expense
    saved_expenses = loadExpenseData()
    if saved_expenses is not None:
        for expense in saved_expenses:
            if expense["amount"] and expense.get('missing_info') == None:
                total_expense = total_expense + int(expense.get("amount"))

def writeInCsv(expenses):
    global file_name
    global ABSOLUTE_PATH
    global FIELD_NAMES
    if len(expenses) > 0 :
        date = expenses[0].get("date")
        file_name = ABSOLUTE_PATH + "/expenses_" + date.strftime("%B") + date.strftime("%Y") + ".csv"
        if os.path.exists(file_name):
            write_mode = "a"
        else:
            write_mode = "w"
        with open(file_name, write_mode, newline="") as csvfile:        
            writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES, extrasaction="ignore")
            if write_mode == "w":
                writer.writeheader()
            writer.writerows(expenses)

def loadExpenseData():
    global file_name
    global ABSOLUTE_PATH
    load_expenses = []
    date = datetime.datetime.now().date()
    file_name = ABSOLUTE_PATH + "/expenses_" + date.strftime("%B") + date.strftime("%Y") + ".csv"
    try:
        with open(file=file_name, mode="r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row['date'], row['category'], row['amount'], row['description'])
                load_expenses.append(row)
        return load_expenses
    except:
        print("No expenses saved yet. Please make another choice.")

def menu():
    for k,v in MENU.items():
        print(k + " " + v)
    choice = input(f"What would you like to do today, choose one: (enter the number)")
    return choice

if __name__ == "__main__":
    
    budgetedAmount = setMonthlyBudget()
    print(f"Your monthly budget is set to: {budgetedAmount}")

    while(True):
        choice = menu()
        match choice:
            case '1':
                expenses = inputExpenses()
                writeInCsv(expenses)
                expenses=[]
            case '2':
                saved_expenses = loadExpenseData()
            case '3':
                calculateExpenses()
                print(f"Your monthly budget is set to: {budgetedAmount}")
                print(f"Your total expenses so far are {total_expense}")
                if total_expense > int(budgetedAmount) :
                    print("You've exceeded your budget!")
                else :
                    print(f"You've {int(budgetedAmount) - total_expense} left for the month")
            case '4':
                writeInCsv(expenses)
            case '5':
                quit()


    
    
    


    
    
    


