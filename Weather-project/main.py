from flask import Flask, render_template, request
import requests
import datetime
import pytz  # Import the pytz library for timezone conversion

app = Flask(__name__)

# Route for the home page
@app.route('/', methods=['GET', 'POST'])

def index():

    if request.method == 'POST':
        # Get the city name from the form
        city = request.form.get('city')
        
        # Your API key (replace 'Your_OpenWeatherMap_API_Key' with your actual API key)
        api_key = 'f8a7b36e99e5c0af8a37d79e9b0cb3be'
        
        # URL to fetch the weather data
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        
        # Make a request to the OpenWeatherMap API
        response = requests.get(url)
        
        # Convert the response to JSON format
        weather_data = response.json()
        
        # Extracting required information
        
        # Assuming weather_data["dt"] contains the Unix timestamp
        unix_timestamp = weather_data["dt"]
        sunrise_unix_timestamp = weather_data["sys"]["sunrise"]
        sunset_unix_timestamp = weather_data["sys"]["sunset"]

        # Convert Unix timestamp to a datetime object
        datetime_object = datetime.datetime.fromtimestamp(unix_timestamp)
        sunrise_datetime_object = datetime.datetime.fromtimestamp(sunrise_unix_timestamp)
        sunset_datetime_object = datetime.datetime.fromtimestamp(sunset_unix_timestamp)

        # Convert UTC time to the timezone of Cambodia
        cambodia_timezone = pytz.timezone('Asia/Phnom_Penh')
        datetime_object = datetime_object.astimezone(cambodia_timezone)
        sunrise_datetime_object = sunrise_datetime_object.astimezone(cambodia_timezone)
        sunset_datetime_object = sunset_datetime_object.astimezone(cambodia_timezone)

        # Add 10 minutes to the datetime objects
        datetime_object += datetime.timedelta(minutes=4)
        

        # Format the datetime object as a string
        #formatted_time = datetime_object.strftime('%H:%M:%S %d-%m-%Y')
        #sunrise_time = sunrise_datetime_object.strftime('%H:%M:%S')                    #Time 24
        #sunset_time = sunset_datetime_object.strftime('%H:%M:%S')

        formatted_time = datetime_object.strftime('%I:%M:%S %p %d-%m-%Y')
        sunrise_time = sunrise_datetime_object.strftime('%I:%M:%S %p')                  # Time 12
        sunset_time = sunset_datetime_object.strftime('%I:%M:%S %p')

        # Temperature conversion from Kelvin to Celsius
        
        temperature_celsius = round(weather_data['main']['temp'] - 273.15)
        #formatted1_temperature = f"{temperature_celsius:.2f}"
        
        
        feels_temperature_celsius = round(weather_data["main"]["feels_like"] - 273.15)
        #formatted2_temperature = f"{feels_temperature_celsius:.2f}"
        
        
        weather = {

            'city': city,
            'temperature': temperature_celsius,  #formatted1_temperature
            'description': weather_data['weather'][0]['description'],
            'icon': weather_data['weather'][0]['icon'],
            'time': formatted_time,
            'date': weather_data["dt"],
            'feels_like': feels_temperature_celsius,       #formatted2_temperature 
            'wind_speed': weather_data["wind"]["speed"], 
            'humidity': weather_data["main"]["humidity"],
            'uv_index': weather_data.get("uvi", "N/A"),                                                            #making by Sao Sambath and group member#
            #'visibility': weather_data[" visibility"],  
            #'pressure': weather_data["main"]["pressure"], 
            'sunrise': sunrise_time,
            'sunset': sunset_time,
        }
        
        # Render the template with the weather information
        return render_template('weather.html', weather=weather)
    
    # If it's a GET request, just render the form
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
