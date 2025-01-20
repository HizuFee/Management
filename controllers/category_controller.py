# controllers/category_controller.py
from controllers.auth_controller import AuthController
from models.category import Category
from models.audit import Audit
class CategoryController:
    @staticmethod
    def get_all_categories():
        return Category.get_all()

    @staticmethod
    def add_new_category(name):
        category_id = Category.add_category(name)
        new_data = {'id': category_id, 'name': name}
        admin_id = AuthController.get_logged_in_admin_id()
        Audit.log_change('categories', category_id, 'INSERT', {}, new_data, admin_id)

    @staticmethod
    def update_category(category_id, name):
        # Fetch existing data for logging
        old_data = Category.get_category_by_id(category_id)
        new_data = {'name': name}
        Category.update_category(category_id, name)
        admin_id = AuthController.get_logged_in_admin_id()
        Audit.log_change('categories', category_id, 'UPDATE', old_data, new_data, admin_id)

    @staticmethod
    def delete_category(category_id):
        # Fetch existing data for logging
        old_data = Category.get_category_by_id(category_id)
        Category.delete_category(category_id)
        admin_id = AuthController.get_logged_in_admin_id()
        Audit.log_change('categories', category_id, 'DELETE', old_data, {}, admin_id)

    @staticmethod
    def get_category_by_id(category_id):
        return Category.get_category_by_id(category_id)