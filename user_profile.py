# user_profile.py
from config import get_db_connection

def get_user_profile(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user_profile = cursor.fetchone()
    cursor.close()
    conn.close()
    return user_profile

def update_user_profile(user_id, age, gender, weight, height, dietary_preferences, allergies, health_goals):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET age = %s, gender = %s, weight = %s, height = %s, dietary_preferences = %s, allergies = %s, health_goals = %s
        WHERE user_id = %s
    """, (age, gender, weight, height, dietary_preferences, allergies, health_goals, user_id))
    conn.commit()
    cursor.close()
    conn.close()
