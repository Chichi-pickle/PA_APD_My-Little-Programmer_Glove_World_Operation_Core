import matplotlib.pyplot as plt
from colorama import Fore, Style, init
from InquirerPy import inquirer
from utility import load_data, save_data, input_angka_rekursif, input_teks_wajib

init(autoreset=True)

WAHANA_FILE = "wahana.json"
HISTORY_FILE = "history.json"


def _buat_id_tersedia(wahana_list):
    id_terpakai = {w.get("id") for w in wahana_list if isinstance(w.get("id"), int)}
    id_baru = 1
    while id_baru in id_terpakai:
        id_baru += 1
    return id_baru

def _input_angka_positif(prompt, minimal=1):
    while True:
        nilai = input_angka_rekursif(prompt)
        if nilai < minimal:
            print(f"{Fore.RED}[GAGAL!] Nilai minimal adalah {minimal}. Coba lagi.")
            continue
        return nilai


def tambah_wahana():
    wahana = load_data(WAHANA_FILE)

    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== TAMBAH WAHANA ===")

    nama = input_teks_wajib("Masukkan nama wahana: ")
    kategori = input_teks_wajib("Masukkan kategori wahana: ")
    deskripsi = input_teks_wajib("Masukkan deskripsi wahana: ")
    harga = _input_angka_positif("Masukkan harga wahana (koin): ", minimal=0)
    kapasitas = _input_angka_positif("Masukkan kapasitas wahana: ", minimal=1)
    durasi = _input_angka_positif("Masukkan durasi wahana (dalam menit): ", minimal=1)

    id_baru = _buat_id_tersedia(wahana)

    wahana_baru = {
        "id": id_baru,
        "nama": nama,
        "kategori": kategori,
        "deskripsi": deskripsi,
        "harga": harga,
        "kapasitas": kapasitas,
        "durasi": durasi,
        "status": "tersedia",
    }

    wahana.append(wahana_baru)
    wahana.sort(key=lambda x: x.get("id", 0))
    save_data(WAHANA_FILE, wahana)

    print(f"{Fore.GREEN}{Style.BRIGHT}Wahana '{nama}' berhasil ditambahkan dengan ID #{id_baru}!")


