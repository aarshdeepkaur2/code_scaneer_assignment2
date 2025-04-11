import os
import pymysql
import re
import smtplib
from urllib.parse import urlparse
from urllib.request import urlopen, Request
from email.mime.text import MIMEText


# Secure DB config using environment variables
db_config = {
    'host': os.getenv('DB_HOST', 'mydatabase.com'),
    'user': os.getenv('DB_USER', 'admin'),
    'password': os.getenv('DB_PASSWORD', 'secret123')
}


def get_user_input():
    """Prompt the user and validate input to prevent injection."""
    user_input = input('Enter your name: ')
    if not re.match(r'^[a-zA-Z0-9 ]+$', user_input):
        raise ValueError("Input is Invalid! Only alphanumeric characters and spaces are allowed.")
    return user_input


def send_email(to, subject, body):
    """Send an email using secure SMTP."""
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = 'email@example.com'
        msg['To'] = to

        with smtplib.SMTP('localhost') as server:
            server.sendmail('email@example.com', [to], msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")


def get_data():
    """Fetch data from a secure API endpoint using HTTPS."""
    url = 'https://secure-api.com/get-data'
    try:
        parsed_url = urlparse(url)
        if parsed_url.scheme not in ['http', 'https']:
            raise ValueError("Unsupported URL scheme")

        headers = {'User-Agent': 'SecureClient/1.0'}
        req = Request(url, headers=headers)
        data = urlopen(req, timeout=5).read().decode()
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def save_to_db(data):
    """Save data to the database using parameterized queries."""
    query = "INSERT INTO mytable (column1, column2) VALUES (%s, %s)"
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            cursor.execute(query, (data, 'Another Value'))
        connection.commit()
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()


if __name__ == '__main__':
    try:
        user_input = get_user_input()
        data = get_data()
        if data:
            save_to_db(data)
        send_email('admin@example.com', 'User Input', user_input)
    except Exception as e:
        print(f"An error occurred: {e}")
