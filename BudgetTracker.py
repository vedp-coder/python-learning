from datetime import datetime

class BudgetTracker:
    def __init__(self):
        self.transactions = []
        self.categories = ['food', 'transport', 'entertainment', 'bills', 'other']
    
    def add_transaction(self, amount, category, description):
        if category not in self.categories:
            print("Invalid category!")
            return
            
        transaction = {
            'date': datetime.now(),
            'amount': amount,
            'category': category,
            'description': description
        }
        self.transactions.append(transaction)
        print("Transaction added successfully!")
    
    def view_transactions(self):
        if not self.transactions:
            print("No transactions found!")
            return
            
        print("\nTransaction History:")
        print("-" * 50)
        for t in self.transactions:
            print(f"Date: {t['date'].strftime('%Y-%m-%d %H:%M')}")
            print(f"Amount: ${t['amount']:.2f}")
            print(f"Category: {t['category']}")
            print(f"Description: {t['description']}")
            print("-" * 50)
    
    def get_total_spending(self):
        total = sum(t['amount'] for t in self.transactions)
        print(f"\nTotal spending: ${total:.2f}")

def main():
    budget = BudgetTracker()
    
    while True:
        print("\n1. Add transaction")
        print("2. View transactions")
        print("3. View total spending")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            amount = float(input("Enter amount: $"))
            print("\nCategories:", ', '.join(budget.categories))
            category = input("Enter category: ").lower()
            description = input("Enter description: ")
            budget.add_transaction(amount, category, description)
        
        elif choice == '2':
            budget.view_transactions()
        
        elif choice == '3':
            budget.get_total_spending()
        
        elif choice == '4':
            print("Thank you for using Budget Tracker!")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
