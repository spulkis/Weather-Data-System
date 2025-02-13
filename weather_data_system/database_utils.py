import logging
from sqlalchemy_utils import create_database, database_exists
from database_views import create_all_views
from database_models import Base

def initialize_database(engine):
    """
    Initializes the database by checking if it exists. If not, it creates the database.

    Args:
        engine (Engine): The SQLAlchemy engine used for the database connection.
    """
    if not database_exists(engine.url):
        create_database(engine.url)
        logging.info("Database created.")
    else:
        logging.info("Database already exists.")

async def create_tables(async_engine):
    """
    Asynchronously creates all tables in the database based on the defined schema.

    Args:
        async_engine (AsyncEngine): The SQLAlchemy asynchronous engine used for the database connection.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logging.info("Created database tables based on schema.")

async def create_views(async_engine):
    """
    Asynchronously creates all database views defined in the project.

    Args:
        async_engine (AsyncEngine): The SQLAlchemy asynchronous engine used for the database connection.
    """
    async with async_engine.begin() as conn:
        try:
            await create_all_views(conn)
            logging.info("Created database views.")
        except Exception as e:
            logging.error(f"Error creating views: {e}")
