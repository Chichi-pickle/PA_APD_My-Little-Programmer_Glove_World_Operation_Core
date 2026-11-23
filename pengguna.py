from datetime import datetime, timedelta
from colorama import Fore, Style, init
from prettytable import PrettyTable
from InquirerPy import inquirer
from InquirerPy.separator import Separator
import utility

init(autoreset=True)

FORMAT_TANGGAL = "%Y-%m-%d"

HARI_ID = {
    0: "Senin",
    1: "Selasa",
    2: "Rabu",
    3: "Kamis",
    4: "Jumat",
    5: "Sabtu",
    6: "Minggu",
}


def _ambil_tanggal_main(item):
    nilai = item.get("tanggal_main")
    if not nilai or not isinstance(nilai, str):
        return None
    try:
        return datetime.strptime(nilai.strip(), FORMAT_TANGGAL).date()
    except ValueError:
        return None


def _daftar_7_hari_ke_depan():
    hari_ini = datetime.now().date()
    hasil = []
    for i in range(7):
        tgl = hari_ini + timedelta(days=i)
        nama_hari = HARI_ID.get(tgl.weekday(), "")
        tag = " (Hari Ini)" if i == 0 else (" (Besok)" if i == 1 else "")
        label = f"{nama_hari}, {tgl.strftime('%d-%m-%Y')}{tag}"
        hasil.append((tgl, label))
    return hasil


def perbarui_status_riwayat(riwayat_list):
    hari_ini = datetime.now().date()
    ada_perubahan = False
    for item in riwayat_list:
        if item.get("status") == "aktif":
            tgl_main = _ambil_tanggal_main(item)
            if tgl_main is not None and hari_ini > tgl_main:
                item["status"] = "tidak aktif"
                ada_perubahan = True
    return ada_perubahan


def hitung_sisa_kapasitas(wahana, tanggal_main, riwayat_list):
    kapasitas_maks = int(wahana.get("kapasitas", 0))
    id_wahana = wahana.get("id")
    nama_wahana = wahana.get("nama")

    terpakai = 0
    for r in riwayat_list:
        if r.get("status") != "aktif":
            continue
        cocok_wahana = (r.get("id_wahana") == id_wahana) or (
            id_wahana is None and r.get("wahana") == nama_wahana
        )
        if cocok_wahana and _ambil_tanggal_main(r) == tanggal_main:
            terpakai += int(r.get("jumlah_tiket", 1))

    return max(0, kapasitas_maks - terpakai)


