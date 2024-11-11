from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the food dataset
def load_food_data(file_name=r'C:\Users\Kalyani Shimpi\Desktop\project\app2.py'):

    try:
        return pd.read_csv(file_name)
    except FileNotFoundError:
        print("Food dataset not found!")
        return None

# Example function for calculating insulin for blood sugar levels
def insulin_for_blood_sugar(blood_sugar_level):
    if blood_sugar_level > 100:
        insulin_units = (blood_sugar_level - 100) / 50
    else:
        insulin_units = 0
    return insulin_units

# Example function for calculating insulin based on food intake
def insulin_for_food_intake(food_name, serving_input, food_data):
    food = food_data[food_data['Food'].str.lower() == food_name.lower()]
    if not food.empty:
        servings = extract_quantity(serving_input)
        if servings == 0:
            return 0

        carbs_per_serving = food.iloc[0]['Carbs_per_serving']
        total_carbs = carbs_per_serving * servings
        return total_carbs
    else:
        print(f"Food item '{food_name}' not found in the dataset!")
        return 0

# Example helper to extract quantity from serving input
def extract_quantity(serving_input):
    # Example regex to find numbers in the input (for simplicity)
    import re
    quantity = re.findall(r'\d+', serving_input)
    if quantity:
        return int(quantity[0])
    return 0

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/calculate-insulin', methods=['POST'])
def calculate_insulin():
    data = request.json
    blood_sugar = float(data['blood_sugar'])
    food_items = data['food_items']
    
    # Calculate insulin for blood sugar
    insulin_blood_sugar = insulin_for_blood_sugar(blood_sugar)
    
    # Load food data
    food_data = load_food_data()
    if food_data is None:
        return jsonify({'error': 'Food data not found'}), 500

    # Calculate insulin for food intake
    total_carbs = 0
    for item in food_items:
        total_carbs += insulin_for_food_intake(item['name'], item['serving'], food_data)
    
    # Calculate insulin for food (assuming 1 unit per 10 grams of carbs)
    insulin_food = total_carbs / 10
    
    # Total insulin
    total_insulin = insulin_blood_sugar + insulin_food
    
    return jsonify({'total_insulin': total_insulin})

if __name__ == '__main__':
    app.run(debug=True)
