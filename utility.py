import os
import json
from colorama import init, Fore, Style
from datetime import datetime, timedelta
import textwrap

DATABASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "databases")
USERS_FILE = os.path.join(DATABASE_DIR, "users.json")
WAHANA_FILE = os.path.join(DATABASE_DIR, "wahana.json")
HISTORY_FILE = os.path.join(DATABASE_DIR, "history.json")

def baca_database(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def load_data(nama_file):
    file_path = os.path.join(DATABASE_DIR, nama_file)
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def save_data(nama_file, data):
    os.makedirs(DATABASE_DIR, exist_ok=True)
    file_path = os.path.join(DATABASE_DIR, nama_file)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def login(users_list):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== Login GloveWorld ===")
    username = input("Username: ")
    password = input("Password: ")

    for user in users_list:
        if user.get("username") == username and user.get("password") == password:
            print(f"{Fore.GREEN}Login berhasil! Selamat datang, {username} ({user.get('role')}).")
            return user

    print(f"{Fore.RED}[GAGAL!] Username atau password salah.")
    return None

def register(users_list):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== Register Akun Baru GloveWorld ===")

    while True:
        username = input("Masukkan username baru: ").strip()
        if not validasi_panjang_input(username, 4, 15):
            continue
        if any(u.get("username") == username for u in users_list):
            print(f"{Fore.RED}[GAGAL!] Username '{username}' sudah digunakan. Pilih yang lain.")
            continue
        break

    while True:
        password = input("Masukkan password baru: ").strip()
        if not validasi_panjang_input(password, 6, 20):
            continue
        break

    id_baru = max((u.get("id", 0) for u in users_list), default=0) + 1

    user_baru = {
        "id": id_baru,
        "username": username,
        "password": password,
        "role": "pengguna",
        "coin": 0
    }

    users_list.append(user_baru)
    print(f"{Fore.GREEN}Registrasi berhasil! Akun '{username}' siap digunakan untuk login.")

def clear_screen():
    input(f"\n{Fore.YELLOW}Tekan Enter untuk melanjutkan...")
    os.system('cls' if os.name == 'nt' else 'clear')

def input_angka_rekursif(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print(f"{Fore.RED}[GAGAL!] Input wajib berupa angka mutlak (tanpa huruf/simbol). Coba lagi.")
        return input_angka_rekursif(prompt)

def waktu_simulasi(waktu_mulai):
    selisih_nyata = datetime.now() - waktu_mulai
    selisih_simulasi = timedelta(seconds=selisih_nyata.total_seconds() * 60)
    return waktu_mulai + selisih_simulasi

def validasi_panjang_input(input_str, min_teks = 4, max_teks = 20):
    if len(input_str) < min_teks:
        print(f"{Fore.RED}[GAGAL!] Input minimal {min_teks} karakter. Coba lagi.")
        return False
    if len(input_str) > max_teks:
        print(f"{Fore.RED}[GAGAL!] Input maksimal {max_teks} karakter. Coba lagi.")
        return False
    return True

def tampilkan_wahana(wahana_list):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}================ DAFTAR WAHANA GLOVEWORLD ================")
    if not wahana_list:
        print(f"{Fore.YELLOW}Belum ada data wahana tersedia.")
        return

    lebar = 56  
    garis = "+" + "-" * (lebar + 2) + "+"

    for w in wahana_list:
        id_w = w.get("id", "-")
        nama = w.get("nama", "-").upper()
        kategori = w.get("kategori", "-")
        harga = w.get("harga", 0)
        kapasitas = w.get("kapasitas", 0)
        durasi = w.get("durasi", 0)
        status = w.get("status", "-").lower()
        deskripsi = w.get("deskripsi", "-")

        warna_status = Fore.GREEN if status == "tersedia" else Fore.RED

        header = f"[ID: {id_w}] {nama} ({kategori})"
        info = f"Harga: {harga} Koin | Kapasitas: {kapasitas} | Durasi: {durasi}m"

        print(f"{Fore.CYAN}{garis}")
        print(f"{Fore.CYAN}| {Fore.YELLOW}{Style.BRIGHT}{header:<{lebar}}{Style.RESET_ALL} {Fore.CYAN}|")
        print(f"{Fore.CYAN}| {Fore.WHITE}{info:<{lebar}} {Fore.CYAN}|")
        print(f"{Fore.CYAN}| {Fore.WHITE}Status: {warna_status}{status.upper():<{lebar - 8}} {Fore.CYAN}|")
        print(f"{Fore.CYAN}{garis}")

        baris_deskripsi = textwrap.wrap(deskripsi, width=lebar)
        for baris in baris_deskripsi:
            print(f"{Fore.CYAN}| {Fore.LIGHTBLACK_EX}{baris:<{lebar}} {Fore.CYAN}|")

        print(f"{Fore.CYAN}{garis}\n")