def booking_wahana(user, wahana_list, riwayat_list, waktu_mulai=None):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== Booking Wahana ===")
    print(f"Saldo Koin Anda: {Fore.YELLOW}{user.get('coin', 0)} Koin\n")

    perbarui_status_riwayat(riwayat_list)

    if not wahana_list:
        print(f"{Fore.YELLOW}Belum ada data wahana tersedia.")
        return False

    opsi_tanggal = [{"name": label, "value": tgl} for tgl, label in _daftar_7_hari_ke_depan()]
    opsi_tanggal.append(Separator("-" * 35))
    opsi_tanggal.append({"name": "Kembali", "value": None})

    tanggal_main = inquirer.select(
        message="Pilih tanggal main (7 hari ke depan):",
        choices=opsi_tanggal,
        max_height="70%",
    ).execute()

    if tanggal_main is None:
        print(f"{Fore.YELLOW}Kembali ke menu pengunjung.")
        return False

    header_tabel = (
        f"  {'ID':<4} | {'NAMA WAHANA':<26} | {'KATEGORI':<10} | "
        f"{'HARGA':<9} | {'KAPASITAS':<18} | {'STATUS'}"
    )
    garis_bingkai = "-" * len(header_tabel)

    pilihan_wahana = [
        Separator(garis_bingkai),
        Separator(header_tabel),
        Separator(garis_bingkai),
    ]

    for w in wahana_list:
        id_str = f"#{w.get('id', '-')}"
        nama_str = str(w.get("nama", "-"))[:26]
        kat_str = str(w.get("kategori", "-"))[:10]
        harga_str = f"{w.get('harga', 0)} Koin"
        kap_maks = int(w.get("kapasitas", 0))
        sisa_slot = hitung_sisa_kapasitas(w, tanggal_main, riwayat_list)
        kap_str = f"{sisa_slot}/{kap_maks} kapasitas"
        status_str = str(w.get("status", "-")).upper()

        label = (
            f"{id_str:<4} | {nama_str:<26} | {kat_str:<10} | "
            f"{harga_str:<9} | {kap_str:<18} | {status_str}"
        )
        pilihan_wahana.append({"name": label, "value": w})

    pilihan_wahana.append(Separator(garis_bingkai))
    pilihan_wahana.append({"name": "Kembali", "value": None})

    wahana_dipilih = inquirer.select(
        message=f"Pilih wahana untuk tanggal {tanggal_main.strftime('%d-%m-%Y')}:",
        choices=pilihan_wahana,
        max_height="70%",
    ).execute()

    if wahana_dipilih is None:
        print(f"{Fore.YELLOW}Kembali ke menu pengunjung.")
        return False

    status_wahana = str(wahana_dipilih.get("status", "")).lower()
    sisa_slot = hitung_sisa_kapasitas(wahana_dipilih, tanggal_main, riwayat_list)

    if status_wahana != "tersedia" or sisa_slot <= 0:
        print(
            f"{Fore.RED}[GAGAL!] Wahana tidak tersedia pada tanggal tersebut "
            f"(Status: {wahana_dipilih.get('status', '-')} | Sisa kapasitas: {sisa_slot})."
        )
        return False

    while True:
        jumlah_orang = utility.input_angka_rekursif(
            f"Masukkan jumlah orang (1 - {sisa_slot} kapasitas tersedia): "
        )
        if jumlah_orang <= 0:
            print(f"{Fore.RED}[GAGAL!] Jumlah orang minimal 1.")
            continue
        if jumlah_orang > sisa_slot:
            print(f"{Fore.RED}[GAGAL!] Melebihi sisa kapasitas tanggal main ({sisa_slot}).")
            continue
        break

    harga_satuan = int(wahana_dipilih.get("harga", 0))
    total_harga = harga_satuan * jumlah_orang
    saldo_saat_ini = int(user.get("coin", 0))

    if saldo_saat_ini < total_harga:
        print(
            f"{Fore.RED}[GAGAL!] Koin tidak cukup untuk {jumlah_orang} orang "
            f"(Butuh: {total_harga} koin, Saldo Anda: {saldo_saat_ini} koin). "
            f"Silakan top-up terlebih dahulu."
        )
        return False

    user["coin"] = saldo_saat_ini - total_harga
    tanggal_booking_str = datetime.now().date().strftime(FORMAT_TANGGAL)
    tanggal_main_str = tanggal_main.strftime(FORMAT_TANGGAL)

    riwayat_list.append({
        "id_user": user.get("id", user.get("username")),
        "id_wahana": wahana_dipilih.get("id"),
        "wahana": wahana_dipilih.get("nama"),
        "jumlah_tiket": jumlah_orang,
        "tanggal_booking": tanggal_booking_str,
        "tanggal_main": tanggal_main_str,
        "status": "aktif",
    })

    print(
        f"{Fore.GREEN}Booking berhasil untuk {jumlah_orang} orang pada tanggal main "
        f"{tanggal_main.strftime('%d-%m-%Y')}! Sisa koin Anda: {user['coin']}."
    )
    return True


def top_up(user):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== Top-Up Koin ===")
    print(f"Jumlah koin saat ini: {Fore.YELLOW}{user.get('coin', 0)}")

    while True:
        jumlah = utility.input_angka_rekursif("Masukkan jumlah koin yang ingin di top-up: ")
        if jumlah <= 0:
            print(f"{Fore.RED}[GAGAL!] Jumlah top-up tidak valid.")
            continue
        if user.get("coin", 0) + jumlah > 9999:
            print(f"{Fore.RED}[GAGAL!] Jumlah koin melebihi batas maksimal (9999).")
            continue
        break

    user["coin"] = user.get("coin", 0) + jumlah
    print(f"{Fore.GREEN}Top-up berhasil! Saldo koin terbaru: {user['coin']}.")
    return True


