import unittest
import database

class TestExpenseTracker(unittest.TestCase):

    def test_add_expense(self):
        database.add_expense(100, "Food", "Lunch", "2024-10-10")
        expenses = database.get_expenses()
        self.assertEqual(expenses[-1][1], 100)  # Check if the last added expense is correct

    def test_delete_expense(self):
        database.add_expense(50, "Travel", "Bus fare", "2024-10-11")
        expenses_before = database.get_expenses()
        database.delete_expense(expenses_before[-1][0])  # Delete the last expense
        expenses_after = database.get_expenses()
        self.assertEqual(len(expenses_after), len(expenses_before) - 1)

if __name__ == '__main__':
    unittest.main()
