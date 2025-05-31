import mysql.connector


def stream_users_in_batches(batch_size):
    """Generator to fetch rows in batches from user_data."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_username",  # change this
            password="your_password",  # change this
            database="ALX_prodev",
        )
        cursor = connection.cursor(dictionary=True)

        offset = 0
        while True:
            cursor.execute(
                "SELECT * FROM user_data LIMIT %s OFFSET %s", (batch_size, offset)
            )
            batch = cursor.fetchall()
            if not batch:
                break
            yield batch
            offset += batch_size

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def batch_processing(batch_size):
    """Generator to process batches and yield users older than 25."""
    for batch in stream_users_in_batches(batch_size):  # loop 1
        for user in batch:  # loop 2
            if user["age"] > 25:
                yield user  # yield matching users
