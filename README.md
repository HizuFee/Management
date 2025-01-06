


```markdown
# Panduan Setup 

## Clone Project
```bash
git clone https://github.com/HizuFee/Management.git
```

## Pindah ke Directory
```bash
cd Management
```

## Pastikan Database Sudah Ada
Pastikan database dengan nama **`inventory_db`** sudah dibuat.

## Langkah-Langkah

### 1. Buat Virtual Environment
```bash
python -m venv GUI-venv
```

### 2. Aktifkan Virtual Environment
```bash
GUI-venv\Scripts\activate
```

### 3. Install Dependencies
#### Pilihan 1: Install MySQL Connector Langsung
```bash
pip install mysql-connector-python
```

#### Pilihan 2: Install dari File `requirements.txt`
```bash
pip install -r requirements.txt
```

### 4. Jalankan Migration
```bash
python run_migration.py
```

### 5. Jalankan Aplikasi
```bash
python main.py
```
```
