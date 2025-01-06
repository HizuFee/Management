import mysql.connector
from config.database import get_connection

def run_migrations():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        with open('migrations/schema.sql', 'r') as f:
            sql_commands = f.read().split(';')
            for command in sql_commands:
                if command.strip():
                    cursor.execute(command)
        conn.commit()
        print("Migrations executed successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    run_migrations()
