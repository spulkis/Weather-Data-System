import aiohttp
import asyncio
import logging
import time
from decouple import config
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine
from async_functions import get_weather_info, insert_weather_data
from database_utils import initialize_database, create_tables, create_views
from pathlib import Path

async def main():
    """
    The main entry point for the weather data collection and storage program.

    This function performs the following tasks:
    1. Sets up logging.
    2. Loads environment variables.
    3. Creates synchronous and asynchronous database engines.
    4. Initializes the database and creates tables and views.
    5. Reads the list of cities and countries from a file.
    6. Fetches weather data asynchronously for each city using the OpenWeatherMap API.
    7. Inserts the collected weather data into the database.

    Raises:
        IOError: If there is an issue reading the cities file specified by CITIES_FILE_PATH.
        Exception: Any exception raised during weather data insertion or the main program execution.
    """
    LOGS_FILE_PATH = config('LOGS_FILE_PATH')
    # Set up logging
    logging.basicConfig(
        filename=LOGS_FILE_PATH,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.info("Starting program.")

    # Load environment variables
    CONNECTION_STRING = config('CONNECTION_STRING')
    CONNECTION_STRING_ASYNC = config('CONNECTION_STRING_ASYNC')
    API_KEY = config('API_KEY')
    CITIES_FILE_PATH = config('CITIES_FILE_PATH')
    logging.info("Loaded environment variables.")

    # Create engines
    engine = create_engine(CONNECTION_STRING)
    async_engine = create_async_engine(CONNECTION_STRING_ASYNC, echo=True)
    logging.info("Created database engines.")

    # Create database synchronously and tables asynchronously
    initialize_database(engine)
    await create_tables(async_engine)
    await create_views(async_engine)

    # Read cities from the file
    city_country_pairs = []
    cities_file_path = Path(CITIES_FILE_PATH)
    
    try:
        with open(cities_file_path, 'r') as cities_file:
            for line in cities_file:
                city, country = map(str.strip, line.split(',', 1))
                city_country_pairs.append((city, country))
        logging.info("Cities file has been read.")
    except IOError as e:
        logging.error(f"File I/O error: {e}")
        return

    # Fetch and insert weather data
    async with aiohttp.ClientSession() as session:
        tasks = []
        for city, country in city_country_pairs:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={API_KEY}&units=metric"
            logging.info(f"Fetching weather data for {city}, {country}.")
            tasks.append(get_weather_info(session, url))

        try:
            weather_responses = await asyncio.gather(*tasks)
            logging.info("Successfully fetched weather data for all cities.")
        except Exception as e:
            logging.error(f"Error occurred while fetching weather data: {e}")
            raise

        # Insert weather data into the database asynchronously
        async with AsyncSession(bind=async_engine) as db_session:
            try:
                for weather in weather_responses:
                    await insert_weather_data(weather, db_session)
            except Exception as e:
                await db_session.rollback()
                logging.error(f"Error during weather data insertion: {e}")
            finally:
                await db_session.close()

    await async_engine.dispose()
    engine.dispose()
    logging.info("Program completed successfully.")

if __name__ == "__main__":
    start_time = time.time()
    try:
        asyncio.run(main())
        print(f"--- {time.time() - start_time} seconds ---")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        logging.shutdown()