def riwayat_booking(user, wahana_list=None, riwayat_list=None, waktu_mulai=None, perbarui_slot=None):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== Riwayat Booking ===")
    if riwayat_list is None:
        riwayat_list = []

    perbarui_status_riwayat(riwayat_list)
    if callable(perbarui_slot):
        perbarui_slot(wahana_list, riwayat_list, waktu_mulai)

    id_user = user.get("id", user.get("username"))
    riwayat_user = [r for r in riwayat_list if r.get("id_user") == id_user]

    if len(riwayat_user) == 0:
        print(f"{Fore.YELLOW}Belum ada riwayat booking.")
        return

    opsi_filter = [
        {"name": "Semua Riwayat", "value": "SEMUA"},
        Separator("-" * 35),
    ]
    for tgl, label in _daftar_7_hari_ke_depan():
        opsi_filter.append({"name": f"Tanggal Main: {label}", "value": tgl})
    opsi_filter.append(Separator("-" * 35))
    opsi_filter.append({"name": "Kembali", "value": None})

    pilihan_tanggal = inquirer.select(
        message="Filter riwayat booking (7 hari ke depan):",
        choices=opsi_filter,
        max_height="70%",
    ).execute()

    if pilihan_tanggal is None:
        print(f"{Fore.YELLOW}Kembali ke menu pengunjung.")
        return

    if pilihan_tanggal == "SEMUA":
        data_tampil = riwayat_user
    else:
        data_tampil = [r for r in riwayat_user if _ambil_tanggal_main(r) == pilihan_tanggal]

    if len(data_tampil) == 0:
        print(f"{Fore.YELLOW}Tidak ada riwayat booking untuk pilihan tersebut.")
        return

    tabel = PrettyTable()
    tabel.field_names = [
        "No",
        "Wahana",
        "Jumlah Orang",
        "Tanggal Booking",
        "Tanggal Main",
        "Status",
    ]

    for idx, item in enumerate(data_tampil, start=1):
        tgl_booking_raw = item.get("tanggal_booking", "-")
        if isinstance(tgl_booking_raw, str):
            try:
                tgl_booking_str = datetime.strptime(tgl_booking_raw.strip(), FORMAT_TANGGAL).strftime("%d-%m-%Y")
            except ValueError:
                tgl_booking_str = tgl_booking_raw
        else:
            tgl_booking_str = "-"

        tgl_main_obj = _ambil_tanggal_main(item)
        tgl_main_str = tgl_main_obj.strftime("%d-%m-%Y") if tgl_main_obj else str(item.get("tanggal_main", "-"))

        tabel.add_row([
            idx,
            item.get("wahana", "-"),
            item.get("jumlah_tiket", 1),
            tgl_booking_str,
            tgl_main_str,
            item.get("status", "-"),
        ])

    print(tabel)


def edit_akun_pengunjung(user, cek_username_ganda):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== Edit Akun Pengunjung ===")
    username_lama = user["username"]
    password_lama = user["password"]
    user_aktif = user.get("id", username_lama)

    while True:
        username_baru = input("Username baru (kosongkan jika tidak ingin diubah): ").strip()
        if username_baru == "":
            username_baru = username_lama
            break
        if not utility.validasi_panjang_input(username_baru, 4, 15):
            continue
        if cek_username_ganda(username_baru, user_aktif):
            print(f"{Fore.RED}[GAGAL!] Username sudah dipakai.")
            continue
        break

    while True:
        password_baru = input("Password baru (kosongkan jika tidak ingin diubah): ").strip()
        if password_baru == "":
            password_baru = password_lama
            break
        if not utility.validasi_panjang_input(password_baru, 6, 20):
            continue
        break

    user["username"] = username_baru
    user["password"] = password_baru
    print(f"{Fore.GREEN}Akun berhasil diubah.")
    return True