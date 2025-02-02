from flask import Flask, jsonify,request
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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

# @app.route('/api/petpointofinterest', methods=['GET'])
# def read_table():
#     """
#     Endpoint to fetch all rows from a PostgreSQL table.
#     """
#     try:
#         # Establish database connection
#         connection = get_db_connection()
#         cursor = connection.cursor(cursor_factory=RealDictCursor)
        
#         # Query the database table
#         cursor.execute("select id, ""name"", ""category"", st_astext(geometry) as geometry from petspointofinterest;")
#         rows = cursor.fetchall()
        
#         # Return the data as JSON
#         return jsonify(rows), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#     finally:
#         if connection:
#             cursor.close()
#             connection.close()
@app.route('/api/petpointofinterest', methods=['GET'])
def get_all_points():
    conn = None
    try:
        # Connect to the database
        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Query the database (exclude NULL geometries)
            cursor.execute("""
                SELECT id, name, category, ST_AsGeoJSON(geometry) AS geometry
                FROM petspointofinterest
                WHERE geometry IS NOT NULL;
            """)
            points = cursor.fetchall()

            # Build the GeoJSON FeatureCollection
            features = []
            for point in points:
                try:
                    # Parse geometry as JSON
                    geometry = json.loads(point["geometry"])
                    features.append({
                        "type": "Feature",
                        "properties": {
                            "id": point["id"],
                            "name": point["name"],
                            "category": point["category"]
                        },
                        "geometry": geometry
                    })
                except Exception as geo_error:
                    # Log or handle invalid geometry
                    print(f"Error parsing geometry for point ID {point['id']}: {geo_error}")
            
            return jsonify({
                "type": "FeatureCollection",
                "features": features
            }), 200
    except Exception as e:
        # Return a JSON error response with details
        return jsonify({"error": str(e)}), 500
    finally:
        # Ensure the database connection is closed
        if conn:
            conn.close()


@app.route('/api/petpointofinterest/<int:id>', methods=['GET'])
def get_object_by_id(id):
    """
    Endpoint to fetch all rows from a PostgreSQL table.
    """
    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        
        # Query the table for the row with the specified ID
        query = "SELECT id, name, category, city, address, image, comment, st_astext(geometry) AS geometry FROM petspointofinterest WHERE id = %s;"
        #query = "SELECT id, name, category, city, address, image, comment, ST_AsGeoJSON(geometry) AS geometry FROM petspointofinterest WHERE id = %s;"
        cursor.execute(query, (id,))
        row = cursor.fetchone()

        # Check if the object was found
        if row:
            # Use ensure_ascii=False to properly display Unicode characters
            return app.response_class(
                response=json.dumps(row, ensure_ascii=False),
                status=200,
                mimetype='application/json'
            )
        else:
            return jsonify({"error": f"Object with ID {id} not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            cursor.close()
            connection.close()
   

@app.route('/api/petpointofinterest', methods=['POST'])
def insert_table_data():
    """
    Endpoint to insert data into a PostgreSQL table.
    """
    data = request.get_json()  # Get JSON payload from the client
    
    # Validate input data
    required_fields = ('name', 'category', 'geometry', 'address', 'city')
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Invalid input. Must include 'name', 'category', 'geometry', 'address', 'city'"}), 400
    
    try:
        # Extract values from the JSON payload
        name = data['name']
        category = data['category']
        geometry = data['geometry']
        address = data['address']
        city = data['city']

                # Handle optional fields
        comment = data.get('comment', None)  # Use None if not provided
        image = data.get('image', None)      # Use None if not provided

        
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Insert data into the table
        insert_query = """
            INSERT INTO petspointofinterest (name, category, geometry, address, city, comment, image)
            VALUES (%s, %s, ST_Transform(ST_GeomFromText(%s, 3857), 4326), %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (name, category, geometry, address, city, comment, image))
        connection.commit()  # Commit the transaction
        
        return jsonify({"message": "Data inserted successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            cursor.close()
            connection.close()

@app.route('/api/petpointofinterest/<int:id>', methods=['DELETE'])
def delete_petpointofinterest(id):
    """
    Endpoint to delete a record from the petspointofinterest table by id.
    """
    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        # Execute the DELETE query
        delete_query = "DELETE FROM petspointofinterest WHERE id = %s RETURNING id;"
        cursor.execute(delete_query, (id,))
        deleted_id = cursor.fetchone()  # Fetch the id of the deleted record

        # Commit the transaction
        connection.commit()

        if deleted_id:
            return jsonify({"message": f"Record with id {id} deleted successfully!"}), 200
        else:
            return jsonify({"error": f"No record found with id {id}"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            cursor.close()
            connection.close()

@app.route('/api/petpointofinterest/<int:id>', methods=['PUT'])
def update_petpointofinterest(id):
    """
    Endpoint to update an existing record in the petspointofinterest table.
    """
    data = request.get_json()

    # Validate input data
    if not data:
        return jsonify({"error": "Invalid input. JSON payload is required."}), 400

    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        # Prepare the update query dynamically based on provided fields
        update_fields = []
        parameters = []

        # Check for fields to update
        if 'name' in data:
            update_fields.append("name = %s")
            parameters.append(data['name'])
        if 'category' in data:
            update_fields.append("category = %s")
            parameters.append(data['category'])
        if 'geometry' in data:
            update_fields.append("geometry = ST_GeomFromText(%s, 4326)")
            parameters.append(data['geometry'])
        if 'address' in data:
            update_fields.append("address = %s")
            parameters.append(data['address'])
        if 'city' in data:
            update_fields.append("city = %s")
            parameters.append(data['city'])
        if 'comment' in data:
            update_fields.append("comment = %s")
            parameters.append(data['comment'])
        if 'image' in data:
            update_fields.append("image = %s")
            parameters.append(data['image'])

        # If no fields are provided for update, return an error
        if not update_fields:
            return jsonify({"error": "No fields provided for update."}), 400

        # Add id to parameters for the WHERE clause
        parameters.append(id)

        # Construct the full query
        update_query = f"""
            UPDATE petspointofinterest
            SET {', '.join(update_fields)}
            WHERE id = %s
            RETURNING id;
        """

        # Execute the query
        cursor.execute(update_query, tuple(parameters))
        updated_id = cursor.fetchone()

        # Commit the transaction
        connection.commit()

        # If no rows were updated, return a 404 error
        if not updated_id:
            return jsonify({"error": f"No record found with id {id}"}), 404

        return jsonify({"message": f"Record with id {id} updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            cursor.close()
            connection.close()




if __name__ == '__main__':
    app.run(debug=True)     