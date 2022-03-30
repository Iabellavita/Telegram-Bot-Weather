from pprint import pprint
from config import API_KEY
import requests
import datetime


def get_weather(city, API_KEY):
    code_to_smile = {
        "CLear": "Ясно \U00002600 \U0001F324",
        "Clouds": "Облачно \U000026C5 \U000026C5",
        "Rain": "Дождь \U0001F326",
        "Drizzle": "Дождь \U0001F327 \U000026C8",
        "Thunderstorm": "Гроза \U000026A1 \U0001F329",
        "Snow": "Снег \U00002744 \U0001F328",
        "Mist": "Туман \U0001F32B \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        )
        data = r.json()

        # КРАСИВЫЙ ВВЫОД JSON
        # pprint(data)

        city = data["name"]
        cur_weather = data["main"]["temp"]

        # Взяли с сайта возможные описания погоды и создали на их фоне свой словарь и в случае если слово
        # там совпадет со словом в словаре то вывести то шо в словаре
        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотори в окно, сложно определить погоду...) "

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind_speed = data["wind"]["speed"]
        sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset = datetime.datetime.fromtimestamp((data["sys"]["sunset"]))
        length_day = sunset - sunrise
        print(f"{' ' * 10} {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} {wd}\n"
              f"Погода в городе: {city}\nТемпература воздуха: {cur_weather} С° {wd}\n"
              f"Влажность: {humidity} %\nДавление: {pressure} мм.рт.ст.\nСкорость ветра: {wind_speed} м/с\n"
              f"Рассвет: {sunrise}\nЗакат: {sunset}\nПродолжительность дня: {length_day}\n"
              f"{' ' * 10} Хорошего дня!:)")




    except Exception as ex:
        print(ex)
        print("Проверьте на правильность введение города!")


def main():
    city = input("Введите Ваш город: ")
    get_weather(city, API_KEY)


if __name__ == "__main__":
    main()
