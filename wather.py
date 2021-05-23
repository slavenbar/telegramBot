import requests
from config import open_weather_token

def get_weather(city, open_weather_token):
    pass

def main():
    city = input("Введите город: ")
    get_weather(city, open_weather_token)

if __name__ == " __main__":
    main()