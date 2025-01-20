from config.database import get_connection
import hashlib


class Admin:
    @staticmethod
    def register(username, password):
        conn = get_connection()
        cursor = conn.cursor()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("INSERT INTO admin (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        conn.close()

    @staticmethod
    def login(username, password):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, hashed_password))
        admin = cursor.fetchone()
        conn.close()
        return admin
