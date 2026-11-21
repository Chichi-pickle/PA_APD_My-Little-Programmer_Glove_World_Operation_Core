from colorama import Fore, Style, init
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from datetime import datetime, timedelta
from prettytable import PrettyTable
from utility import validasi_panjang_input

init(autoreset=True)
FORMAT_WAKTU = "%Y-%m-%d %H:%M:%S"

def grafik_wahana_favorit(riwayat_list):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== Grafik Frekuensi Wahana Favorit (3 Bulan Terakhir) ===")
    
    batas_waktu = datetime.now() - timedelta(days=90)
    frekuensi = {}

    for item in riwayat_list:
        nama_wahana = item.get("wahana")
        waktu_str = item.get("waktu_mulai")
        
        if not nama_wahana or not waktu_str:
            continue

        try:
            if isinstance(waktu_str, str):
                waktu_booking = datetime.strptime(waktu_str, FORMAT_WAKTU)
            else:
                waktu_booking = waktu_str
        except ValueError:
            continue

        if waktu_booking >= batas_waktu:
            frekuensi[nama_wahana] = frekuensi.get(nama_wahana, 0) + 1

    if len(frekuensi) == 0:
        print(f"{Fore.YELLOW}{Style.BRIGHT}Belum ada data riwayat booking dalam 3 bulan terakhir.")
        return

    data_urut = sorted(frekuensi.items(), key=lambda x: x[1], reverse=True)
    daftar_wahana = [x[0] for x in data_urut] # Sumbu X 
    total_booking = [x[1] for x in data_urut] # Sumbu Y 

    # Tetap tampilkan ringkasan tabel di CLI sebelum jendela grafik terbuka
    tabel = PrettyTable()
    tabel.field_names = ["Wahana", "Total Booking (3 Bulan Terakhir)"]
    for nama, jumlah in data_urut:
        tabel.add_row([nama, jumlah])
    print(tabel)

    print(f"{Fore.GREEN}Membuka jendela grafik... (Tutup jendela grafik untuk kembali ke menu)")

    # Membuat Bar Chart dengan Matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(daftar_wahana, total_booking, color="#0b60b0", edgecolor="black", width=0.6)

    # Judul dan label sumbu
    ax.set_title("Total Booking Wahana GloveWorld (3 Bulan Terakhir)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Nama Wahana", fontsize=11, fontweight="bold", labelpad=10)
    ax.set_ylabel("Total Booking", fontsize=11, fontweight="bold", labelpad=10)

    # Miringkan label nama wahana di sumbu X agar tidak saling bertumpuk
    plt.xticks(rotation=30, ha="right")

    # Paksa angka sumbu Y menjadi bilangan bulat (bukan koma/desimal)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    # Tampilkan angka exact di atas setiap batang grafik
    for bar in bars:
        tinggi = bar.get_height()
        ax.annotate(
            f"{tinggi}",
            xy=(bar.get_x() + bar.get_width() / 2, tinggi),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontweight="bold"
        )

    plt.tight_layout()
    plt.show()

# def grafik_wahana_favorit(riwayat_list):
#     frekuensi = {}
#     for item in riwayat_list:
#         nama_wahana = item.get("wahana")
#         if nama_wahana:
#             frekuensi[nama_wahana] = frekuensi.get(nama_wahana, 0) + 1

#     print(f"\n{Fore.CYAN}{Style.BRIGHT}=== Grafik Frekuensi Wahana Kesukaan Pengunjung ===")
#     if len(frekuensi) == 0:
#         print(f"{Fore.YELLOW}{Style.BRIGHT}Belum ada data riwayat booking.")
#         return

#     tabel = PrettyTable()
#     tabel.field_names = ["Wahana", "Jumlah Booking", "Grafik"]
#     for nama_wahana, jumlah in frekuensi.items():
#         tabel.add_row([nama_wahana, jumlah, "*" * jumlah])
#     print(tabel)

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