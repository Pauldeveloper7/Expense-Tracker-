import sqlite3

# Establish a connection to the database
connection = sqlite3.connect('expenses.db')
cursor = connection.cursor()

# Create the expenses table if it doesn't exist
def create_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            description TEXT,
            date TEXT
        )
    ''')
    connection.commit()

create_table()

# Function to add an expense
def add_expense(amount, category, description, date):
    cursor.execute('INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)', 
                   (amount, category, description, date))
    connection.commit()

# Function to get all expenses
def get_expenses():
    cursor.execute('SELECT * FROM expenses')
    return cursor.fetchall()

# Function to filter by category
def filter_by_category(category):
    cursor.execute('SELECT * FROM expenses WHERE category = ?', (category,))
    return cursor.fetchall()

# Function to filter by date range
def filter_by_date_range(start_date, end_date):
    cursor.execute('SELECT * FROM expenses WHERE date BETWEEN ? AND ?', (start_date, end_date))
    return cursor.fetchall()

# Function to delete an expense by ID
def delete_expense(expense_id):
    cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    connection.commit()

# Don't forget to close the connection when the program ends
def close_connection():
    connection.close()
