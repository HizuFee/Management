# models/category.py
from config.database import get_connection

class Category:
    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categories")
        result = cursor.fetchall()
        conn.close()
        return result

    @staticmethod
    def add_category(name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO categories (name) VALUES (%s)",
            (name,)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def update_category(category_id, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE categories SET name=%s WHERE id=%s",
            (name, category_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete_category(category_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM categories WHERE id=%s", (category_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_category_by_id(category_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categories WHERE id=%s", (category_id,))
        result = cursor.fetchone()
        conn.close()
        return result