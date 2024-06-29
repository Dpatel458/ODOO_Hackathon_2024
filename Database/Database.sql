CREATE DATABASE diet_recommendation_system;

USE diet_recommendation_system;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    age INT,
    gender ENUM('male', 'female', 'other'),
    weight FLOAT,
    height FLOAT,
    dietary_preferences TEXT,
    allergies TEXT,
    health_goals TEXT
);

select*from users;

CREATE TABLE meal_plans (
    plan_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    plan_date DATE,
    meal_type ENUM('breakfast', 'lunch', 'dinner', 'snack'),
    food_items TEXT,
    calories INT,
    protein FLOAT,
    fat FLOAT,
    carbs FLOAT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


