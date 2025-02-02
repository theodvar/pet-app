from flask import Flask, jsonify,request
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

@app.route('/api/table-data', methods=['GET'])
def read_table():
    """
    Endpoint to fetch all rows from a PostgreSQL table.
    """
    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        
        # Query the database table
        cursor.execute("select id, ""name"", st_astext(geom) as geometries from mygeometries;")
        rows = cursor.fetchall()
        
        # Return the data as JSON
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            cursor.close()
            connection.close()

@app.route('/api/table-data', methods=['POST'])
def insert_table_data():
    """
    Endpoint to insert data into a PostgreSQL table.
    """
    data = request.get_json()  # Get JSON payload from the client
    
    # Validate input data
    if not data or not all(key in data for key in ('name', 'geometries')):
        return jsonify({"error": "Invalid input, must include 'name' and 'geometries'"}), 400
    
    try:
        # Extract values from the JSON payload
        column1_value = data['name']
        column2_value = data['geometries']
        
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Insert data into the table
        insert_query = """
            INSERT INTO mygeometries (name, geom)
            VALUES (%s, ST_GeomFromText(%s, 4326));
        """
        cursor.execute(insert_query, (column1_value, column2_value))
        connection.commit()  # Commit the transaction
        
        return jsonify({"message": "Data inserted successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)
