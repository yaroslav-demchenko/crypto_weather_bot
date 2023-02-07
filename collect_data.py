import requests


def get_weather(city: str) -> list:
    req = requests.get(
        f"http://api.weatherapi.com/v1/"
        f"forecast.json?key=ca312dd06431499080e93311220912 "
        f"&q={city}&days=1&aqi=no&alerts=no"
    )
    response = req.json()
    data = response["forecast"]["forecastday"][0]

    def is_windy(wind_speed: int) -> str:
        if wind_speed == 0:
            return f"Full calm, {wind_speed} m/h"
        elif wind_speed <= 4:
            return f"Breeze, {wind_speed} m/h"
        elif 4 < wind_speed <= 10:
            return f"Moderate wind, {wind_speed} m/h"
        else:
            return f"Strong wind, {wind_speed} m/h"

    today = data["date"]
    maxtemp = data["day"]["maxtemp_c"]
    mintemp = data["day"]["mintemp_c"]
    wind = is_windy(data["day"]["maxwind_mph"])
    condition = data["day"]["condition"]["text"]
    return [today, maxtemp, mintemp, wind, condition]


def get_crypto_price(currency_pair: str):
    currencyes = currency_pair.upper().split("_")
    currency_pair = currency_pair.upper().replace("_", "")
    req = requests.get(
        f"https://api.binance.com/api/v3/ticker/price?symbol={currency_pair}"
    )
    response = req.json()
    price = response["price"]
    return f"Sell {currencyes[0]} prise: {price} {currencyes[1]}"


if __name__ == "__main__":
    print(get_crypto_price("bnb_usdt"))
