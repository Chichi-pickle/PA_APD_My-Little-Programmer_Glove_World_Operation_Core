from utility import baca_database, save_data, WAHANA_FILE, input_angka_rekursif, HISTORY_FILE
import matplotlib.pyplot as plt
from colorama import Fore, Style
from InquirerPy import inquirer

def tambah_wahana():
    wahana = baca_database(WAHANA_FILE)

    print(f"{Fore.CYAN}{Style.BRIGHT}\n=== TAMBAH WAHANA ===")

    nama = input("Masukkan nama wahana: ")
    kategori = input("Masukkan kategori wahana: ")
    deskripsi = input("Masukkan deskripsi wahana: ")
    harga = input_angka_rekursif("Masukkan harga wahana: ")
    kapasitas = input_angka_rekursif("Masukkan kapasitas wahana: ")
    durasi = input_angka_rekursif("Masukkan durasi wahana (dalam menit): ")

    if len(wahana) == 0:
        id_baru = 1
    else:
        id_baru = max(data["id"] for data in wahana) + 1

    wahana_baru = {
        "id": id_baru,
        "nama": nama,
        "kategori": kategori,
        "deskripsi": deskripsi,
        "harga": harga,
        "kapasitas": kapasitas,
        "durasi": durasi,
        "status": "tersedia"
    }

    wahana.append(wahana_baru)

    save_data(WAHANA_FILE, wahana)

    print(f"{Fore.GREEN}{Style.BRIGHT}Wahana berhasil ditambahkan!")

def ubah_wahana():
    wahana = baca_database(WAHANA_FILE)
    id_wahana = input_angka_rekursif("Masukkan ID wahana yang ingin diubah: ")

    for data in wahana:
        if data["id"] == id_wahana:
            print(f"Data wahana dengan ID {id_wahana}:")
            print(f"Nama: {data['nama']}")
            print(f"Kategori: {data['kategori']}")
            print(f"Deskripsi: {data['deskripsi']}")
            print(f"Harga: {data['harga']}")
            print(f"Kapasitas: {data['kapasitas']}")
            print(f"Durasi: {data['durasi']}")

            print(f"{Fore.CYAN}{Style.BRIGHT}\n=== UBAH WAHANA ===")
            data["harga"] = input_angka_rekursif("Masukkan harga wahana baru: ")
            data["kapasitas"] = input_angka_rekursif("Masukkan kapasitas wahana baru: ")
            data["durasi"] = input_angka_rekursif("Masukkan durasi wahana baru (dalam menit): ")

            save_data(WAHANA_FILE, wahana)
            print("Wahana berhasil diubah!")
            return

    print("Wahana tidak ditemukan!")

def hapus_wahana():
    wahana = baca_database(WAHANA_FILE)
    id_wahana = input_angka_rekursif("Masukkan ID wahana yang ingin dihapus: ")

    for data in wahana:
        if data["id"] == id_wahana:
            wahana.remove(data)
            save_data(WAHANA_FILE, wahana)
            print("Wahana berhasil dihapus!")
            return

    print("Wahana tidak ditemukan!")

def update_status_wahana():
    wahana = baca_database(WAHANA_FILE)
    id_wahana = input_angka_rekursif("Masukkan ID wahana yang ingin diubah statusnya: ")

    for data in wahana:
        if data["id"] == id_wahana:
            print(f"Status saat ini: {data.get('status', 'Tidak tersedia')}")
            status_baru = inquirer.select(
                message="Pilih status baru:",
                choices=[
                    "Tersedia",
                    "Penuh",
                    "Sedang Maintenance"
                ]
            ).execute()
            data["status"] = status_baru
            save_data(WAHANA_FILE, wahana)
            print("Status wahana berhasil diubah! Status baru:", status_baru)
            return

    print("Wahana tidak ditemukan!")

def trafik_wahana():
    history = baca_database(HISTORY_FILE)
    wahana = baca_database(WAHANA_FILE)

    jumlah_booking = {}

    for data in history:
        if data["status"] == "aktif":
            id_wahana = data["id_wahana"]
            if id_wahana in jumlah_booking:
                jumlah_booking[id_wahana] += 1
            else:
                jumlah_booking[id_wahana] = 1

    nama_wahana = []
    total_booking = []

    for data in wahana:
        id_wahana = data["id"]

        if id_wahana in jumlah_booking:
            nama_wahana.append(data["nama"])
            total_booking.append(jumlah_booking[id_wahana])

    if not nama_wahana:
        print("Tidak ada data booking yang tersedia.")
        return

    plt.figure(figsize=(10, 5))
    plt.bar(nama_wahana, total_booking, color='skyblue')
    plt.title('Trafik Wahana')
    plt.xlabel('Nama Wahana')
    plt.ylabel('Jumlah Booking')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    plt.show()