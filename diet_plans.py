# diet_plans.py
from config import get_db_connection

def create_meal_plan(user_id, plan_date, meal_type, food_items, calories, protein, fat, carbs):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO meal_plans (user_id, plan_date, meal_type, food_items, calories, protein, fat, carbs)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (user_id, plan_date, meal_type, food_items, calories, protein, fat, carbs))
    conn.commit()
    cursor.close()
    conn.close()

def get_meal_plan(user_id, plan_date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM meal_plans WHERE user_id = %s AND plan_date = %s", (user_id, plan_date))
    plans = cursor.fetchall()
    cursor.close()
    conn.close()
    return plans
