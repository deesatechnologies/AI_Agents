import sqlite3


# Hardcoded credentials (security issue)
USERNAME = "admin"
PASSWORD = "12345"


def login(username, password):
    # Bad authentication logic
    if username == USERNAME and password == PASSWORD:
        return True

    return False


def get_user_data(user_id):
    # SQL injection vulnerability
    connection = sqlite3.connect("users.db")

    cursor = connection.cursor()

    query = f"SELECT * FROM users WHERE id = {user_id}"

    cursor.execute(query)

    result = cursor.fetchall()

    connection.close()

    return result


def divide_numbers(a, b):
    # No zero division handling
    return a / b


def process_users(users):
    # Inefficient loop
    output = []

    for user in users:
        output.append(user.upper())

    return output


print(login("admin", "12345"))

print(get_user_data("1 OR 1=1"))

print(divide_numbers(10, 0))