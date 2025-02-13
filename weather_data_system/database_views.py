import logging
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

async def temperature_differences_today_view(connection: AsyncConnection):
    """
    Creates or replaces a view named `temperature_differences_today` that shows
    the maximum, minimum, and standard deviation of temperatures for each city today.
    """
    sql = text("""
    CREATE OR REPLACE VIEW `temperature_differences_today` AS
    SELECT 
        `weather_data`.`city_name` AS `city_name`,
        `weather_data`.`country` AS `country`,
        MAX(`weather_data`.`temperature`) AS `max_temp`,
        MIN(`weather_data`.`temperature`) AS `min_temp`,
        STD(`weather_data`.`temperature`) AS `stddev_temp`
    FROM
        `weather_data`
    WHERE
        (CAST(`weather_data`.`timestamp` AS DATE) = CURDATE())
    GROUP BY `weather_data`.`city_name` , `weather_data`.`country`
    """)
    await connection.execute(sql)

async def temperature_differences_yesterday_view(connection: AsyncConnection):
    """
    Creates or replaces a view named `temperature_differences_yesterday` that shows
    the maximum, minimum, and standard deviation of temperatures for each city yesterday.
    """
    sql = text("""
    CREATE OR REPLACE VIEW `temperature_differences_yesterday` AS
    SELECT 
        `weather_data`.`city_name` AS `city_name`,
        `weather_data`.`country` AS `country`,
        MAX(`weather_data`.`temperature`) AS `max_temp`,
        MIN(`weather_data`.`temperature`) AS `min_temp`,
        STD(`weather_data`.`temperature`) AS `stddev_temp`
    FROM
        `weather_data`
    WHERE
        (CAST(`weather_data`.`timestamp` AS DATE) = (CURDATE() - INTERVAL 1 DAY))
    GROUP BY `weather_data`.`city_name` , `weather_data`.`country`
    """)
    await connection.execute(sql)

async def temperature_differences_current_week_view(connection: AsyncConnection):
    """
    Creates or replaces a view named `temperature_differences_current_week` that shows
    the maximum, minimum, and standard deviation of temperatures for each city for the current week.
    """
    sql = text("""
    CREATE OR REPLACE VIEW `temperature_differences_current_week` AS
    SELECT 
        `weather_data`.`city_name` AS `city_name`,
        `weather_data`.`country` AS `country`,
        MAX(`weather_data`.`temperature`) AS `max_temp`,
        MIN(`weather_data`.`temperature`) AS `min_temp`,
        STD(`weather_data`.`temperature`) AS `stddev_temp`
    FROM
        `weather_data`
    WHERE
        (YEARWEEK(`weather_data`.`timestamp`, 1) = YEARWEEK(CURDATE(), 1))
    GROUP BY `weather_data`.`city_name` , `weather_data`.`country`
    """)
    await connection.execute(sql)

async def temperature_differences_last_7_days_view(connection: AsyncConnection):
    """
    Creates or replaces a view named `temperature_differences_last_7_days` that shows
    the maximum, minimum, and standard deviation of temperatures for each city over the last 7 days.
    """
    sql = text("""
    CREATE OR REPLACE VIEW `temperature_differences_last_7_days` AS
    SELECT 
        `weather_data`.`city_name` AS `city_name`,
        `weather_data`.`country` AS `country`,
        MAX(`weather_data`.`temperature`) AS `max_temp`,
        MIN(`weather_data`.`temperature`) AS `min_temp`,
        STD(`weather_data`.`temperature`) AS `stddev_temp`
    FROM
        `weather_data`
    WHERE
        (`weather_data`.`timestamp` >= (CURDATE() - INTERVAL 7 DAY))
    GROUP BY `weather_data`.`city_name` , `weather_data`.`country`
    """)
    await connection.execute(sql)

async def temperature_comparison_view(connection: AsyncConnection):
    """
    Creates or replaces a view named `temperature_comparison` that combines temperature 
    statistics (max, min, and standard deviation) for today, yesterday, the current week,
    and the last 7 days for each city.
    """
    sql = text("""
    CREATE OR REPLACE VIEW `temperature_comparison` AS
    SELECT 
        `weather_data`.`city_name` AS `city_name`,
        `weather_data`.`country` AS `country`,
        MAX(`weather_data`.`temperature`) AS `max_temperature`,
        MIN(`weather_data`.`temperature`) AS `min_temperature`,
        STD(`weather_data`.`temperature`) AS `temperature_stddev`,
        'today' AS `period`
    FROM
        `weather_data`
    WHERE
        (CAST(`weather_data`.`timestamp` AS DATE) = CURDATE())
    GROUP BY 
        `weather_data`.`city_name`, `weather_data`.`country`
        
    UNION ALL 
    
    SELECT 
        `weather_data`.`city_name` AS `city_name`,
        `weather_data`.`country` AS `country`,
        MAX(`weather_data`.`temperature`) AS `max_temperature`,
        MIN(`weather_data`.`temperature`) AS `min_temperature`,
        STD(`weather_data`.`temperature`) AS `temperature_stddev`,
        'yesterday' AS `period`
    FROM
        `weather_data`
    WHERE
        (CAST(`weather_data`.`timestamp` AS DATE) = (CURDATE() - INTERVAL 1 DAY))
    GROUP BY 
        `weather_data`.`city_name`, `weather_data`.`country`
        
    UNION ALL 
    
    SELECT 
        `weather_data`.`city_name` AS `city_name`,
        `weather_data`.`country` AS `country`,
        MAX(`weather_data`.`temperature`) AS `max_temperature`,
        MIN(`weather_data`.`temperature`) AS `min_temperature`,
        STD(`weather_data`.`temperature`) AS `temperature_stddev`,
        'current_week' AS `period`
    FROM
        `weather_data`
    WHERE
        (YEARWEEK(`weather_data`.`timestamp`, 1) = YEARWEEK(CURDATE(), 1))
    GROUP BY 
        `weather_data`.`city_name`, `weather_data`.`country`
        
    UNION ALL 
    
    SELECT 
        `weather_data`.`city_name` AS `city_name`,
        `weather_data`.`country` AS `country`,
        MAX(`weather_data`.`temperature`) AS `max_temperature`,
        MIN(`weather_data`.`temperature`) AS `min_temperature`,
        STD(`weather_data`.`temperature`) AS `temperature_stddev`,
        'last_7_days' AS `period`
    FROM
        `weather_data`
    WHERE
        (`weather_data`.`timestamp` >= (CURDATE() - INTERVAL 7 DAY))
    GROUP BY 
        `weather_data`.`city_name`, `weather_data`.`country`
    """)
    await connection.execute(sql)

