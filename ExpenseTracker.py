import csv
from datetime import datetime

def add_expense(amount, category, note):
    with open('expenses.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), amount, category, note])

def view_expenses():
    try:
        with open('expenses.csv', 'r') as file:
            reader = csv.reader(file)
            print("Date\t\t\tAmount\tCategory\tNote")
            for row in reader:
                print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}")
    except FileNotFoundError:
        print("No expenses recorded yet.")

if __name__ == "__main__":
    while True:
        choice = input("1. Add Expense\n2. View Expenses\n3. Quit\nChoose: ")
        if choice == '1':
            amt = input("Amount: ")
            cat = input("Category: ")
            note = input("Note: ")
            add_expense(amt, cat, note)
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            break
        else:
            print("Invalid choice.")
