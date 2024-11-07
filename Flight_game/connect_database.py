import mysql.connector

def connect_database():
    return mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            database='flight_sim',
            user='root',
            password='root',
            charset='utf8mb4',
            collation='utf8mb4_general_ci',
            autocommit=True
    )
connect_database()
