import os
from colorama import init, Fore, Style
from datetime import datetime, timedelta
from InquirerPy import inquirer



def clear_screen():
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

def menu_utama():
    print(f"{Fore.CYAN}{Style.BRIGHT}===== Menu Utama =====")
    pilihan = inquirer.select(
            message="Pilih opsi 1~4:",
            choices=[
                "1. Login",
                "2. Register",
                "3. Tentang GloveWorld",
                "4. Exit",
            ],
        ).execute()   

def menu_pengunjung():
    print(f"{Fore.CYAN}{Style.BRIGHT}===== Menu Pengunjung =====")
    pilihan = inquirer.select(
            message="Pilih opsi 1~6:",
            choices=[
                "1. Lihat Wahana",
                "2. Booking Wahana",
                "3. Riwayat Booking",
                "4. Edit Profile",
                "5. Top-up Koin", 
                "6. Logout"
            ],
        ).execute()   

def menu_admin():
    print(f"{Fore.CYAN}{Style.BRIGHT}===== Menu Admin =====")
    pilihan = inquirer.select(
            message="Pilih opsi 1~4:",
            choices=[
                "1. Manajemen Wahana",
                "2. Grafik Wahana",
                "3. Edit Profile",
                "4. Logout",
            ],
        ).execute()   
    
def menu_CRUD():
    print(f"{Fore.CYAN}{Style.BRIGHT}===== Manajemen Wahana =====")
    pilihan = inquirer.select(
        message="Pilih opsi 1~6:",
        choices=[
            "1. Tambah Wahana",
            "2. Edit harga/kapasitas",
            "3. Hapus Wahana",
            "4. Update Status",
            "5. Trafik Wahana",
            "6. Kembali"
        ],
    ).execute()

def validasi_panjang_input(input_str, min_teks, max_teks):
    if len(input_str) < min_teks or len(input_str) > max_teks:
        print(f"{Fore.RED}[GAGAL!] Input harus antara {min_teks} dan {max_teks} karakter. Coba lagi.")
        return False
    return True
