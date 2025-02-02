from flask import Flask, jsonify,request
import psycopg2
from psycopg2.extras import RealDictCursor
import json

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

@app.route('/api/dogwalks', methods=['GET'])
def read_dogwalks_table():
    """
    Endpoint to fetch all rows from the dogwalks table.
    """
    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        
        # Query the database table
        query = """
            SELECT 
                id, 
                title, 
                ST_AsText(geometry) AS geometry, 
                location, 
                city, 
                comment, 
                encode(image, 'base64') AS image 
            FROM dogwalks;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Return the data as JSON
        # Use ensure_ascii=False to properly display Unicode characters
        return app.response_class(
            response=json.dumps(rows, ensure_ascii=False),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            cursor.close()
            connection.close()

@app.route('/api/dogwalks/<int:id>', methods=['GET'])
def get_dogwalk_by_id(id):
    """
    Endpoint to fetch all rows from a PostgreSQL table.
    """
    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        
        # Query the table for the row with the specified ID
        query = "SELECT id, title, location, city, image, comment, st_astext(geometry) AS geometry FROM dogwalks WHERE id = %s;"

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


@app.route('/api/dogwalks', methods=['POST'])
def insert_dogwalks_data():
    """
    Endpoint to insert data into a PostgreSQL table.
    """
    data = request.get_json()  # Get JSON payload from the client
    
    # Validate input data
    required_fields = ('title', 'geometry', 'location', 'city')
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Invalid input. Must include 'title', 'geometry', 'location', 'city'"}), 400
    
    try:
        # Extract values from the JSON payload
        title = data['title']
        geometry = data['geometry']
        location = data['location']
        city = data['city']

                # Handle optional fields
        comment = data.get('comment', None)  # Use None if not provided
        image = data.get('image', None)      # Use None if not provided

        
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Insert data into the table
        insert_query = """
            INSERT INTO dogwalks (title, geometry, location, city, comment, image)
            VALUES (%s, ST_GeomFromText(%s, 4326), %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (title, geometry, location, city, comment, image))
        connection.commit()  # Commit the transaction
        
        return jsonify({"message": "Data inserted successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            cursor.close()
            connection.close()

@app.route('/api/dogwalks/<int:id>', methods=['DELETE'])
def delete_dogwalk(id):
    """
    Endpoint to delete a record from the dogwalks table by id.
    """
    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        # Execute the DELETE query
        delete_query = "DELETE FROM dogwalks WHERE id = %s RETURNING id;"
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

@app.route('/api/dogwalks/<int:id>', methods=['PUT'])
def update_dogwalks(id):
    """
    Endpoint to update an existing record in the dogwalk table.
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
        if 'title' in data:
            update_fields.append("title = %s")
            parameters.append(data['title'])
        if 'geometry' in data:
            update_fields.append("geometry = ST_GeomFromText(%s, 4326)")
            parameters.append(data['geometry'])
        if 'location' in data:
            update_fields.append("location = %s")
            parameters.append(data['location'])
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
            UPDATE dogwalks
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