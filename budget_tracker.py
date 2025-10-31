# PROJECT: Personal Budget Tracker
# Let's combine everything we've learned!

import datetime
import re

class BudgetTracker:
    def __init__(self):
        self.transactions = []
        self.categories = set()
    
    def add_transaction(self, amount, description, category, date=None):
        """Add a new transaction"""
        if date is None:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        transaction = {
            'amount': amount,
            'description': description,
            'category': category,
            'date': date
        }
        
        self.transactions.append(transaction)
        self.categories.add(category)
        print(f"Added: {description} - ${amount:.2f} on {date}")
    
    def view_transactions(self):
        """View all transactions"""
        if not self.transactions:
            print("No transactions recorded yet!")
            return
        
        print("\n ALL TRANSACTIONS")
        print("-" * 50)
        
        # Separate income and expenses for better display
        income_transactions = [t for t in self.transactions if t['amount'] > 0]
        expense_transactions = [t for t in self.transactions if t['amount'] < 0]
        
        print("\n--- INCOME ---")
        if income_transactions:
            for i, transaction in enumerate(income_transactions, 1):
                print(f"{i}. {transaction['date']} | {transaction['description']:20} | "
                      f"${transaction['amount']:8.2f} | {transaction['category']}")
        else:
            print("No income recorded yet!")
        
        print("\n--- EXPENSES ---")
        if expense_transactions:
            for i, transaction in enumerate(expense_transactions, 1):
                print(f"{i}. {transaction['date']} | {transaction['description']:20} | "
                      f"${transaction['amount']:8.2f} | {transaction['category']}")
        else:
            print("No expenses recorded yet!")
    
    def get_balance(self):
        """Calculate current balance"""
        total_income = sum(t['amount'] for t in self.transactions if t['amount'] > 0)
        total_expenses = sum(t['amount'] for t in self.transactions if t['amount'] < 0)
        balance = total_income + total_expenses  # Expenses are negative
        
        print(f"\n FINANCIAL SUMMARY")
        print("-" * 30)
        print(f"Total Income: ${total_income:.2f}")
        print(f"Total Expenses: ${-total_expenses:.2f}")  # Show as positive
        print(f"Current Balance: ${balance:.2f}")
        
        # Add budget advice
        if balance < 0:
            print(" WARNING: You are spending more than you earn!")
        elif balance < total_income * 0.1:  # Less than 10% of income saved
            print(" TIP: Try to save more for emergencies!")
        else:
            print(" Great! You're saving money!")
        
        return balance
    
    def spending_by_category(self):
        """Show spending by category"""
        if not self.transactions:
            print("No transactions to analyze!")
            return
        
        category_totals = {}
        
        for transaction in self.transactions:
            category = transaction['category']
            amount = transaction['amount']
            
            if amount < 0:  # Only count expenses (negative amounts)
                if category not in category_totals:
                    category_totals[category] = 0
                category_totals[category] += abs(amount)  # Convert to positive
        
        print("\n SPENDING BY CATEGORY")
        print("-" * 25)
        for category, total in category_totals.items():
            print(f"{category}: ${total:.2f}")

def validate_date(date_string):
    """Validate if the date string is in YYYY-MM-DD format and is a valid date"""
    try:
        # Check format using regex
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_string):
            return False, "Date must be in YYYY-MM-DD format (e.g., 2024-01-15)"
        
        # Parse the date components
        year, month, day = map(int, date_string.split('-'))
        
        # Check month range
        if month < 1 or month > 12:
            return False, "Month must be between 1 and 12"
        
        # Check day range
        if day < 1 or day > 31:
            return False, "Day must be between 1 and 31"
        
        # Check specific month-day combinations
        months_with_30_days = [4, 6, 9, 11]
        if month in months_with_30_days and day > 30:
            return False, f"Month {month} has only 30 days"
        
        # Check February
        if month == 2:
            # Leap year check
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                max_days = 29
            else:
                max_days = 28
            
            if day > max_days:
                return False, f"February {year} has only {max_days} days"
        
        # Create the date to validate it
        date_obj = datetime.datetime(year, month, day)
        
        # Check if date is not in the future
        if date_obj > datetime.datetime.now():
            return False, "Date cannot be in the future!"
        
        return True, "Valid date"
        
    except ValueError as e:
        return False, f"Invalid date: {str(e)}"

def get_valid_date(prompt):
    """Get a valid date from user input"""
    while True:
        date_input = input(prompt).strip()
        
        if not date_input:  # Allow empty for current date
            return None
        
        is_valid, message = validate_date(date_input)
        if is_valid:
            return date_input
        else:
            print(f" {message}")
            print("Please try again or press Enter for current date.")

def add_income(tracker):
    """Helper function to add income transactions"""
    print("\n--- ADD INCOME ---")
    
    while True:
        try:
            amount = float(input("Enter income amount: $"))
            if amount <= 0:
                print("Income amount must be positive!")
                continue
            break
        except ValueError:
            print("Please enter a valid number!")
    
    description = input("Enter description (e.g., Salary, Freelance, Bonus): ")
    category = "Income"
    
    print("Enter date in YYYY-MM-DD format (or press Enter for today's date): ")
    date = get_valid_date("Date: ")
    
    tracker.add_transaction(amount, description, category, date)
    
    add_more = input("Add another income source? (y/n): ").lower()
    return add_more == 'y'

