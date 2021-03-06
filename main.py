import time
from time import gmtime, strftime
from datetime import datetime,timezone,timedelta
import requests
import datetime
#import reverse_geocoder as rg
from pprint import pprint
from config import open_weather_token

from pytz import timezone

#Код
def get_weather(city, open_weather_token):

    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        pprint(data)

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

                            ###--------ПАРАМЕТРЫ КОТОРЫЕ БУДЕМ ВЫЧИСЛЯТЬ--------###

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        country = data["sys"]["country"]
        wind = data["wind"]["speed"]
        time_zone = datetime.datetime.fromtimestamp(data["timezone"])
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        ###------ВРЕМЯ МОСКОВСКОЕ ПЛЮС ВРЕМЯ ПО ЗОНАМ--------#####
###---ПЕРЕВОДИМ ЗНАЧЕНИЕ ВРЕМЕНИ ВЗЯТОЕ ИЗ DATETIME В СТРОКУ,УДАЛЯЕМ ЛИШНИЕ ЗНАКИ---###
        ###---РАЗБИВАЕМ НА ЭЛЕМЕНТЫ,ДОБАВЛЯЕМ В СПИСОК---###
        ###---ДОСТАЁМ ИЗ СПИСКА И ВЫВОДИМ ТОЛЬКО ЧАСЫ И МИНУТЫ---###
        zone1 = str(time_zone)
        zone2 = zone1.replace("-", " ")
        zone3 = zone2.replace(":", " ")
        zone4 = zone3.replace(" ", " ")
        zone5 = [zone4[0:12]]
        zone5.append(zone4[11:13])
        zone5.append(zone4[14:16])
        zone5.append(zone4[17:19])
        dict_time = {}
        plus_hours = datetime.datetime.now().strftime(f'%H')
        plus_minutes = datetime.datetime.now().strftime(f'%M')
        plus_hours = int(plus_hours)
        main_time = int(zone5[1])
        dict_time["hour"] = plus_hours + main_time
        dict_time["minutes"] = int(zone5[2])

        if dict_time["hour"] > 23 and dict_time["hour"] > 10:
            dict_time["hour"] = dict_time["hour"] - 24
            if dict_time["hour"] > 23 and dict_time["hour"] > 10:
                dict_time["hour"] = dict_time["hour"] - 24
                print("Время: ", dict_time["hour"], ":", plus_minutes)

        if dict_time["hour"] < 10:
            dict_time["hour"] = str(dict_time["hour"])
            dict_time["hour"] = "0" + dict_time["hour"]
            print("Время: ", dict_time["hour"], ":", plus_minutes)
        else:
            print("Время: ", dict_time["hour"], ":", plus_minutes)


        print(f"Дата: {datetime.datetime.now().strftime(f'%d-%m-%Y')}\n"
              f"Страна: {country}\nПогода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
              #f"Зона : {time_zone}\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
              f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
              f"С вами был прогноз погоды!"
              )

    except Exception as ex:
        print(ex)
        print("Проверьте название города")

        # # # Current time in UTC Правильное время
        # now_utc = datetime.datetime.now(datetime.timezone.utc)
        # tm_rus = timezone('Europe/Moscow')
        # time_RU = now_utc.astimezone(tm_rus)
        # print("UTC Time: ", time_RU)

def main():
    city = input("Введите город: ")
    get_weather(city, open_weather_token)


if __name__ == '__main__':
    main()