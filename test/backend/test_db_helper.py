from backend import db_helper

def test_fetch_expenses_for_date_valid():
    expenses = db_helper.fetch_expenses_for_date("2024-08-15")
    
    assert len(expenses) == 1
    assert expenses[0]['amount'] == 10.0
    assert expenses[0]['category'] == 'Shopping'
    assert expenses[0]['notes'] == 'Bought potatoes'

def test_fetch_expenses_for_date_invalid():
    expenses = db_helper.fetch_expenses_for_date("2025-08-15")
    
    assert len(expenses) == 0

def test_fetch_expense_summary():
    expenses = db_helper.fetch_expense_summary("2024-08-01", "2024-08-15")
    
    assert len(expenses) > 1
  