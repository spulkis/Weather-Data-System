[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org)

## Weather Data System

This project aims to create a system that queries the [OpenWeatherMap API](https://openweathermap.org/current) at specified time intervals and stores the results in a MySQL RDBMS. The Python code utilizes `asyncio` coroutines to fetch weather data for 20 different cities concurrently. For scheduling tasks, `crontab` is used in an exemplary WSL environment.

### Key Features:

1. **Multi-platform compatibility:** The package was tested in different environments (Windows & WSL). 
Note: `aiomysql` driver had some compatibility issues in WSL, so it was switched to `asyncmy`.

2. **`cities.txt` configuration file:** The list of cities is separated from the main code and stored in a `cities.txt` file, allowing convenient modifications to the list of cities whose data is fetched and stored in the database.

3. **`asyncio` coroutines for concurrency:** The script uses asyncio coroutines for efficient concurrent data fetching, making it faster and more responsive.

4. **Error logging:** The script includes error logging into a separate file, making it easy to access and check for issues.

5. **Crontab scheduling:** The script is ready for scheduling with `crontab` for automated data fetching at specified intervals.

6. **Wide variety of weather parameters from OpenWeatherMap API:** OpenWeatherMap collects and processes weather data from various sources like global and local weather models, satellites, radars, and a vast network of weather stations. A wide variety of different parameters are available. You can check the full list on the [OpenWeatherMap API](https://openweathermap.org/current) website.

7. **SQL Views for additional analytical information:** SQL views are created for additional analysis, and an example analysis is included in the `examples` folder under the `weather_data_system_additional_information.ipynb` file.

8. **MySQL database backup script included:** A MySQL backup script is provided in the `tools` folder and can be included in your `crontab` scheduler for automatic database backups.

### Installation

Follow these steps to initialize and run this Poetry-based project in a new environment.

1. **Clone the Repository:**

    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2. **Install Poetry (Optional):** Ensure that Poetry is installed in your new environment. If not, you can install it using the official installation script:

    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

3. **Install Dependencies (Optional):** Navigate to the project directory and install the dependencies specified in the `pyproject.toml` file using Poetry:

    ```bash
    poetry install
    ```

    This command will create a virtual environment (if it doesn't already exist) and install all the dependencies listed in `pyproject.toml` and `poetry.lock`.

4. **Activate the Virtual Environment (Optional):** Poetry automatically manages virtual environments for you. To activate the virtual environment, you can use:

    ```bash
    poetry shell
    ```

    This will activate the environment, and you can start working within it.

5. **Set up environment variables:** This package uses the `python-decouple` library for managing environment variables. Create a `.env` file or an `.ini` file and include your environment settings. Example:

    ```bash
    CONNECTION_STRING=mysql+pymysql://user:password@localhost/weather_data_system
    CONNECTION_STRING_ASYNC=mysql+aiomysql://user:password@localhost/weather_data_system
    CONNECTION_STRING_WSL=mysql+pymysql://user:password@127.0.0.1/weather_data_system
    CONNECTION_STRING_ASYNC_WSL=mysql+asyncmy://user:password@127.0.0.1/weather_data_system
    CITIES_FILE_PATH=cities.txt
    LOGS_FILE_PATH=folder/data_log.txt 
    BACKUP_DIR=weather_data_system/tools/mysql_backup_files
    API_KEY=xxxkeyxxx
    MYSQL_USER=user
    MYSQL_PASSWORD=password
    MYSQL_HOST=127.0.0.1
    MYSQL_DATABASE=weather_data_system
    ```

    Note: For WSL, ensure that `LOGS_FILE_PATH` and `BACKUP_DIR` are set as absolute paths, as relative paths may not work correctly.

6. **Usage:** Start the data extraction and insertion process by running:

    ```bash
    cd ./weather_data_system
    python main.py
    ```

7. **Scheduling with Crontab:** You can use `crontab` to schedule the script execution at regular intervals. Open `crontab` in your preferred Linux environment (e.g., WSL):

    ```bash
    crontab -e
    ```
    Add entries like these to run the main script every 5 minutes and the backup script every night at 23:00:

    ```
    */5 * * * * /usr/bin/python3 /weather_data_system/main.py >> /home/user_name/cron.log 2>&1
    0 23 * * * /usr/bin/python3 /weather_data_system/tools/mysql_backup.py >> /home/user_name/cron.log 2>&1
    ```

### Suggestions for Future Improvements

- **Error Handling:** Implement more robust error handling to manage potential issues such as invalid input types or API errors, providing clearer feedback.
- **Experiment with Different Concurrent Methods:** Explore various data retrieval methods (e.g., threads and processes) to enhance code performance through different concurrency approaches.
- **Database Health Monitoring:** Implement a monitoring solution that visualizes metrics representing the health of your database, allowing for proactive management and maintenance.
