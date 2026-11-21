from colorama import Fore, Style, init
from prettytable import PrettyTable
from utility import validasi_panjang_input

init(autoreset=True)


def grafik_wahana_favorit(riwayat_list):
    frekuensi = {}
    for item in riwayat_list:
        nama_wahana = item.get("wahana")
        if nama_wahana:
            frekuensi[nama_wahana] = frekuensi.get(nama_wahana, 0) + 1

    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== Grafik Frekuensi Wahana Kesukaan Pengunjung ===")
    if len(frekuensi) == 0:
        print(f"{Fore.YELLOW}{Style.BRIGHT}Belum ada data riwayat booking.")
        return

    tabel = PrettyTable()
    tabel.field_names = ["Wahana", "Jumlah Booking", "Grafik"]
    for nama_wahana, jumlah in frekuensi.items():
        tabel.add_row([nama_wahana, jumlah, "*" * jumlah])
    print(tabel)

def edit_akun_admin(admin_data, cek_username_ganda):
    username_lama = admin_data["username"]
    password_lama = admin_data["password"]
    id_admin = admin_data.get("id", username_lama)

    while True:
        username_baru = input("Username baru (kosongkan jika tidak ingin diubah): ")
        if username_baru == "":
            username_baru = username_lama
            break
        if not validasi_panjang_input(username_baru, 4, 15):
            continue
        if cek_username_ganda(username_baru, id_admin):
            print(f"{Fore.RED}{Style.BRIGHT}[GAGAL!] Username sudah dipakai!")
            continue
        break

    while True:
        password_baru = input("Password baru (kosongkan jika tidak ingin diubah): ")
        if password_baru == "":
            password_baru = password_lama
            break
        if not validasi_panjang_input(password_baru, 6, 20):
            continue
        break

    admin_data["username"] = username_baru
    admin_data["password"] = password_baru
    print(f"{Fore.GREEN}{Style.BRIGHT}Akun berhasil diubah.")