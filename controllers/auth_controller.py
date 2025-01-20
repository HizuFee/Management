from models.admin import Admin


class AuthController:
    
    logged_in_admin_id = None 

    @staticmethod
    def register_admin(username, password):
        Admin.register(username, password)

    @staticmethod
    def login_admin(username, password):
        admin = Admin.login(username, password)
        if admin:
            AuthController.logged_in_admin_id = admin['id']
        return admin

    @staticmethod
    def get_logged_in_admin_id():
        return AuthController.logged_in_admin_id