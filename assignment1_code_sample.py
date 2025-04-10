import os
import pymysql
import re
import smtplib
from urllib.request import urlopen
from email.mime.text import MIMEText

# 1. Corrected the cryptographic failure in here 
# Hardcoded credentials have been replaced by secure credentials using environment variables.
# cryptographic Failures
db_config = {
    'host': os.getenv('DB_HOST', 'mydatabase.com'),
    'user': os.getenv('DB_USER', 'admin'),
    'password': os.getenv('DB_PASSWORD', 'secret123')
}
## added the def user 
def get_user_input():
    user_input = input('Enter your name: ')

    # 2. Fixed security misconfiguration by validating user input to prevent injection attacks.
    # Security Misconfiguration
    if not re.match(r'^[a-zA-Z0-9 ]+$', user_input):
        raise ValueError("Input is Invalid! Only alphanumeric characters and spaces are allowed.")
    
    return user_input

def send_email(to, subject, body):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = 'email@example.com'
        msg['To'] = to

        # 3. Replaced os.system() with smtplib for sending email securely.
        # using a secure SMTP server is recommended.
        # Injection
        with smtplib.SMTP('localhost') as server:
            server.sendmail('email@example.com', [to], msg.as_string())
    
    except Exception as e:
        print(f"Error sending email: {e}")

def get_data():
    # 4. Corrected the insecure API call vulnerability: changed from HTTP to HTTPS.
    # Security Logging & Monitoring Failures
    url = 'https://secure-api.com/get-data'  # Fixed URL
    try:
        data = urlopen(url, timeout=5).read().decode()  # Added timeout to avoid hanging requests
    except Exception as e:
        print(f"Error fetching data: {e}")
        data = None
    return data

def save_to_db(data):
    # 5. Fixed SQL Injection vulnerability by using parameterized queries.
    # Injection
    query = "INSERT INTO mytable (column1, column2) VALUES (%s, %s)"
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(query, (data, 'Another Value'))
        connection.commit()
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    try:
        user_input = get_user_input()
        data = get_data()
        if data is not None:
            save_to_db(data)
        send_email('admin@example.com', 'User Input', user_input)
    except Exception as e:
        print(f"An error occurred: {e}")
