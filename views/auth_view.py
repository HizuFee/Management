import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from controllers.auth_controller import AuthController
from views.main_view import InventoryApp

class LoginWindow(ttk.Window):
    def __init__(self):
        super().__init__(themename="cosmo")
        self.title("Admin Login")
        self.geometry("300x250")
        self.setup_ui()

    def setup_ui(self):
        ttk.Label(self, text="Username:").pack(pady=5)
        self.username_entry = ttk.Entry(self)
        self.username_entry.pack(pady=5)

        ttk.Label(self, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        ttk.Button(self, text="Login", command=self.login, bootstyle=PRIMARY).pack(pady=10)
        ttk.Button(self, text="Register", command=self.open_register, bootstyle=SECONDARY).pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Username dan password tidak boleh kosong!")
            return

        if len(username) < 3 or len(password) < 8:
            messagebox.showerror("Error", "Username minimal 3 karakter dan password minimal 8 karakter!")
            return

        if not username.isalnum() or not password.isalnum():
            messagebox.showerror("Error", "Username dan password hanya boleh mengandung huruf dan angka!")
            return

        if AuthController.login_admin(username, password):
            messagebox.showinfo("Success", "Login successful!")
            self.withdraw() 
            app = InventoryApp(self)
            app.mainloop()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def open_register(self):
        self.withdraw()
        RegisterWindow(self)

class RegisterWindow(ttk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Admin Register")
        self.geometry("300x250")
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        ttk.Label(self, text="Username:").pack(pady=5)
        self.username_entry = ttk.Entry(self)
        self.username_entry.pack(pady=5)

        ttk.Label(self, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        ttk.Button(self, text="Register", command=self.register, bootstyle=PRIMARY).pack(pady=10)
        ttk.Button(self, text="Back to Login", command=self.close_register, bootstyle=SECONDARY).pack(pady=5)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Username dan password tidak boleh kosong!")
            return

        if len(username) < 3 or len(password) < 8:
            messagebox.showerror("Error", "Username minimal 3 karakter dan password minimal 8 karakter!")
            return

        if not username.isalnum() or not password.isalnum():
            messagebox.showerror("Error", "Username dan password hanya boleh mengandung huruf dan angka!")
            return

        try:
            AuthController.register_admin(username, password)
            messagebox.showinfo("Success", "Registration successful!")
            self.close_register()  
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def close_register(self):
        self.destroy()
        self.parent.deiconify()

if __name__ == "__main__":
    login_window = LoginWindow()
    login_window.mainloop()