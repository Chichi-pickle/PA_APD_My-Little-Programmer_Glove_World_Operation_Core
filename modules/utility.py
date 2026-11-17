import os
from datetime import datetime, timedelta
from prettytable import PrettyTable
from colorama import init, Fore, Style
from db_handler import load_csv, save_csv, WAHANA_HEADERS, HISTORY_HEADERS


init(autoreset=True)

FORMAT_WAKTU = "%Y-%m-%d %H:%M:%S"


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def waktu_simulasi(waktu_mulai):
    selisih_nyata = datetime.now() - waktu_mulai
    selisih_simulasi = timedelta(seconds=selisih_nyata.total_seconds() * 60)
    return waktu_mulai + selisih_simulasi


def perbarui_slot(waktu_mulai):
    history_list = load_csv('history.csv')
    if not history_list:
        return

    wahana_list = load_csv('wahana.csv')
    sekarang = waktu_simulasi(waktu_mulai)
    ada_perubahan = False

    for item in history_list:
        if item['status'] == 'aktif':
            waktu_selesai = datetime.strptime(item['waktu_selesai'], FORMAT_WAKTU)
            if sekarang >= waktu_selesai:
                item['status'] = 'selesai'
                ada_perubahan = True

                # Kembalikan +1 slot ke wahana terkait
                for w in wahana_list:
                    if w['nama'] == item['nama_wahana']:
                        slot_baru = int(w['slot_tersedia']) + 1
                        kapasitas_maks = int(w['kapasitas'])
                        w['slot_tersedia'] = str(min(slot_baru, kapasitas_maks))
                        break

    if ada_perubahan:
        save_csv('history.csv', history_list, HISTORY_HEADERS)
        save_csv('wahana.csv', wahana_list, WAHANA_HEADERS)


def input_angka_rekursif(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print(f"{Fore.RED}[!] Input tidak valid. Harap masukkan angka bulat.")
        return input_angka_rekursif(prompt)


def tampilkan_wahana(waktu_mulai):
    perbarui_slot(waktu_mulai)
    wahana_list = load_csv('wahana.csv')

    if not wahana_list:
        print(f"{Fore.YELLOW}Belum ada data wahana yang tersedia saat ini.")
        return False

    tabel = PrettyTable()
    tabel.field_names = ["No", "Nama Wahana", "Harga (Koin)", "Sisa Slot", "Status"]

    for w in wahana_list:
        status_teks = (
            f"{Fore.GREEN}{w['status']}{Style.RESET_ALL}"
            if w['status'] == 'Buka'
            else f"{Fore.RED}{w['status']}{Style.RESET_ALL}"
        )
        slot_info = f"{w['slot_tersedia']}/{w['kapasitas']}"
        tabel.add_row([w['nomor'], w['nama'], w['harga'], slot_info, status_teks])

    print(tabel)
    return True