def ubah_wahana():
    wahana = load_data(WAHANA_FILE)
    if not wahana:
        print(f"{Fore.YELLOW}Belum ada data wahana untuk diubah.")
        return

    id_wahana = input_angka_rekursif("Masukkan ID wahana yang ingin diubah: ")

    for data in wahana:
        if data.get("id") == id_wahana:
            print(f"\n{Fore.CYAN}{Style.BRIGHT}=== UBAH WAHANA (ID #{id_wahana}) ===")
            print(f"Nama saat ini      : {data.get('nama', '-')}")
            print(f"Kategori saat ini  : {data.get('kategori', '-')}")
            print(f"Deskripsi saat ini : {data.get('deskripsi', '-')}")
            print(f"Harga saat ini     : {data.get('harga', 0)}")
            print(f"Kapasitas saat ini : {data.get('kapasitas', 0)}")
            print(f"Durasi saat ini    : {data.get('durasi', 0)} menit\n")

            nama_baru = input("Nama baru (kosongkan jika tidak ingin diubah): ")
            if nama_baru != "":
                if nama_baru.strip() == "":
                    print(f"{Fore.YELLOW}Input spasi diabaikan, nama lama dipertahankan.")
                else:
                    data["nama"] = nama_baru.strip()

            kategori_baru = input("Kategori baru (kosongkan jika tidak ingin diubah): ")
            if kategori_baru != "":
                if kategori_baru.strip() == "":
                    print(f"{Fore.YELLOW}Input spasi diabaikan, kategori lama dipertahankan.")
                else:
                    data["kategori"] = kategori_baru.strip()

            deskripsi_baru = input("Deskripsi baru (kosongkan jika tidak ingin diubah): ")
            if deskripsi_baru != "":
                if deskripsi_baru.strip() == "":
                    print(f"{Fore.YELLOW}Input spasi diabaikan, deskripsi lama dipertahankan.")
                else:
                    data["deskripsi"] = deskripsi_baru.strip()

            while True:
                harga_input = input("Harga baru (kosongkan jika tidak ingin diubah): ")
                if harga_input == "":
                    break
                if harga_input.strip() == "":
                    print(f"{Fore.RED}[GAGAL!] Input tidak boleh hanya spasi.")
                    continue
                try:
                    nilai_harga = int(harga_input.strip())
                    if nilai_harga < 0:
                        print(f"{Fore.RED}[GAGAL!] Harga tidak boleh minus.")
                        continue
                    data["harga"] = nilai_harga
                    break
                except ValueError:
                    print(f"{Fore.RED}[GAGAL!] Harga wajib berupa angka.")

            while True:
                kap_input = input("Kapasitas baru (kosongkan jika tidak ingin diubah): ")
                if kap_input == "":
                    break
                if kap_input.strip() == "":
                    print(f"{Fore.RED}[GAGAL!] Input tidak boleh hanya spasi.")
                    continue
                try:
                    nilai_kap = int(kap_input.strip())
                    if nilai_kap < 1:
                        print(f"{Fore.RED}[GAGAL!] Kapasitas minimal 1.")
                        continue
                    data["kapasitas"] = nilai_kap
                    break
                except ValueError:
                    print(f"{Fore.RED}[GAGAL!] Kapasitas wajib berupa angka.")

            while True:
                dur_input = input("Durasi baru dalam menit (kosongkan jika tidak ingin diubah): ")
                if dur_input == "":
                    break
                if dur_input.strip() == "":
                    print(f"{Fore.RED}[GAGAL!] Input tidak boleh hanya spasi.")
                    continue
                try:
                    nilai_dur = int(dur_input.strip())
                    if nilai_dur < 1:
                        print(f"{Fore.RED}[GAGAL!] Durasi minimal 1 menit.")
                        continue
                    data["durasi"] = nilai_dur
                    break
                except ValueError:
                    print(f"{Fore.RED}[GAGAL!] Durasi wajib berupa angka.")

            save_data(WAHANA_FILE, wahana)
            print(f"{Fore.GREEN}{Style.BRIGHT}Wahana berhasil diubah!")
            return

    print(f"{Fore.RED}Wahana dengan ID #{id_wahana} tidak ditemukan!")


def hapus_wahana():
    wahana = load_data(WAHANA_FILE)
    if not wahana:
        print(f"{Fore.YELLOW}Belum ada data wahana untuk dihapus.")
        return

    id_wahana = input_angka_rekursif("Masukkan ID wahana yang ingin dihapus: ")

    for idx, data in enumerate(wahana):
        if data.get("id") == id_wahana:
            nama_dihapus = data.get("nama", "-")
            wahana.pop(idx)
            save_data(WAHANA_FILE, wahana)
            print(f"{Fore.GREEN}{Style.BRIGHT}Wahana '{nama_dihapus}' (ID #{id_wahana}) berhasil dihapus!")
            return

    print(f"{Fore.RED}Wahana dengan ID #{id_wahana} tidak ditemukan!")


def update_status_wahana():
    wahana = load_data(WAHANA_FILE)
    if not wahana:
        print(f"{Fore.YELLOW}Belum ada data wahana.")
        return

    id_wahana = input_angka_rekursif("Masukkan ID wahana yang ingin diubah statusnya: ")

    for data in wahana:
        if data.get("id") == id_wahana:
            print(f"Status saat ini: {data.get('status', 'tidak tersedia')}")
            status_baru = inquirer.select(
                message="Pilih status baru:",
                choices=[
                    "tersedia",
                    "penuh",
                    "sedang maintenance",
                    "Batal",
                ],
            ).execute()

            if status_baru is None or status_baru == "Batal":
                print(f"{Fore.YELLOW}Perubahan status dibatalkan.")
                return

            data["status"] = status_baru
            save_data(WAHANA_FILE, wahana)
            print(f"{Fore.GREEN}Status wahana berhasil diubah menjadi: {status_baru}")
            return

    print(f"{Fore.RED}Wahana dengan ID #{id_wahana} tidak ditemukan!")


