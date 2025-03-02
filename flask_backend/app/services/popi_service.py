from flask import jsonify
import json
from psycopg2.extras import RealDictCursor
from app.db import get_db_connection

def get_all_points():
    """
    Retrieve all pet points of interest and return them in GeoJSON format.
    """
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT id, name, category, address, city, comment, ST_AsGeoJSON(geometry) AS geometry
                FROM petspointofinterest
                WHERE geometry IS NOT NULL;
            """)
            points = cursor.fetchall()

            # Convert results to GeoJSON format
            features = []
            for point in points:
                try:
                    geometry = json.loads(point["geometry"])  # Convert string to JSON object
                    features.append({
                        "type": "Feature",
                        "properties": {
                            "id": point["id"],
                            "name": point["name"],
                            "category": point["category"],
                            "address": point["address"],
                            "city": point["city"],
                            "comment": point["comment"]
                        },
                        "geometry": geometry
                    })
                except Exception as geo_error:
                    print(f"Error parsing geometry for point ID {point['id']}: {geo_error}")

            return jsonify({
                "type": "FeatureCollection",
                "features": features
            }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

# def get_point_by_id(id):
#     """
#     Retrieve a specific pet point of interest by ID.
#     """
#     try:
#         connection = get_db_connection()
#         cursor = connection.cursor(cursor_factory=RealDictCursor)
        
#         query = """
#             SELECT id, name, category, city, address, image, comment, 
#                    ST_AsGeoJSON(geometry) AS geometry
#             FROM petspointofinterest 
#             WHERE id = %s;
#         """
#         cursor.execute(query, (id,))
#         row = cursor.fetchone()

#         if row:
#             return jsonify(row), 200
#         else:
#             return jsonify({"error": f"Object with ID {id} not found"}), 404
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#     finally:
#         if connection:
#             cursor.close()
#             connection.close()

def get_point_by_id(id):
    """
    Retrieve a specific pet point of interest by ID.
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        
        query = """
            SELECT id, name AS title, category, city, address AS location, 
                   image, comment, ST_AsText(geometry) AS geometry
            FROM petspointofinterest 
            WHERE id = %s;
        """
        cursor.execute(query, (id,))
        row = cursor.fetchone()

        if row:
            return jsonify(row), 200
        else:
            return jsonify({"error": f"Object with ID {id} not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            cursor.close()
            connection.close()


def insert_point_data(data):
    """
    Insert a new pet point of interest into the database.
    """
    required_fields = ('name', 'category', 'geometry', 'address', 'city')
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Invalid input. Must include 'name', 'category', 'geometry', 'address', 'city'"}), 400

    try:
        name = data['name']
        category = data['category']
        geometry = data['geometry']
        address = data['address']
        city = data['city']
        comment = data.get('comment', None)
        image = data.get('image', None)

        connection = get_db_connection()
        cursor = connection.cursor()
        
        insert_query = """
            INSERT INTO petspointofinterest (name, category, geometry, address, city, comment, image)
            VALUES (%s, %s, ST_GeomFromText(%s, 4326), %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (name, category, geometry, address, city, comment, image))
        connection.commit()

        return jsonify({"message": "Data inserted successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            cursor.close()
            connection.close()

def update_petpointofinterest(id, data):
    """
    Update an existing pet point of interest record.
    """
    if not data:
        return jsonify({"error": "Invalid input. JSON payload is required."}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        update_fields = []
        parameters = []

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

        if not update_fields:
            return jsonify({"error": "No fields provided for update."}), 400

        parameters.append(id)

        update_query = f"""
            UPDATE petspointofinterest
            SET {', '.join(update_fields)}
            WHERE id = %s
            RETURNING id;
        """

        cursor.execute(update_query, tuple(parameters))
        updated_id = cursor.fetchone()

        connection.commit()

        if not updated_id:
            return jsonify({"error": f"No record found with ID {id}"}), 404

        return jsonify({"message": f"Record with ID {id} updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            cursor.close()
            connection.close()

def delete_petpointofinterest(id):
    """
    Delete a pet point of interest record by ID.
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        delete_query = "DELETE FROM petspointofinterest WHERE id = %s RETURNING id;"
        cursor.execute(delete_query, (id,))
        deleted_id = cursor.fetchone()

        connection.commit()

        if deleted_id:
            return jsonify({"message": f"Record with ID {id} deleted successfully!"}), 200
        else:
            return jsonify({"error": f"No record found with ID {id}"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            cursor.close()
            connection.close()
