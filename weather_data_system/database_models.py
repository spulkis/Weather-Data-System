from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, Float, DateTime

Base = declarative_base()

class WeatherData(Base):
    """
    Represents the weather data table in the database.

    Attributes:
        index (int): Primary key for the weather data table.
        city_id (int): Unique identifier for the city.
        city_name (str): Name of the city.
        country (str): Country where the city is located.
        lon_coordinate (float): Longitude coordinate of the city.
        lat_coordinate (float): Latitude coordinate of the city.
        timestamp (DateTime): Represents the time of the data collection.
        weather_type (str): General weather condition (e.g., "Clear", "Cloudy", "Rain").
        weather_description (str): Detailed weather description (e.g., "scattered clouds").
        temperature (float): Current temperature in Celsius.
        feels_like (float): Perceived temperature in Celsius.
        temperature_min (float): Minimum temperature for the day in Celsius.
        temperature_max (float): Maximum temperature for the day in Celsius.
        pressure (float): Atmospheric pressure in hPa.
        humidity (float): Relative humidity in percentage.
        visibility (float): Visibility in meters.
        wind_speed (float): Wind speed in meters per second.
        wind_deg (float): Wind direction in degrees (0-360).
        rain_1h (float): Rain volume for the last 1 hour, mm.
    """
    __tablename__ = "weather_data"

    index = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    city_id = Column(Integer, index=True)
    city_name = Column(String(128))
    country = Column(String(64))
    lon_coordinate = Column(Float)
    lat_coordinate = Column(Float)
    timestamp = Column(DateTime)
    weather_type = Column(String(128))
    weather_description = Column(String(128))
    temperature = Column(Float)
    feels_like = Column(Float)
    temperature_min = Column(Float)
    temperature_max = Column(Float)
    pressure = Column(Float)
    humidity = Column(Float)
    visibility = Column(Float)
    wind_speed = Column(Float)
    wind_deg = Column(Float)
    rain_1h = Column(Float)

    def __init__(self, city_id, city_name, country, lon_coordinate, lat_coordinate, timestamp, weather_type, weather_description, temperature, feels_like, temperature_min, temperature_max, pressure, humidity, visibility, wind_speed, wind_deg, rain_1h):
        """
        Initializes a WeatherData instance.

        Args:
            city_id (int): Unique identifier for the city.
            city_name (str): Name of the city.
            country (str): Country where the city is located.
            lon_coordinate (float): Longitude coordinate of the city.
            lat_coordinate (float): Latitude coordinate of the city.
            timestamp (DateTime): Represents the time of the data collection.
            weather_type (str): General weather condition (e.g., "Clear", "Cloudy", "Rain").
            weather_description (str): Detailed weather description (e.g., "scattered clouds").
            temperature (float): Current temperature in Celsius.
            feels_like (float): Perceived temperature in Celsius.
            temperature_min (float): Minimum temperature for the day in Celsius.
            temperature_max (float): Maximum temperature for the day in Celsius.
            pressure (float): Atmospheric pressure in hPa.
            humidity (float): Relative humidity in percentage.
            visibility (float): Visibility in meters.
            wind_speed (float): Wind speed in meters per second.
            wind_deg (float): Wind direction in degrees (0-360).
            rain_1h (float): Rain volume for the last 1 hour, mm.
        """
        self.city_id = city_id
        self.city_name = city_name
        self.country = country
        self.lon_coordinate = lon_coordinate
        self.lat_coordinate = lat_coordinate
        self.timestamp = timestamp
        self.weather_type = weather_type
        self.weather_description = weather_description
        self.temperature = temperature
        self.feels_like = feels_like
        self.temperature_min = temperature_min
        self.temperature_max = temperature_max
        self.pressure = pressure
        self.humidity = humidity
        self.visibility = visibility
        self.wind_speed = wind_speed
        self.wind_deg = wind_deg
        self.rain_1h = rain_1h

    def __repr__(self):
        """
        Provides a string representation of the WeatherData instance.

        Returns:
            str: String representation of the WeatherData instance.
        """
        return (
            f"<WeatherData(city_id={self.city_id}, city_name={self.city_name}, country={self.country}, "
            f"lon_coordinate={self.lon_coordinate}, lat_coordinate={self.lat_coordinate}, timestamp={self.timestamp}, "
            f"weather_type={self.weather_type}, weather_description={self.weather_description}, "
            f"temperature={self.temperature}, feels_like={self.feels_like}, temperature_min={self.temperature_min}, "
            f"temperature_max={self.temperature_max}, pressure={self.pressure}, humidity={self.humidity}, "
            f"visibility={self.visibility}, wind_speed={self.wind_speed}, wind_deg={self.wind_deg}, rain_1h={self.rain_1h})>"
        )