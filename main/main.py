import database
import matplotlib.pyplot as plt
from datetime import datetime
import csv

def main():
    while True:
        print("\n=== Expense Tracker ===")
        print("1. Add a new expense")
        print("2. View all expenses")
        print("3. Delete an expense")
        print("4. Filter expenses")
        print("5. Generate monthly report")
        print("6. Export expenses to CSV")
        print("7. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_new_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            delete_expense()
        elif choice == "4":
            filter_expenses()
        elif choice == "5":
            generate_monthly_report()
        elif choice == "6":
            export_expenses_to_csv()
        elif choice == "7":
            database.close_connection()  # Ensure proper closing of connection
            print("Thank You!")
            break
        else:
            print("Invalid choice. Please try again.")

def add_new_expense():
    try:
        amount = float(input("Enter expense amount: "))
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")
        
        category = input("Enter category (e.g., food, travel): ")
        if not category:
            raise ValueError("Category cannot be empty.")
        
        description = input("Enter a short description: ")
        date_input = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
        
        # Validate date format
        if date_input:
            date = datetime.strptime(date_input, '%Y-%m-%d').strftime('%Y-%m-%d')
        else:
            date = datetime.now().strftime('%Y-%m-%d')

        database.add_expense(amount, category, description, date)
        print("Expense added successfully!")
    except ValueError as e:
        print(f"Invalid input: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def view_expenses():
    expenses = database.get_expenses()
    print("\n=== All Expenses ===")
    for expense in expenses:
        print(f"ID: {expense[0]}, Amount: {expense[1]}, Category: {expense[2]}, Description: {expense[3]}, Date: {expense[4]}")

def delete_expense():
    try:
        expense_id = int(input("Enter the ID of the expense to delete: "))
        database.delete_expense(expense_id)
        print("Expense deleted successfully!")
    except ValueError:
        print("Invalid input! Please try again.")

def filter_expenses():
    print("1. Filter by category")
    print("2. Filter by date range")
    choice = input("Enter your choice: ")

    if choice == "1":
        category = input("Enter the category to filter by: ")
        filtered_expenses = database.filter_by_category(category)
        display_filtered_expenses(filtered_expenses)
    elif choice == "2":
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        filtered_expenses = database.filter_by_date_range(start_date, end_date)
        display_filtered_expenses(filtered_expenses)
    else:
        print("Invalid choice!")

def display_filtered_expenses(expenses):
    if not expenses:
        print("No expenses found.")
    else:
        for expense in expenses:
            print(f"ID: {expense[0]}, Amount: {expense[1]}, Category: {expense[2]}, Description: {expense[3]}, Date: {expense[4]}")

def generate_monthly_report():
    year = input("Enter year (YYYY): ")
    month = input("Enter month (MM): ")
    start_date = f"{year}-{month}-01"
    end_date = f"{year}-{month}-31"  # Simplified; better to handle month lengths dynamically

    expenses = database.filter_by_date_range(start_date, end_date)
    if not expenses:
        print("No expenses found for the selected month.")
        return
    
    display_filtered_expenses(expenses)
    
    # Create a category-wise summary
    summary = {}
    for expense in expenses:
        category = expense[2]
        amount = expense[1]
        summary[category] = summary.get(category, 0) + amount
    
    print("\n=== Monthly Report ===")
    for category, total in summary.items():
        print(f"{category}: ${total:.2f}")

def export_expenses_to_csv():
    expenses = database.get_expenses()
    if not expenses:
        print("No expenses to export.")
        return

    filename = "expenses.csv"
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['ID', 'Amount', 'Category', 'Description', 'Date'])
        csvwriter.writerows(expenses)
    
    print(f"Expenses successfully exported to {filename}.")

if __name__ == "__main__":
    main()
