import requests
import datetime
# from config import TG_TOKEN, API_KEY
from os import getenv
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot_token = getenv("TG_TOKEN")
if not bot_token:
    exit("Error: no token provided")

bot = Bot(token=bot_token, parse_mode="HTML")
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer("Привет! Напиши город! \U0001F609")


# Можно таким образом оформить приветствие c єкранированием
# @dp.message_handler()
# async def greetings(message: types.Message):
#     await message.answer(f"Привет, <b>{fmt.quote_html(message.text)}</b>")
#     # А можно и так:
#     # await message.answer(fmt.text("Привет,", hbold(message.text)), parse_mode=""HTML)

@dp.message_handler()
async def get_weather(message: types.Message):
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
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={getenv('API_KEY')}&units=metric"
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

        # parse_mode=types.ParseMode.HTML, parse_mode="HTML" - можем пользоваться тегами
        # для обработки вывода текста (жирный, курсив и тд)
        await message.answer(f"<b>{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</b>\n\n"
                             f"Погода в городе: <b><u>{city}</u></b>\nТемпература воздуха: {cur_weather} С°\n{wd}\n\n"
                             f"Влажность: {humidity} %\nДавление: {pressure} мм.рт.ст.\n"
                             f"Скорость ветра: {wind_speed} м/с\n"
                             f"Рассвет: {sunrise.strftime('%H:%M')}\nЗакат: {sunset.strftime('%H:%M')}\n"
                             f"Продолжительность дня: {length_day}\n\n"
                             f"<i>Хорошего дня!</i>\U0001F917 \U0001F60E")




    except:
        await message.reply("\U0001F914 Проверьте на правильность введение города! \U0001F914")


if __name__ == "__main__":
    executor.start_polling(dp)
