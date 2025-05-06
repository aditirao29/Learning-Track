import mysql.connector

DB_NAME = 'learning_tracker_db'

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': DB_NAME
}

base_db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234'
}

def create_database():
    connection = mysql.connector.connect(**base_db_config)
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    connection.close()

def create_table():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS topics (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT
        )
    ''')
    connection.close()

def create_user_table():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) NOT NULL,
        password VARCHAR(255) NOT NULL
    );
    """)
    connection.close()

def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

def get_all_topics():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM topics')
    topics = cursor.fetchall()
    conn.close()
    return topics

def add_topic(title, description):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO topics (title, description) VALUES (%s, %s)', (title, description))
    conn.commit()
    conn.close()

def get_topic_by_id(topic_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM topics WHERE id = %s', (topic_id,))
    topic = cursor.fetchone()
    conn.close()
    return topic

def update_topic(topic_id, title, description):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE topics SET title = %s, description = %s WHERE id = %s', (title, description, topic_id))
    conn.commit()
    conn.close()

def delete_topic(topic_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM topics WHERE id = %s', (topic_id,))
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()
    conn.close()
    return user
