import pandas as pd
from flask import Flask, render_template, request, jsonify
import joblib

app = Flask(__name__)

model = joblib.load('/Users/yashmakadia/Documents/Yash Makadia/Project/Car Price Prediction/model.pkl')
car = pd.read_csv('clean_car.csv')

@app.route('/')
def index():
    car_name = sorted(car['name'].unique())
    year = sorted(car['year'].unique(), reverse=True)
    km_driven = sorted(car['km_driven'].unique(), reverse=True)
    fuel = sorted(car['fuel'].unique())
    transmission = sorted(car['transmission'].unique())
    owner = sorted(car['owner'].unique())
    mileage = sorted(car['mileage(km/ltr/kg)'].unique(), reverse=True)
    engine = sorted(car['engine'].unique(), reverse=True)
    max_power = sorted(car['max_power'].unique(), reverse=True)
    seats = sorted(car['seats'].unique(), reverse=True)

    return render_template('index.html', car_name=car_name,
                           year=year, km_driven=km_driven, fuel=fuel,
                           transmission=transmission, owner=owner, mileage=mileage, engine=engine, max_power=max_power,
                           seats=seats)


@app.route('/predict', methods=['POST'])
def predict():
    if request.is_json:
        input_data = request.get_json()
    else:
        car_name = request.form.get('car_name')
        year = int(request.form.get('year'))
        km_driven = int(request.form.get('km_driven'))
        fuel = request.form.get('fuel')
        transmission = request.form.get('transmission')
        owner = request.form.get('owner')
        mileage = float(request.form.get('mileage'))
        engine = int(request.form.get('engine'))
        max_power = float(request.form.get('max_power'))
        seats = int(request.form.get('seats'))

        input_data = {
            'name': car_name,
            'year': year,
            'km_driven': km_driven,
            'fuel': fuel,
            'transmission': transmission,
            'owner': owner,
            'mileage(km/ltr/kg)': mileage,
            'engine': engine,
            'max_power': max_power,
            'seats': seats
        }

    # Convert to DataFrame and ensure data types are correct
    input_df = pd.DataFrame([input_data])

    # Debugging information
    print("Input DataFrame:")
    print(input_df)

    # Ensure correct data types
    input_df['name'] = input_df['name'].astype(str)
    input_df['year'] = input_df['year'].astype(int)
    input_df['km_driven'] = input_df['km_driven'].astype(int)
    input_df['fuel'] = input_df['fuel'].astype(str)
    input_df['transmission'] = input_df['transmission'].astype(str)
    input_df['owner'] = input_df['owner'].astype(str)
    input_df['mileage(km/ltr/kg)'] = input_df['mileage(km/ltr/kg)'].astype(float)
    input_df['engine'] = input_df['engine'].astype(int)
    input_df['max_power'] = input_df['max_power'].astype(float)
    input_df['seats'] = input_df['seats'].astype(int)

    # Debugging information after type conversion
    print("Converted DataFrame:")
    print(input_df)

    try:
        # Make the prediction
        prediction = model.predict(input_df)
        return jsonify({'prediction': prediction[0]})
    except Exception as e:
        # Debugging information for exception
        print("Exception occurred:")
        print(e)
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)


















































# import pandas as pd
# from flask import Flask, render_template, request, jsonify
# import pickle
# import joblib
#
# app = Flask(__name__)
#
# # model = pickle.load(open("/Users/yashmakadia/Documents/Yash Makadia/Project/Car Price Prediction/model.pkl", "rb"))
# model = joblib.load('/Users/yashmakadia/Documents/Yash Makadia/Project/Car Price Prediction/model.pkl')
# car = pd.read_csv('clean_car.csv')
#
#
# @app.route('/')
# def index():
#     car_name = sorted(car['name'].unique())
#     year = sorted(car['year'].unique(), reverse=True)
#     km_driven = sorted(car['km_driven'].unique(), reverse=True)
#     fuel = sorted(car['fuel'].unique())
#     transmission = sorted(car['transmission'].unique())
#     owner = sorted(car['owner'].unique())
#     mileage = sorted(car['mileage(km/ltr/kg)'].unique(), reverse=True)
#     engine = sorted(car['engine'].unique(), reverse=True)
#     max_power = sorted(car['max_power'].unique(), reverse=True)
#     seats = sorted(car['seats'].unique(), reverse=True)
#
#     return render_template('index.html', car_name=car_name,
#                            year=year, km_driven=km_driven, fuel=fuel,
#                            transmission=transmission, owner=owner, mileage=mileage, engine=engine, max_power=max_power,
#                            seats=seats)
#
#
# @app.route('/predict', methods=['POST'])
# def predict():
#     car_name = request.form.get('car_name')
#     year = int(request.form.get('year'))
#     km_driven = int(request.form.get('km_driven'))
#     fuel = request.form.get('fuel')
#     transmission = request.form.get('transmission')
#     owner = request.form.get('owner')
#     mileage = int(request.form.get('mileage'))
#     engine = int(request.form.get('engine'))
#     max_power = request.form.get('max_power')
#     seats = int(request.form.get('seats'))
#     if request.is_json:
#         input_data = request.get_json()
#     else:
#         car_name = request.form.get('car_name')
#         year = int(request.form.get('year'))
#         km_driven = int(request.form.get('km_driven'))
#         fuel = request.form.get('fuel')
#         transmission = request.form.get('transmission')
#         owner = request.form.get('owner')
#         mileage = float(request.form.get('mileage'))
#         engine = int(request.form.get('engine'))
#         max_power = float(request.form.get('max_power'))
#         seats = int(request.form.get('seats'))
#
#         input_data = {
#             'name': car_name,
#             'year': year,
#             'km_driven': km_driven,
#             'fuel': fuel,
#             'transmission': transmission,
#             'owner': owner,
#             'mileage(km/ltr/kg)': mileage,
#             'engine': engine,
#             'max_power': max_power,
#             'seats': seats
#         }
#
#     input_df = pd.DataFrame([input_data])  # Convert to DataFrame
#
#     # Make the prediction
#     prediction = model.predict(input_df)
#
#     return jsonify({'prediction': prediction[0]})
#     # prediction = model.predict(
#     #     [[car_name, year, km_driven, fuel, transmission, owner, mileage, engine, max_power, seats]],
#     #     columns=['name', 'year', 'km_driven', 'fuel', 'transmission', 'owner', 'mileage(km/ltr/kg)', 'engine',
#     #              'max_power', 'seats'])
#
#     # return str(prediction[0])
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
