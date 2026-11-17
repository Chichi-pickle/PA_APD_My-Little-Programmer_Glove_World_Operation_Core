import csv
import os

DB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database'))

USER_HEADERS = ('id', 'username', 'password', 'koin', 'role')
WAHANA_HEADERS = ('nomor', 'nama', 'harga', 'kapasitas', 'slot_tersedia', 'status')
HISTORY_HEADERS = ('id_user', 'nama_wahana', 'waktu_mulai', 'waktu_selesai', 'status')

DEFAULT_ADMIN = {
    'id': '1',
    'username': 'admin',
    'password': 'admin123',
    'koin': '0',
    'role': 'admin'
}


def load_csv(filename):
    filepath = os.path.join(DB_DIR, filename)
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]
    except (csv.Error, OSError) as e:
        print(f"[Error Database] Gagal membaca {filename}: {e}")
        return []


def save_csv(filename, data, fieldnames):
    os.makedirs(DB_DIR, exist_ok=True)
    filepath = os.path.join(DB_DIR, filename)

    try:
        with open(filepath, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(data)
        return True
    except PermissionError:
        print(f"[Error Database] Akses ditolak! Tutup file {filename} jika sedang dibuka di Excel.")
        return False
    except OSError as e:
        print(f"[Error Database] Gagal menyimpan {filename}: {e}")
        return False


def init_db():
    os.makedirs(DB_DIR, exist_ok=True)

    schema_map = {
        'users.csv': USER_HEADERS,
        'wahana.csv': WAHANA_HEADERS,
        'history.csv': HISTORY_HEADERS
    }

    for filename, headers in schema_map.items():
        filepath = os.path.join(DB_DIR, filename)
        if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
            save_csv(filename, [], headers)

    users = load_csv('users.csv')
    if not users:
        save_csv('users.csv', [DEFAULT_ADMIN], USER_HEADERS)


def generate_id(users_list):
    if not users_list:
        return 1
    existing_ids = [int(u['id']) for u in users_list if str(u.get('id', '')).isdigit()]
    return max(existing_ids) + 1 if existing_ids else 1
