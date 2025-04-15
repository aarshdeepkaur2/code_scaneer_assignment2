import os
import re
import smtplib
import pymysql
import requests
from email.mime.text import MIMEText
from urllib.parse import urlparse

# Secure DB config using environment variables
db_config = {
    "host": os.getenv("DB_HOST", "mydatabase.com"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "secret123"),
}

def get_user_input():
    user_input = input("Enter your name: ")
    if not re.match(r"^[a-zA-Z0-9 ]+$", user_input):
        raise ValueError("Input is invalid! Only alphanumeric characters and spaces are allowed.")
    return user_input

def send_email(to, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "email@example.com"
    msg["To"] = to

    try:
        with smtplib.SMTP("localhost") as server:
            server.sendmail("email@example.com", [to], msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")

def get_data():
    url = "https://secure-api.com/get-data"
    parsed_url = urlparse(url)

    if parsed_url.scheme != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    try:
        response = requests.get(url, headers={"User-Agent": "SecureClient/1.0"}, timeout=5)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def save_to_db(data):
    query = "INSERT INTO mytable (column1, column2) VALUES (%s, %s)"
    connection = None

    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            cursor.execute(query, (data, "Another Value"))
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
    finally:
        if connection and connection.open:
            connection.close()

def main():
    try:
        user_input = get_user_input()
        data = get_data()
        if data:
            save_to_db(data)
        send_email("admin@example.com", "User Input", user_input)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
