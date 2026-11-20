from datetime import timedelta
from colorama import Fore, Style, init
from prettytable import PrettyTable
from utility import input_angka_rekursif, validasi_panjang_input, waktu_simulasi

init(autoreset = True)


def booking_wahana(user, wahana_list, riwayat_list, waktu_mulai, tampilkan_wahana):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}==== Booking Wahana ====")
    tampilkan_wahana(wahana_list)

    id_pilih = input_angka_rekursif("Masukkan ID wahana yang dipilih: ")
    wahana_dipilih = next((w for w in wahana_list if w.get("id") == id_pilih), None)

    if (
        wahana_dipilih is None
        or wahana_dipilih.get("status") != "tersedia"
        or wahana_dipilih.get("kapasitas", 0) <= 0
    ):
        print(f"{Fore.RED}[GAGAL!] Wahana tidak tersedia (Perbaikan / kapasitas penuh).")
        return

    if user.get("coin", 0) < wahana_dipilih.get("harga", 0):
        print(f"{Fore.RED}[GAGAL!] Koin yang anda miliki tidak cukup, silahkan top-up terlebih dahulu.")
        return

    user["coin"] -= wahana_dipilih["harga"]
    wahana_dipilih["kapasitas"] -= 1

    durasi = wahana_dipilih.get("durasi", 30)
    waktu_mulai_booking = waktu_simulasi(waktu_mulai)
    waktu_selesai_booking = waktu_mulai_booking + timedelta(minutes=durasi)

    riwayat_list.append({
        "id_user": user.get("id", user.get("username")),
        "id_wahana": wahana_dipilih.get("id"),
        "wahana": wahana_dipilih.get("nama"),
        "waktu_mulai": waktu_mulai_booking,
        "waktu_selesai": waktu_selesai_booking,
        "status": "aktif",
    })

    print(f"{Fore.GREEN}Booking anda telah berhasil, kami menunggu kedatangan anda.")

def top_up(user):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}==== Top-Up Koin ====")
    print(f"Jumlah koin saat ini: {Fore.YELLOW}{user.get('coin', 0)}")

    while True:
        jumlah = input_angka_rekursif("Masukkan jumlah koin yang ingin di top-up: ")
        if jumlah > 0:
            break
        print(f"{Fore.RED}[GAGAL!] Jumlah top-up tidak valid.")

    user["coin"] = user.get("coin", 0) + jumlah
    print(f"{Fore.GREEN}Top-up berhasil! Saldo koin terbaru: {user['coin']}.")

def riwayat_booking(user, wahana_list, riwayat_list, waktu_mulai, perbarui_slot=None):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}==== Riwayat Booking ====")
    if callable(perbarui_slot):
        perbarui_slot(wahana_list, riwayat_list, waktu_mulai)
        
    id_user = user.get("id", user.get("username"))
    riwayat_user = []
    for r in riwayat_list:
        if r.get("id_user") == id_user:
            riwayat_user.append(r)

    if len(riwayat_user) == 0:
        print(f"{Fore.YELLOW}Belum ada riwayat booking")
        return

    tabel = PrettyTable()
    tabel.field_names = ["No", "Wahana", "Waktu Mulai", "Waktu Selesai", "Status"]
    for idx, item in enumerate(riwayat_user, start=1):
        waktu_mulai_item = item.get("waktu_mulai")
        waktu_selesai_item = item.get("waktu_selesai")

        if waktu_mulai_item is not None:
            mulai_str = waktu_mulai_item.strftime("%H:%M")
        else:
            mulai_str = "-"

        if waktu_selesai_item is not None:
            selesai_str = waktu_selesai_item.strftime("%H:%M")
        else:
            selesai_str = "-"

        tabel.add_row([
            idx,
            item.get("wahana", "-"),
            mulai_str,
            selesai_str,
            item.get("status", "-"),
        ])
    print(tabel)

def edit_akun_pengunjung(user, cek_username_ganda):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}==== Edit Akun Pengunjung ====")
    username_lama = user["username"]
    password_lama = user["password"]
    user_aktif = user.get("id", username_lama)

    while True:
        username_baru = input("Username baru (kosongkan jika tidak ingin diubah): ")
        if username_baru == "":
            username_baru = username_lama
            break
        if not validasi_panjang_input(username_baru, 4, 15):
            continue
        if cek_username_ganda(username_baru, user_aktif):
            print(f"{Fore.RED}[GAGAL!] Username sudah dipakai.")
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

    user["username"] = username_baru
    user["password"] = password_baru
    print(f"{Fore.GREEN}Akun berhasil diubah.")