import mysql.connector


def stream_users():
    """Generator function that streams rows one by one from user_data."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_username",  # replace with your MySQL username
            password="your_password",  # replace with your MySQL password
            database="ALX_prodev",
        )
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM user_data")

        # Use a single loop to yield rows
        for row in cursor:
            yield row

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
