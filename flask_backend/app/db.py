import psycopg2
from psycopg2.extras import RealDictCursor
from flask import current_app

def get_db_connection():
    """
    Establish a database connection.
    """
    return psycopg2.connect(
        host=current_app.config["DB_HOST"],
        database=current_app.config["DB_NAME"],
        user=current_app.config["DB_USER"],
        password=current_app.config["DB_PASSWORD"],
        port=current_app.config["DB_PORT"],
    )
