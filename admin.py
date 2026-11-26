from colorama import Fore, Style, init
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from datetime import datetime, timedelta
from prettytable import PrettyTable
from utility import validasi_panjang_input

init(autoreset=True)

def grafik_wahana_favorit(riwayat_list):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== Grafik Frekuensi Wahana Favorit (3 Bulan Terakhir) ===")

    batas_tanggal = (datetime.now() - timedelta(days=90)).date()
    frekuensi = {}

    for item in riwayat_list:
        nama_wahana = item.get("wahana")
        tgl_raw = item.get("tanggal_booking") or item.get("waktu_mulai")

        if not nama_wahana or not tgl_raw or not isinstance(tgl_raw, str):
            continue

        tgl_bersih = tgl_raw.strip()
        tgl_obj = None
        for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S"):
            try:
                tgl_obj = datetime.strptime(tgl_bersih, fmt).date()
                break
            except ValueError:
                continue

        if tgl_obj is None:
            continue

        if tgl_obj >= batas_tanggal:
            tiket = int(item.get("jumlah_tiket", 1))
            frekuensi[nama_wahana] = frekuensi.get(nama_wahana, 0) + tiket

    if len(frekuensi) == 0:
        print(f"{Fore.YELLOW}{Style.BRIGHT}Belum ada data riwayat booking dalam 3 bulan terakhir.")
        return

    data_urut = sorted(frekuensi.items(), key=lambda x: x[1], reverse=True)[:10]
    daftar_wahana = [x[0] for x in data_urut]
    total_booking = [x[1] for x in data_urut]

    tabel = PrettyTable()
    tabel.field_names = ["Wahana", "Total Booking (3 Bulan Terakhir)"]
    for nama, jumlah in data_urut:
        tabel.add_row([nama, jumlah])
    print(tabel)

    print(f"{Fore.GREEN}Membuka jendela grafik... (Tutup jendela grafik untuk kembali ke menu)")

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(daftar_wahana, total_booking, color="#0b60b0", edgecolor="black", width=0.6)

    ax.set_title("Total Booking Wahana GloveWorld (3 Bulan Terakhir - Maks. 10)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Nama Wahana", fontsize=11, fontweight="bold", labelpad=10)
    ax.set_ylabel("Total Booking", fontsize=11, fontweight="bold", labelpad=10)

    plt.xticks(rotation=30, ha="right")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    for bar in bars:
        tinggi = bar.get_height()
        ax.annotate(
            f"{tinggi}",
            xy=(bar.get_x() + bar.get_width() / 2, tinggi),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontweight="bold",
        )

    plt.tight_layout()
    plt.show()

def edit_akun_admin(admin_data, cek_username_ganda):
    username_lama = admin_data["username"]
    password_lama = admin_data["password"]
    id_admin = admin_data.get("id", username_lama)

    while True:
        username_baru = input("Username baru (kosongkan jika tidak ingin diubah): ").strip()
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
        password_baru = input("Password baru (kosongkan jika tidak ingin diubah): ").strip()
        if password_baru == "":
            password_baru = password_lama
            break
        if not validasi_panjang_input(password_baru, 6, 20):
            continue
        break

    admin_data["username"] = username_baru
    admin_data["password"] = password_baru
    print(f"{Fore.GREEN}{Style.BRIGHT}Akun berhasil diubah.")