def add_expenses(tracker):
    """Helper function to add expense transactions"""
    print("\n--- ADD EXPENSES ---")
    
    while True:
        try:
            amount = float(input("Enter expense amount: $"))
            if amount >= 0:
                print("Expense amount must be negative! I'll convert it to negative.")
                amount = -amount
            break
        except ValueError:
            print("Please enter a valid number!")
    
    description = input("Enter description (e.g., Rent, Groceries, Utilities): ")
    category = input("Enter category (e.g., Housing, Food, Transportation): ")
    
    print("Enter date in YYYY-MM-DD format (or press Enter for today's date): ")
    date = get_valid_date("Date: ")
    
    tracker.add_transaction(amount, description, category, date)
    
    add_more = input("Add another expense? (y/n): ").lower()
    return add_more == 'y'

def view_transactions_by_month(tracker):
    """View transactions for a specific month"""
    if not tracker.transactions:
        print("No transactions recorded yet!")
        return
    
    while True:
        month_input = input("Enter month and year (MM-YYYY) or press Enter for current month: ").strip()
        
        if not month_input:
            # Default to current month
            current_date = datetime.datetime.now()
            target_month = current_date.month
            target_year = current_date.year
            break
        else:
            # Validate month input
            try:
                if not re.match(r'^\d{2}-\d{4}$', month_input):
                    print("Please use MM-YYYY format (e.g., 01-2024)")
                    continue
                
                month, year = map(int, month_input.split('-'))
                if month < 1 or month > 12:
                    print("Month must be between 01 and 12")
                    continue
                
                if year < 1900 or year > datetime.datetime.now().year:
                    print(f"Year must be between 1900 and {datetime.datetime.now().year}")
                    continue
                
                target_month = month
                target_year = year
                break
                
            except ValueError:
                print("Invalid format. Please use MM-YYYY (e.g., 01-2024)")
                continue
    
    # Filter transactions for the selected month
    month_transactions = []
    for transaction in tracker.transactions:
        trans_date = datetime.datetime.strptime(transaction['date'], "%Y-%m-%d")
        if trans_date.month == target_month and trans_date.year == target_year:
            month_transactions.append(transaction)
    
    if not month_transactions:
        print(f"\nNo transactions found for {target_month:02d}-{target_year}")
        return
    
    print(f"\n TRANSACTIONS FOR {target_month:02d}-{target_year}")
    print("-" * 50)
    
    # Separate income and expenses
    income_transactions = [t for t in month_transactions if t['amount'] > 0]
    expense_transactions = [t for t in month_transactions if t['amount'] < 0]
    
    print("\n--- INCOME ---")
    if income_transactions:
        for i, transaction in enumerate(income_transactions, 1):
            print(f"{i}. {transaction['date']} | {transaction['description']:20} | "
                  f"${transaction['amount']:8.2f} | {transaction['category']}")
    else:
        print("No income for this month!")
    
    print("\n--- EXPENSES ---")
    if expense_transactions:
        for i, transaction in enumerate(expense_transactions, 1):
            print(f"{i}. {transaction['date']} | {transaction['description']:20} | "
                  f"${transaction['amount']:8.2f} | {transaction['category']}")
    else:
        print("No expenses for this month!")
    
    # Show monthly summary
    monthly_income = sum(t['amount'] for t in month_transactions if t['amount'] > 0)
    monthly_expenses = sum(t['amount'] for t in month_transactions if t['amount'] < 0)
    monthly_balance = monthly_income + monthly_expenses
    
    print(f"\n MONTHLY SUMMARY")
    print("-" * 20)
    print(f"Income: ${monthly_income:.2f}")
    print(f"Expenses: ${-monthly_expenses:.2f}")
    print(f"Balance: ${monthly_balance:.2f}")

# LET'S USE OUR BUDGET TRACKER!
def main():
    tracker = BudgetTracker()
    
    print("=== PERSONAL BUDGET TRACKER ===")
    print("Let's start by adding your income sources, then your expenses.\n")
    
    # First, add income
    print("STEP 1: ADD YOUR INCOME SOURCES")
    print("-" * 30)
    
    adding_income = True
    while adding_income:
        adding_income = add_income(tracker)
    
    # Then, add expenses
    print("\nSTEP 2: ADD YOUR EXPENSES")
    print("-" * 25)
    
    adding_expenses = True
    while adding_expenses:
        adding_expenses = add_expenses(tracker)
    
    # Show summary after initial setup
    print("\n" + "="*50)
    print("INITIAL SETUP COMPLETE!")
    print("="*50)
    tracker.get_balance()
    
    # Continue with main menu
    while True:
        print("\nWhat would you like to do next?")
        print("1. Add more income")
        print("2. Add more expenses")
        print("3. View all transactions")
        print("4. View transactions by month")
        print("5. Check balance")
        print("6. View spending by category")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            adding_income = True
            while adding_income:
                adding_income = add_income(tracker)
                
        elif choice == '2':
            adding_expenses = True
            while adding_expenses:
                adding_expenses = add_expenses(tracker)
                
        elif choice == '3':
            tracker.view_transactions()
            
        elif choice == '4':
            view_transactions_by_month(tracker)
            
        elif choice == '5':
            tracker.get_balance()
            
        elif choice == '6':
            tracker.spending_by_category()
            
        elif choice == '7':
            print("\nThank you for using the Personal Budget Tracker!")
            print("Final Summary:")
            tracker.get_balance()
            break
            
        else:
            print("Invalid choice! Please enter a number between 1-7.")

# Run the program
if __name__ == "__main__":
    main()