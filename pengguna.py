from datetime import timedelta, datetime
from colorama import Fore, Style, init
import inquirer
from prettytable import PrettyTable
from InquirerPy import inquirer
from InquirerPy.separator import Separator
import utility 

init(autoreset = True)
FORMAT_WAKTU = "%Y-%m-%d %H:%M:%S"

def booking_wahana(user, wahana_list, riwayat_list, waktu_mulai):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== Booking Wahana ===")
    print(f"Saldo Koin Anda: {Fore.YELLOW}{user.get('coin', 0)} Koin\n")

    if not wahana_list:
        print(f"{Fore.YELLOW}Belum ada data wahana tersedia.")
        return

    header_tabel = (
        f"  {'ID':<4} | {'NAMA WAHANA':<26} | {'KATEGORI':<10} | "
        f"{'HARGA':<9} | {'SLOT':<4} | {'DURASI':<6} | {'STATUS'}"
    )
    garis_bingkai = "-" * len(header_tabel)

    pilihan_wahana = [
        Separator(garis_bingkai),
        Separator(header_tabel),
        Separator(garis_bingkai),
    ]

    for w in wahana_list:
        id_str = f"#{w.get('id', '-')}"
        nama_str = w.get('nama', '-')[:26]
        kat_str = w.get('kategori', '-')[:10]
        harga_str = f"{w.get('harga', 0)} Koin"
        slot_str = f"{w.get('kapasitas', 0)}"
        durasi_str = f"{w.get('durasi', 0)}m"
        status_str = w.get('status', '-').upper()

        label = (
            f"{id_str:<4} | {nama_str:<26} | {kat_str:<10} | "
            f"{harga_str:<9} | {slot_str:<4} | {durasi_str:<6} | {status_str}"
        )
        pilihan_wahana.append({"name": label, "value": w})

    pilihan_wahana.append(Separator(garis_bingkai))
    pilihan_wahana.append({"name": "Batal / Kembali", "value": None})

    wahana_dipilih = inquirer.select(
        message="Pilih wahana yang ingin dibooking:",
        choices=pilihan_wahana,
        max_height="70%",  
    ).execute()
    user["coin"] -= wahana_dipilih["harga"]
    wahana_dipilih["kapasitas"] -= 1
    
    durasi = wahana_dipilih.get("durasi", 30)
    waktu_mulai_booking = utility.waktu_simulasi(waktu_mulai)
    waktu_selesai_booking = waktu_mulai_booking + timedelta(minutes=durasi)
    print(f"{Fore.GREEN}Booking anda telah berhasil, kami menunggu kedatangan anda.")
    riwayat_list.append({
        "id_user": user.get("id", user.get("username")),
        "id_wahana": wahana_dipilih.get("id"),
        "wahana": wahana_dipilih.get("nama"),
        "waktu_mulai": waktu_mulai_booking.strftime(FORMAT_WAKTU),
        "waktu_selesai": waktu_selesai_booking.strftime(FORMAT_WAKTU),
        "status": "aktif",
    
    
    })
    if wahana_dipilih is None:
        print(f"{Fore.YELLOW}Booking dibatalkan.")
        return

def top_up(user):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== Top-Up Koin ===")
    print(f"Jumlah koin saat ini: {Fore.YELLOW}{user.get('coin', 0)}")

    while True:
        jumlah = utility.input_angka_rekursif("Masukkan jumlah koin yang ingin di top-up: ")
        if jumlah > 0:
            break
        print(f"{Fore.RED}[GAGAL!]Jumlah top-up tidak valid.")
    if user.get("coin", 0) + jumlah > 9999:
        print(f"{Fore.RED}[GAGAL!]Jumlah koin melebihi batas maksimal (9999).")
        utility.clear_screen()
        top_up(user)
        return
    user["coin"] = user.get("coin", 0) + jumlah
    print(f"{Fore.GREEN}Top-up berhasil! Saldo koin terbaru: {user['coin']}.")
    return

def riwayat_booking(user, wahana_list, riwayat_list, waktu_mulai, perbarui_slot=None):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== Riwayat Booking ===")
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

        if isinstance(waktu_mulai_item, str):
            mulai_dt = datetime.strptime(waktu_mulai_item, "%Y-%m-%d %H:%M:%S")
            mulai_str = mulai_dt.strftime("%H:%M")
        elif waktu_mulai_item is not None:
            mulai_str = waktu_mulai_item.strftime("%H:%M")
        else:
            mulai_str = "-"

        if isinstance(waktu_selesai_item, str):
            selesai_dt = datetime.strptime(waktu_selesai_item, "%Y-%m-%d %H:%M:%S")
            selesai_str = selesai_dt.strftime("%H:%M")
        elif waktu_selesai_item is not None:
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
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== Edit Akun Pengunjung ===")
    username_lama = user["username"]
    password_lama = user["password"]
    user_aktif = user.get("id", username_lama)

    while True:
        username_baru = input("Username baru (kosongkan jika tidak ingin diubah): ")
        if username_baru == "":
            username_baru = username_lama
            break
        if not utility.validasi_panjang_input(username_baru, 4, 15):
            continue
        if cek_username_ganda(username_baru, user_aktif):
            print(f"{Fore.RED}[GAGAL!]Username sudah dipakai.")
            continue
        break

    while True:
        password_baru = input("Password baru (kosongkan jika tidak ingin diubah): ")
        if password_baru == "":
            password_baru = password_lama
            break
        if not utility.validasi_panjang_input(password_baru, 6, 20):
            continue
        break

    user["username"] = username_baru
    user["password"] = password_baru
    print(f"{Fore.GREEN}Akun berhasil diubah.")