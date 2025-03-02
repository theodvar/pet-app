from flask import jsonify
import json
from psycopg2.extras import RealDictCursor
from app.db import get_db_connection

def get_all_dogparks():
    """
    Retrieve all dog parks from the database.
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT id, title, ST_AsGeoJSON(geometry) AS geometry, location, city, comment FROM dogparks WHERE geometry IS NOT NULL;")
        rows = cursor.fetchall()

        # Convert results to GeoJSON format
        features = []
        for polygon in rows:
            try:
                geometry = json.loads(polygon["geometry"])  # Convert string to JSON object
                features.append({
                        "type": "Feature",
                        "properties": {
                            "id": polygon["id"],
                            "title": polygon["title"],
                            "location": polygon["location"],
                            "city": polygon["city"],
                            "comment": polygon["comment"]
                        },
                        "geometry": geometry
                    })
                    
            except Exception as geo_error:
                print(f"Error parsing geometry for polygon ID {polygon['id']}: {geo_error}")
        return jsonify({
            "type": "FeatureCollection",
            "features": features
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            cursor.close()
            connection.close()

def get_dogpark_by_id(id):
    """
    Retrieve a specific dog park by ID.
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        
        query = "SELECT id, title, location, city, image, comment, ST_AsText(geometry) AS geometry FROM dogparks WHERE id = %s;"
        cursor.execute(query, (id,))
        row = cursor.fetchone()

        if row:
            return jsonify(row), 200
        else:
            return jsonify({"error": f"Dog park with ID {id} not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            cursor.close()
            connection.close()

def create_dogpark(data):
    """
    Insert a new dog park into the database.
    """
    required_fields = ('title', 'geometry', 'location', 'city')
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Invalid input. Must include 'title', 'geometry', 'location', 'city'"}), 400

    try:
        title = data['title']
        geometry = data['geometry']
        location = data['location']
        city = data['city']
        comment = data.get('comment', None)
        image = data.get('image', None)

        connection = get_db_connection()
        cursor = connection.cursor()
        
        insert_query = """
            INSERT INTO dogparks (title, geometry, location, city, comment, image)
            VALUES (%s, ST_GeomFromText(%s, 4326), %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (title, geometry, location, city, comment, image))
        connection.commit()

        return jsonify({"message": "Dog park added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            cursor.close()
            connection.close()

def update_dogpark(id, data):
    """
    Update an existing dog park record.
    """
    if not data:
        return jsonify({"error": "Invalid input. JSON payload is required."}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        update_fields = []
        parameters = []

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

        if not update_fields:
            return jsonify({"error": "No fields provided for update."}), 400

        parameters.append(id)

        update_query = f"""
            UPDATE dogparks
            SET {', '.join(update_fields)}
            WHERE id = %s
            RETURNING id;
        """

        cursor.execute(update_query, tuple(parameters))
        updated_id = cursor.fetchone()

        connection.commit()

        if not updated_id:
            return jsonify({"error": f"No dog park found with ID {id}"}), 404

        return jsonify({"message": f"Dog park with ID {id} updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            cursor.close()
            connection.close()

def delete_dogpark(id):
    """
    Delete a dog park record by ID.
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        delete_query = "DELETE FROM dogparks WHERE id = %s RETURNING id;"
        cursor.execute(delete_query, (id,))
        deleted_id = cursor.fetchone()

        connection.commit()

        if deleted_id:
            return jsonify({"message": f"Dog park with ID {id} deleted successfully!"}), 200
        else:
            return jsonify({"error": f"No dog park found with ID {id}"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            cursor.close()
            connection.close()
