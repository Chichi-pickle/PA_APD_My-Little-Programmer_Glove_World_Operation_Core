import os
import json
import textwrap
from datetime import datetime, timedelta
from colorama import init, Fore, Style
from InquirerPy import inquirer

init(autoreset=True)

DATABASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "databases")
USERS_FILE = os.path.join(DATABASE_DIR, "users.json")
WAHANA_FILE = os.path.join(DATABASE_DIR, "wahana.json")
HISTORY_FILE = os.path.join(DATABASE_DIR, "history.json")


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


def input_teks_wajib(prompt, izinkan_batal=False):
    while True:
        teks = input(prompt).strip()
        if izinkan_batal and teks.lower() in ("0", "batal", "keluar"):
            return None
        if teks == "":
            print(f"{Fore.RED}[GAGAL!] Input tidak boleh kosong atau hanya spasi. Coba lagi.")
            continue
        return teks


def login(users_list):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== Login GloveWorld ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    for user in users_list:
        if user.get("username") == username and user.get("password") == password:
            print(f"{Fore.GREEN}Login berhasil! Selamat datang, {username} ({user.get('role')}).")
            return user

    print(f"{Fore.RED}[GAGAL!] Username atau password salah.")
    return None


def register(users_list):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== Register Akun Baru GloveWorld ===")
    print(f"{Fore.LIGHTBLACK_EX}(Ketik '0' atau 'batal' kapan saja untuk kembali ke Menu Utama)")

    while True:
        username = input_teks_wajib("Masukkan username baru: ", izinkan_batal=True)
        if username is None:
            print(f"{Fore.YELLOW}Registrasi dibatalkan.")
            return False
        if not validasi_panjang_input(username, 4, 15):
            continue
        if any(u.get("username") == username for u in users_list):
            print(f"{Fore.RED}[GAGAL!] Username '{username}' sudah digunakan. Pilih yang lain.")
            continue
        break

    while True:
        password = input_teks_wajib("Masukkan password baru: ", izinkan_batal=True)
        if password is None:
            print(f"{Fore.YELLOW}Registrasi dibatalkan.")
            return False
        if not validasi_panjang_input(password, 6, 20):
            continue
        break

    id_baru = max((u.get("id", 0) for u in users_list), default=0) + 1

    user_baru = {
        "id": id_baru,
        "username": username,
        "password": password,
        "role": "pengguna",
        "coin": 0,
    }

    users_list.append(user_baru)
    print(f"{Fore.GREEN}Registrasi berhasil! Akun '{username}' siap digunakan untuk login.")
    return True


def clear_screen():
    input(f"\n{Fore.YELLOW}Tekan Enter untuk melanjutkan...")
    os.system("cls" if os.name == "nt" else "clear")


def clear_screen_langsung():
    os.system("cls" if os.name == "nt" else "clear")


def input_angka_rekursif(prompt):
    try:
        nilai = int(input(prompt).strip())
        return nilai
    except ValueError:
        print(f"{Fore.RED}[GAGAL!] Input wajib berupa angka mutlak (tanpa huruf/simbol/spasi kosong). Coba lagi.")
        return input_angka_rekursif(prompt)


def waktu_simulasi(waktu_mulai):
    selisih_nyata = datetime.now() - waktu_mulai
    selisih_simulasi = timedelta(seconds=selisih_nyata.total_seconds() * 60)
    return waktu_mulai + selisih_simulasi


def validasi_panjang_input(input_str, min_teks=4, max_teks=20):
    teks_bersih = input_str.strip()
    if len(teks_bersih) == 0:
        print(f"{Fore.RED}[GAGAL!] Input tidak boleh hanya spasi.")
        return False
    if len(teks_bersih) < min_teks:
        print(f"{Fore.RED}[GAGAL!] Input minimal {min_teks} karakter. Coba lagi.")
        return False
    if len(teks_bersih) > max_teks:
        print(f"{Fore.RED}[GAGAL!] Input maksimal {max_teks} karakter. Coba lagi.")
        return False
    return True


def _cetak_card_wahana(w, tampilkan_deskripsi=True):
    lebar = 56
    garis = "+" + "-" * (lebar + 2) + "+"

    id_w = w.get("id", "-")
    nama = str(w.get("nama", "-")).upper()
    kategori = w.get("kategori", "-")
    harga = w.get("harga", 0)
    kapasitas = w.get("kapasitas", 0)
    durasi = w.get("durasi", 0)
    status = str(w.get("status", "-")).lower()
    deskripsi = w.get("deskripsi", "-")

    warna_status = Fore.GREEN if status == "tersedia" else Fore.RED

    header = f"[ID: {id_w}] {nama} ({kategori})"
    info = f"Harga: {harga} Koin | Kapasitas: {kapasitas} | Durasi: {durasi}m"

    print(f"{Fore.CYAN}{garis}")
    print(f"{Fore.CYAN}| {Fore.YELLOW}{Style.BRIGHT}{header:<{lebar}}{Style.RESET_ALL} {Fore.CYAN}|")
    print(f"{Fore.CYAN}| {Fore.WHITE}{info:<{lebar}} {Fore.CYAN}|")
    print(f"{Fore.CYAN}| {Fore.WHITE}Status: {warna_status}{status.upper():<{lebar - 8}} {Fore.CYAN}|")
    print(f"{Fore.CYAN}{garis}")

    if tampilkan_deskripsi:
        baris_deskripsi = textwrap.wrap(deskripsi, width=lebar)
        for baris in baris_deskripsi:
            print(f"{Fore.CYAN}| {Fore.LIGHTBLACK_EX}{baris:<{lebar}} {Fore.CYAN}|")
        print(f"{Fore.CYAN}{garis}")

    print()


def tampilkan_wahana(wahana_list, batas=None, tampilkan_deskripsi=True):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}================ DAFTAR WAHANA GLOVEWORLD ================")
    if not wahana_list:
        print(f"{Fore.YELLOW}Belum ada data wahana tersedia.")
        return

    data_tampil = wahana_list[:batas] if batas is not None else wahana_list
    for w in data_tampil:
        _cetak_card_wahana(w, tampilkan_deskripsi=tampilkan_deskripsi)


def tentang_gloveworld(wahana_list=None):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== Tentang GloveWorld ===")
    print(
        "\nSelamat datang di GloveWorld!\n\n"
        "GloveWorld adalah taman hiburan yang menawarkan berbagai wahana menarik dan pengalaman seru bagi pengunjung dari segala usia. "
        "Dengan berbagai pilihan wahana, pengunjung dapat menikmati keseruan dan kegembiraan yang tak terlupakan. "
        "Kami berkomitmen untuk memberikan pengalaman yang aman, menyenangkan, dan memuaskan bagi semua pengunjung kami. "
        "Selalu ingat, jika ingin bersenang-senang, datanglah ke GloveWorld dan rasakan sensasi yang luar biasa!\n\n"
        "GloveWorld, Beyond Fun, Beyond Adventure!"
    )

    if wahana_list:
        tampilkan_wahana(wahana_list, batas=3, tampilkan_deskripsi=False)
        if len(wahana_list) > 3:
            aksi = inquirer.select(
                message=f"Menampilkan 3 dari {len(wahana_list)} wahana. Pilih tindakan:",
                choices=[
                    "Lihat Selengkapnya (Semua Wahana)",
                    "Kembali",
                ],
            ).execute()
            if aksi == "Lihat Selengkapnya (Semua Wahana)":
                clear_screen_langsung()
                tampilkan_wahana(wahana_list, tampilkan_deskripsi=True)