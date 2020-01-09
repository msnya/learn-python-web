from flask import current_app # Позволяет обращаться к текущему Фласк приложению
import requests


def weather_by_city(city_name):
    weather_url = current_app.config["WEATHER_URL"] # Берем ссылку из конфига
    params = {
        "key":current_app.config['WEARTHER_API_KEY'], # Берем ключ из конфига
        "q":city_name,
        "format":"json",
        "num_of_days":"1",
        "lang":"ru"
    }
    try: # С помощью этой хуйни отлавливаем исключение на случай если запрос не пройдет
        result = requests.get(weather_url, params=params) # Сам запрос к серверу погоды
        result.raise_for_status()
        weather = result.json()
        if "data" in weather:
            if "current_condition" in weather['data']:
                try:
                    return weather['data']["current_condition"][0]
                except(IndexError, TypeError):
                    return False
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False
    return False # Если наши Ифы не сработали - восвращаем Фолс
if __name__ == "__main__": # Если наш блок вызвали напрямую
    w = weather_by_city("Moscoe, Russia")
    print(w)