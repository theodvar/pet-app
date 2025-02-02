from flask import Flask, jsonify, request, abort
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Database connection details
DB_CONFIG = {
    "host": "127.0.0.1",
    "database": "pets_db",
    "user": "postgres",
    "password": "postgres",
    "port": 5432,  # Default PostgreSQL port
}

def get_db_connection():
    """
    Create a connection to the PostgreSQL database.
    """
    return psycopg2.connect(
        host=DB_CONFIG["host"],
        database=DB_CONFIG["database"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        port=DB_CONFIG["port"],
    )

db = get_db_connection()