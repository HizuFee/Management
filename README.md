### Setup Guide
# Clone project
         git clone https://github.com/HizuFee/Management.git

# pindah directory
         cd Management
         
# **pastikan database bernama inventory_db sudah ada**

# 1. jalankan

         python -m venv GUI-venv

# 2. jalankan

         GUI-venv\Scripts\activate

# 3. jalankan

         pip install mysql-connector-python
         ==========================================================
         or
         ==========================================================
         pip install -r requirements.txt

# 5. jalankan

         python run_migration.py
         
# 6. jalankan

         python main.py
