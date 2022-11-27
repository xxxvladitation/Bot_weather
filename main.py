import telebot
from config import TOKEN, WEATHER_TOKEN
from requests import get
import emoji


class Emoji:
    city = emoji.emojize(':round_pushpin:', language='alias')
    temperature = emoji.emojize(':thermometer:', language='alias')
    weather = emoji.emojize(':partly_sunny:', language='alias')


def weather_view(city: str, api=WEATHER_TOKEN):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&APPID={api}'
    response_ = get(url)
    response = response_.json()
    if response.get('name'):
        main_ = response.get('weather')[0].get('main')
        temp_c = int(response.get("main").get('temp')) - 273.15
        city_ = response.get('name')
        return [main_, temp_c, city_]
    return None


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, f'''Hello, {message.from_user.first_name}
Enter city:''')


@bot.message_handler(content_types=['text'])
def main(message):
    weather: list[str] = weather_view(message.text)
    try:
        image = f"static_image/{weather[0].replace(' ', '_')}.jpeg"
    except TypeError or FileNotFoundError as error:
        if error:
            image = 'static_image/weather.png'
    if weather:
        bot.send_photo(message.chat.id, photo=open(image, 'rb'),
                       caption=f"{Emoji.city} <b>{weather[2]}</b>    {Emoji.weather} <b>{weather[0]}</b>    {Emoji.temperature} <b>{int(weather[1])} °C</b>",
                       parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, f'''{message.from_user.first_name}, this city is not exists 
Enter an existing city:''')


bot.polling(none_stop=True)
