import sqlite3
import functools
from datetime import datetime


def log_queries():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Extract the query from kwargs or args
            query = kwargs.get("query") or (args[0] if args else None)
            if query:
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{now}] Executing SQL query: {query}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


@log_queries()
def fetch_all_users(query):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Example usage
users = fetch_all_users(query="SELECT * FROM users")
