import requests

api_key = "1db7fb7e0f7db72159ed68f0f76fa28d"
url = "https://api.openweathermap.org/data/2.5/forecast?q=madrid&appid=1db7fb7e0f7db72159ed68f0f76fa28d"

class Weather:
    """
    Creates a weather object getting an apikey as input
    and either a city name or lat and lon coordinates.
    """
    def __init__(self, apikey, city=None, lat=None, lon=None):
        if city:
            url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={apikey}&units=celcius"
            r = requests.get(url)
            self.data = r.json()
        elif lat and lon:
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=celcius"
            r = requests.get(url)
            self.data = r.json()
        else:
            raise TypeError("Provide either a city or lat&lon information")

        if self.data["cod"] != "200":
            raise ValueError(self.data["message"])

    def next_12h(self):
        return self.data["list"][:4]

    def next_12h_simplified(self):
        simple_data = []
        for dicty in self.data["list"][:4]:
            simple_data.append((dicty["dt_txt"],dicty["main"]["temp"],dicty["weather"][0]["description"],dicty["weather"][0]["icon"]))
        return simple_data