async def highest_temperature_city_last_hour_view(connection: AsyncConnection):
    """
    Creates or replaces a view named `highest_temperature_city_last_hour` that shows
    the city with the highest temperature recorded in the last hour.
    """
    sql = text("""
    CREATE OR REPLACE VIEW `highest_temperature_city_last_hour` AS
    SELECT 
        `weather_data`.`city_name` AS `city_name`,
        `weather_data`.`country` AS `country`,
        MAX(`weather_data`.`temperature`) AS `max_temp`
    FROM
        `weather_data`
    WHERE
        ((`weather_data`.`timestamp` >= (NOW() - INTERVAL 5 HOUR))
            AND (CAST(`weather_data`.`timestamp` AS DATE) = CURDATE()))
    GROUP BY `weather_data`.`city_name` , `weather_data`.`country`
    ORDER BY `max_temp` DESC
    LIMIT 1
    """)
    await connection.execute(sql)

async def highest_temperature_today_view(connection: AsyncConnection):
    """
    Creates or replaces a view named `highest_temperature_city_today` that shows
    the city with the highest temperature recorded today.
    """
    sql = text("""
    CREATE OR REPLACE VIEW `highest_temperature_city_today` AS
    SELECT 
        `weather_data`.`city_name` AS `city_name`,
        `weather_data`.`country` AS `country`,
        MAX(`weather_data`.`temperature`) AS `max_temp`
    FROM
        `weather_data`
    WHERE
        (CAST(`weather_data`.`timestamp` AS DATE) = CURDATE())
    GROUP BY `weather_data`.`city_name` , `weather_data`.`country`
    ORDER BY `max_temp` DESC
    LIMIT 1
    """)
    await connection.execute(sql)

async def highest_temperature_city_last_week_view(connection: AsyncConnection):
    """
    Creates or replaces a view named `highest_temperature_city_last_week` that shows
    the city with the highest temperature recorded during the current week.
    """
    sql = text("""
    CREATE OR REPLACE VIEW `highest_temperature_city_last_week` AS
    SELECT 
        `weather_data`.`city_name` AS `city_name`,
        `weather_data`.`country` AS `country`,
        MAX(`weather_data`.`temperature`) AS `max_temp`
    FROM
        `weather_data`
    WHERE
        (YEARWEEK(`weather_data`.`timestamp`, 1) = YEARWEEK(CURDATE(), 1))
    GROUP BY `weather_data`.`city_name` , `weather_data`.`country`
    ORDER BY `max_temp` DESC
    LIMIT 1
    """)
    await connection.execute(sql)

async def rainy_hours_today_view(connection: AsyncConnection):
    """
    Creates or replaces a view named `rainy_hours_today` that shows
    the total number of rainy hours recorded today.
    """
    sql = text("""
    CREATE OR REPLACE VIEW `rainy_hours_today` AS
    SELECT 
        COUNT(0) AS `rainy_hours`
    FROM
        `weather_data`
    WHERE
        ((CAST(`weather_data`.`timestamp` AS DATE) = (CURDATE() - INTERVAL 1 DAY))
            AND (`weather_data`.`weather_type` = 'Rain'))
    """)
    await connection.execute(sql)

async def rainy_hours_last_week_view(connection: AsyncConnection):
    """
    Creates or replaces a view named `rainy_hours_last_week` that shows
    the total number of rainy hours recorded over the last 7 days.
    """
    sql = text("""
    CREATE OR REPLACE VIEW `rainy_hours_last_week` AS
    SELECT 
        COUNT(0) AS `rainy_hours`
    FROM
        `weather_data`
    WHERE
        ((`weather_data`.`timestamp` >= (CURDATE() - INTERVAL 7 DAY))
            AND (`weather_data`.`weather_type` = 'Rain'))
    """)
    await connection.execute(sql)

async def create_all_views(connection: AsyncConnection):
    """
    Creates all the database views by calling individual view creation functions.

    Args:
        connection (AsyncConnection): The asynchronous database connection.

    Logs:
        An info log is created upon successful creation of all views.
        An error log is generated if an exception occurs while creating views.
    """
    try:
        await temperature_differences_today_view(connection)
        await temperature_differences_yesterday_view(connection)
        await temperature_differences_current_week_view(connection)
        await temperature_differences_last_7_days_view(connection)
        await temperature_comparison_view(connection)
        await highest_temperature_city_last_hour_view(connection)
        await highest_temperature_today_view(connection)
        await highest_temperature_city_last_week_view(connection)
        await rainy_hours_today_view(connection)
        await rainy_hours_last_week_view(connection)
        logging.info("All views created successfully.")
    except Exception as e:
        logging.error(f"An error occurred while creating views: {e}")
