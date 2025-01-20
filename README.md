## **Setup Guide Inventory Management**

# 1. jalankan untuk membuat virtual enviroment

         python -m venv GUI-venv

# 2. jalankan untuk mengaktifkan virtual enviroment

         GUI-venv\Scripts\activate

# 3. jalankan untuk menginstall library

         pip install mysql-connector-python
         ==========================================================
         or
         ==========================================================
         pip install -r requirements.txt

# 4. jalankan untuk migration database, pastikan koneksi dan nama database sesuai

         python run_migration.py

# 5. untuk menjalankan aplikasi

         python main.py

Berikut adalah representasi skema tabel dalam format Markdown:

---

## **Database Schema: `inventory_db`**

### **1. Table: `admin`**

| **Column Name** | **Data Type** | **Attributes**              |
| --------------- | ------------- | --------------------------- |
| `id`            | INT           | AUTO_INCREMENT, PRIMARY KEY |
| `username`      | VARCHAR(255)  | NOT NULL, UNIQUE            |
| `password`      | VARCHAR(255)  | NOT NULL                    |
| `created_at`    | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP   |

---

### **2. Table: `categories`**

| **Column Name** | **Data Type** | **Attributes**              |
| --------------- | ------------- | --------------------------- |
| `id`            | INT           | AUTO_INCREMENT, PRIMARY KEY |
| `name`          | VARCHAR(100)  | NOT NULL, UNIQUE            |
| `created_at`    | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP   |

---

### **3. Table: `items`**

| **Column Name** | **Data Type**  | **Attributes**                                           |
| --------------- | -------------- | -------------------------------------------------------- |
| `id`            | INT            | AUTO_INCREMENT, PRIMARY KEY                              |
| `name`          | VARCHAR(255)   | NOT NULL, UNIQUE                                         |
| `quantity`      | INT            | NOT NULL                                                 |
| `price`         | DECIMAL(10, 2) | NOT NULL                                                 |
| `description`   | TEXT           | NULL                                                     |
| `category_id`   | INT            | NULL, FOREIGN KEY -> `categories(id)` ON DELETE SET NULL |
| `unit`          | VARCHAR(50)    | DEFAULT 'pcs'                                            |
| `is_deleted`    | TINYINT(1)     | DEFAULT 0                                                |
| `created_at`    | TIMESTAMP      | DEFAULT CURRENT_TIMESTAMP                                |
| `updated_at`    | TIMESTAMP      | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP    |

---

### **4. Table: `history`**

| **Column Name**   | **Data Type**               | **Attributes**                                         |
| ----------------- | --------------------------- | ------------------------------------------------------ |
| `id`              | INT                         | AUTO_INCREMENT, PRIMARY KEY                            |
| `item_id`         | INT                         | NOT NULL, FOREIGN KEY -> `items(id)` ON DELETE CASCADE |
| `admin_id`        | INT                         | NOT NULL, FOREIGN KEY -> `admin(id)` ON DELETE CASCADE |
| `change_type`     | ENUM('in', 'out', 'delete') | NOT NULL                                               |
| `quantity_change` | INT                         | NOT NULL                                               |
| `timestamp`       | TIMESTAMP                   | DEFAULT CURRENT_TIMESTAMP                              |

---

### **5. Table: `audit_log`**

| **Column Name** | **Data Type**                      | **Attributes**                                         |
| --------------- | ---------------------------------- | ------------------------------------------------------ |
| `id`            | INT                                | AUTO_INCREMENT, PRIMARY KEY                            |
| `table_name`    | VARCHAR(50)                        | NOT NULL                                               |
| `record_id`     | INT                                | NULL                                                   |
| `action_type`   | ENUM('INSERT', 'UPDATE', 'DELETE') | NOT NULL                                               |
| `old_values`    | TEXT                               | NULL                                                   |
| `new_values`    | TEXT                               | NULL                                                   |
| `admin_id`      | INT                                | NOT NULL, FOREIGN KEY -> `admin(id)` ON DELETE CASCADE |
| `timestamp`     | TIMESTAMP                          | DEFAULT CURRENT_TIMESTAMP                              |

---
