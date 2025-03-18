import mysql.connector
from mysql.connector import Error

# chatgpt help to connect sql with python
def connect(query,data):
    conn = None
    try:
        # Establish connection to MySQL
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="employee_db"
        )

        # Check if the connection was successful
        if conn.is_connected():
            print("Connection established successfully.")

            # Create a cursor object to interact with the database
            cursor = conn.cursor( buffered=True)

            # Execute a simple query
            cursor.execute(query, data)

            # If it's a SELECT query, fetch and print results
            if query.lower().startswith("select"):
                results = cursor.fetchall()
                # If no results, send admin as username and owner as role
                if not results:
                     return [(None, None, 'admin', None, 'owner')]

                cursor.close()
                return results

            # If it's an INSERT/UPDATE/DELETE query, commit the changes
            else:
                conn.commit()
                cursor.close()
                return True

        else:
            print("Failed to connect to the database.")

    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        # Ensure that the connection is closed
        if conn and conn.is_connected():
            conn.close()
            print("Connection closed.")

