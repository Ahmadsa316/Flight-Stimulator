import mysql.connector
from connect_database import connect_database


def execute_sql_file(cursor, file_path):
    # Read the SQL file
    with open(file_path, 'r') as sql_file:
        sql_commands = sql_file.read()

    # Split SQL commands by semicolon
    commands = sql_commands.split(';')

    # Execute each command
    for command in commands:
        command = command.strip()  # Remove any leading/trailing whitespaces
        if command:
            try:
                print(f"Executing command:\n{command}\n")  # Log the command
                cursor.execute(command)
            except Exception as e:
                print(f"Error executing command: {command}\nError: {e}")


if __name__ == "__main__":
    try:
        connection = connect_database()  # Use your own function to connect to MariaDB/MySQL
        cursor = connection.cursor()

        # Execute the first SQL script (e.g., initial setup or drop tables)
        execute_sql_file(cursor, 'flight_simulator_database_script.sql')

        # Execute the second SQL script
        execute_sql_file(cursor, 'setup_db.sql')

        # Commit changes to the database
        connection.commit()
        print("Database setup completed successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Database connection closed.")
