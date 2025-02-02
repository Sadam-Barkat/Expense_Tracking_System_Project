from fastapi import FastAPI, HTTPException
from datetime import date
from backend import db_helper
from typing import List
from pydantic import BaseModel

app = FastAPI()

class Expense(BaseModel):
    amount: float
    category: str
    notes: str

class DateRange(BaseModel):
    start_date: date
    end_date: date


@app.get('/expenses/{expense_date}', response_model=List[Expense])
def get_expenses(expense_date:date):
    expenses = db_helper.fetch_expenses_for_date(expense_date)
    if expenses is None:
        raise HTTPException(status_code=500, detail="Faild to retrive expenses from database")
    return expenses

@app.post('/expenses/{expense_date}')
def add_or_update_expenses(expense_date:date, expenses:List[Expense]):
    db_helper.delete_expenses_for_date(expense_date)
    for expense in expenses:
        db_helper.insert_expense(expense_date, expense.amount, expense.category, expense.notes)
    return {"message":"Expenses Updated Successfully"}   

@app.post('/analytics_category')
def get_analytics_category(date_range: DateRange):
    expense_by_category = db_helper.fetch_expense_by_category(date_range.start_date, date_range.end_date)
    if expense_by_category is None:
        raise HTTPException(status_code=500, detail="Faild to retrive expense category from database")
    
    breakdown = {}
    total = sum([row['total'] for row in expense_by_category])  
    for row in expense_by_category:
        percentage = (row['total'] / total) * 100 if total != 0 else 0

        breakdown[row['category']] = {
            'total':row['total'],
            'percentage':percentage
        }
    return breakdown

@app.get('/analytics_month')
def get_analytics_month():
    try:
        expense_by_month = db_helper.fetch_expense_by_month()
        if not expense_by_month:
            raise HTTPException(status_code=404, detail="No expense data found")
        return expense_by_month
    except Exception as e:
        print(f"Error in get_analytics_month: {e}")  # Log the error
        raise HTTPException(status_code=500, detail="Internal Server Error")

