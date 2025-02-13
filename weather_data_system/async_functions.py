import logging
from database_models import WeatherData
from datetime import datetime, timezone

async def get_weather_info(session, url):
    """
    Fetches weather information from the given URL asynchronously.

    Args:
        session (aiohttp.ClientSession): The aiohttp client session used to make the request.
        url (str): The URL to fetch weather data from.

    Returns:
        dict: The JSON response from the API containing weather data.
    """
    async with session.get(url) as response:
        return await response.json()

def extract_weather_data(api_response):
    """
    Extracts relevant weather data from the API response and converts it into a WeatherData object.

    Args:
        api_response (dict): The JSON response from the weather API.

    Returns:
        WeatherData: An instance of the WeatherData model containing extracted weather information.
    """
    coord = api_response["coord"]
    weather = api_response["weather"][0]
    main = api_response["main"]
    wind = api_response["wind"]
    rain = api_response.get("rain", {})
    sys = api_response["sys"]

    timestamp_utc = datetime.fromtimestamp(api_response["dt"], timezone.utc)

    return WeatherData(
        city_id=api_response["id"],
        city_name=api_response["name"],
        country=sys["country"],
        lon_coordinate=coord["lon"],
        lat_coordinate=coord["lat"],
        timestamp=timestamp_utc,
        weather_type=weather["main"],
        weather_description=weather["description"],
        temperature=main["temp"],
        feels_like=main["feels_like"],
        temperature_min=main["temp_min"],
        temperature_max=main["temp_max"],
        pressure=main["pressure"],
        humidity=main["humidity"],
        visibility=api_response.get("visibility", None),
        wind_speed=wind["speed"],
        wind_deg=wind["deg"],
        rain_1h=rain.get("1h", None)
    )

async def insert_weather_data(api_response, session):
    """
    Inserts weather data into the database asynchronously.

    Args:
        api_response (dict): The JSON response from the weather API.
        session (AsyncSession): The SQLAlchemy asynchronous session used for database operations.

    Logs:
        A success message if data is inserted correctly.
        An error message if insertion fails.
    """
    try:
        weather_data = extract_weather_data(api_response)
        session.add(weather_data)
        await session.commit()
        logging.info("Weather data inserted successfully!")
    except Exception as e:
        await session.rollback()
        logging.error(f"Error inserting weather data: {e}")
