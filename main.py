from twilio.rest import Client
import keys
import requests
import schedule
import time



client = Client(keys.account_sid, keys.auth_token)

def get_weather():
    base_url = f"https://api.openweathermap.org/data/2.5/weather?lat=40.7128&lon=-74.0060&units=imperial&appid={keys.OPENWEATHERMAP_API_KEY}"
    response = requests.get(base_url)
    data = response.json()
    return data
def get_clothing_recommendation(temperature, weather_description):
    if "rain" in weather_description.lower():
        return "Don't forget an umbrella and a waterproof jacket."
    elif "snow" in weather_description.lower():
        return "Wear warm layers and bring a winter coat."
    elif temperature >= 80:
        return "It's hot! Wear shorts, a light shirt, and sunscreen."
    elif 70 <= temperature < 80:
        return "It's warm! Shorts, a t-shirt, and sunglasses are a good choice."
    elif 60 <= temperature < 70:
        return "A light jacket and jeans would be comfortable."
    elif 50 <= temperature < 60:
        return "You may want a sweater or a long-sleeve shirt."
    elif temperature < 50:
        return "Bundle up with a heavy coat, scarf, and gloves."
    else:
        return "It's a good idea to dress comfortably for the weather."


def send_weather_update():
    weather_data = get_weather()
    
    if 'main' in weather_data:
        temperature = weather_data['main']['temp']
        weather_description = weather_data['weather'][0]['description']
        clothing_recommendation = get_clothing_recommendation(temperature, weather_description)
        message_body = f"Good Morning! The weather in New York City is {weather_description} with a temperature of {temperature}°F. {clothing_recommendation}"
        
        try:
            message = client.messages.create(
                body=message_body,
                from_=keys.twilio_number,
                to=keys.target_number
            )
            print(f"Message sent: {message.sid}")
        except Exception as e:
            print(f"Error sending message: {str(e)}")
    else:
        print("Error: Unable to fetch weather data")

if __name__ == "__main__": 
   schedule.every().day.at("08:00").do(send_weather_update)

   while True:
    schedule.run_pending()
    time.sleep(1)