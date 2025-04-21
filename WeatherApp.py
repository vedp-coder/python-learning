import requests

def get_weather(city):
    api_key = 'your_openweathermap_api_key'  # Get a free API key from openweathermap.org
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"Weather in {city}: {data['weather'][0]['main']}, {data['main']['temp']}°C")
    else:
        print("City not found or API error!")

if __name__ == "__main__":
    city = input("Enter city name: ")
    get_weather(city)
