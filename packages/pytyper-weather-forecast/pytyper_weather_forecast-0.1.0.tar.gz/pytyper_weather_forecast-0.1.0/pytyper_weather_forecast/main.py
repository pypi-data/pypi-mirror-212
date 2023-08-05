import typer
from geopy.geocoders import Nominatim
from rich.table import Table
from rich.console import Console
from rich import print as rprint
import requests

console = Console()
app = typer.Typer()

API_KEY = 'ae254281bdb5c85813792b8137b3bd2a'

def displayError(value):
        rprint(f"[red]{value}[/red]")

class MyError(Exception):
     
    def __init__(self, value):
        self.value = value


@app.command()
def forecast(city: str):
    try:
        geolocator = Nominatim(user_agent="pytyper")
        location = geolocator.geocode(city)
        if not location or not location.latitude or not location.longitude:
            raise(MyError("Location not found"))
        print(location)
        query = f"https://api.openweathermap.org/data/2.5/weather?lat={location.latitude}&lon={location.longitude}&appid={API_KEY}"
        response = requests.get(query)
        response.raise_for_status()
        res = response.json()
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Weather",min_width=20)
        table.add_column("Longitude",min_width=12,justify="right")
        table.add_column("Latitude",min_width=12,justify="right")
        table.add_column("Temperature (in \N{DEGREE SIGN}C)",min_width=12,justify="right")
        # table.add_column("Visibility",min_width=12,justify="right")
        # table.add_column("Wind Speed",min_width=12,justify="right")
        table.add_row(
                    res["weather"][0]["main"] + " - " + res["weather"][0]["description"],
                    str(res["coord"]["lon"]),
                    str(res["coord"]["lat"]),
                    str(round(res["main"]["temp"]-273.15,2)),
                    # str(res["visibility"]),
                    # str(res["wind"]["speed"])
                )
        console.print(table)
    except MyError as error:
        displayError(error.value)
    except requests.exceptions.HTTPError as error:
        displayError("An Http Error occurred:" + repr(error))
    except requests.exceptions.ConnectionError as error:
        displayError("An Error Connecting to the API occurred:" + repr(error))
    except requests.exceptions.Timeout as error:
        displayError("A Timeout Error occurred:" + repr(error))
    except requests.exceptions.RequestException as error:
        displayError("An Unknown Error occurred" + repr(error))
    
if __name__ == "__main__":
    app()