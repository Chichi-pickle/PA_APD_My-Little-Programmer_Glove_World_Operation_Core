from colorama import init, Fore, Style
from InquirerPy import inquirer

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
    return pilihan
       

def menu_pengguna():
    print(f"{Fore.CYAN}{Style.BRIGHT}===== Menu Pengguna =====")
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
    return pilihan

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
    return pilihan
    
def menu_CRUD():
    print(f"{Fore.CYAN}{Style.BRIGHT}===== Manajemen Wahana =====")
    pilihan = inquirer.select(
        message="Pilih opsi 1~6:",
        choices=[
            "1. Tambah Wahana",
            "2. Edit harga/kapasitas",
            "3. Hapus Wahana",
            "4. Update Status",
            "5. Tampilkan Wahana",
            "6. Kembali"
        ],
    ).execute()
    return pilihan