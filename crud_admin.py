import matplotlib.pyplot as plt
from colorama import Fore, Style, init
from InquirerPy import inquirer
# [PERUBAHAN] Mengganti 'baca_database' menjadi 'load_data' dan menambahkan 'input_teks_wajib'.
# [MEKANISME] 'baca_database' dihapus dari utility.py karena fungsinya sama dengan 'load_data', sedangkan 'input_teks_wajib' memvalidasi agar teks tidak kosong/spasi saja.
# [NOTULENSI] Notulensi Konsul 2 (21 Nov 2026) - poin "Isi wahana enggak boleh kosong" & "Spasi enggak kehitung karakter".
from utility import load_data, save_data, input_angka_rekursif, input_teks_wajib

init(autoreset=True)

WAHANA_FILE = "wahana.json"
HISTORY_FILE = "history.json"


# [PERUBAHAN] Menambahkan helper '_buat_id_tersedia' untuk pengisian ID wahana.
# [MEKANISME] Melakukan iterasi angka mulai dari 1 hingga menemukan ID pertama yang belum dipakai di wahana_list, lalu data diurutkan berdasarkan ID saat disimpan agar ID lama tidak bergeser.
# [NOTULENSI] Notulensi Konsul 2 (21 Nov 2026) - poin "Pengisian wahana: saling mengisi slot yang kosong".
def _buat_id_tersedia(wahana_list):
    id_terpakai = {w.get("id") for w in wahana_list if isinstance(w.get("id"), int)}
    id_baru = 1
    while id_baru in id_terpakai:
        id_baru += 1
    return id_baru

# [PERUBAHAN] Menambahkan helper '_input_angka_positif'.
# [MEKANISME] Membungkus 'input_angka_rekursif' dengan perulangan validasi batas minimal agar harga, kapasitas, dan durasi tidak bernilai negatif atau 0 (untuk kapasitas & durasi).
# [NOTULENSI] Notulensi Konsul 2 (21 Nov 2026) - poin "Isi wahana enggak boleh kosong" & validasi data wahana.
def _input_angka_positif(prompt, minimal=1):
    while True:
        nilai = input_angka_rekursif(prompt)
        if nilai < minimal:
            print(f"{Fore.RED}[GAGAL!] Nilai minimal adalah {minimal}. Coba lagi.")
            continue
        return nilai


def tambah_wahana():
    # [PERUBAHAN] Menggunakan load_data(WAHANA_FILE) alih-alih baca_database(WAHANA_FILE).
    # [MEKANISME] Membaca file JSON dari folder databases/ menggunakan helper standar load_data.
    # [NOTULENSI] Konsistensi struktur penyimpanan database di folder databases/.
    wahana = load_data(WAHANA_FILE)

    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== TAMBAH WAHANA ===")

    # [PERUBAHAN] Input nama, kategori, dan deskripsi memakai input_teks_wajib().
    # [MEKANISME] Input di-.strip() dan ditolak jika kosong ("") atau hanya spasi sebelum diterima.
    # [NOTULENSI] Notulensi Konsul 2 (21 Nov 2026) - poin "Isi wahana enggak boleh kosong" & "Spasi enggak kehitung karakter".
    nama = input_teks_wajib("Masukkan nama wahana: ")
    kategori = input_teks_wajib("Masukkan kategori wahana: ")
    deskripsi = input_teks_wajib("Masukkan deskripsi wahana: ")
    harga = _input_angka_positif("Masukkan harga wahana (koin): ", minimal=0)
    kapasitas = _input_angka_positif("Masukkan kapasitas wahana: ", minimal=1)
    durasi = _input_angka_positif("Masukkan durasi wahana (dalam menit): ", minimal=1)

    # [PERUBAHAN] Mengganti rumus max(id) + 1 menjadi _buat_id_tersedia(wahana) + sort berdasarkan id.
    # [MEKANISME] Jika misalnya ID 13 dihapus dari 14 wahana, wahana baru mendapat ID 13 lalu list diurutkan ulang berdasarkan ID.
    # [NOTULENSI] Notulensi Konsul 2 (21 Nov 2026) - poin "Pengisian wahana: saling mengisi slot yang kosong".
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

            # [PERUBAHAN] Setiap field boleh dikosongkan (tekan Enter) untuk mempertahankan nilai lama, dan input spasi saja ditolak/diabaikan.
            # [MEKANISME] Jika input == "", nilai lama tetap dipakai; jika input.strip() == "", admin diberi peringatan/diabaikan agar spasi tidak masuk sebagai data valid.
            # [NOTULENSI] Notulensi Konsul 2 (21 Nov 2026) - poin "Ubah wahana: alur ubah wahana caranya disamain aja kayak di edit profil" & "Spasi enggak kehitung karakter".
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
            # [PERUBAHAN] Menyeragamkan pilihan status menjadi huruf kecil dan menambah opsi "Batal".
            # [MEKANISME] Menggunakan inquirer.select agar konsisten dengan pengecekan status di modul pengguna ('tersedia') serta memberi jalan keluar jika batal.
            # [NOTULENSI] Notulensi Konsul 2 (21 Nov 2026) - konsistensi alur & validasi status wahana.
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


def trafik_wahana():
    history = load_data(HISTORY_FILE)
    wahana = load_data(WAHANA_FILE)

    jumlah_booking = {}
    for data in history:
        if str(data.get("status", "")).lower() == "aktif":
            id_wahana = data.get("id_wahana")
            tiket = int(data.get("jumlah_tiket", 1))
            if id_wahana is not None:
                jumlah_booking[id_wahana] = jumlah_booking.get(id_wahana, 0) + tiket

    rekap = []
    for data in wahana:
        id_wahana = data.get("id")
        if id_wahana in jumlah_booking:
            rekap.append((data.get("nama", f"ID {id_wahana}"), jumlah_booking[id_wahana]))

    if not rekap:
        print(f"{Fore.YELLOW}Tidak ada data booking aktif yang tersedia.")
        return

    # [PERUBAHAN] Mengurutkan data dari terbesar ke terkecil dan membatasi maksimal 10 data dengan slicing [:10].
    # [MEKANISME] Melakukan sorted(..., reverse=True)[:10] sebelum membuat bar chart matplotlib agar grafik tidak terlalu padat jika jumlah wahana banyak.
    # [NOTULENSI] Notulensi Konsul 2 (21 Nov 2026) - poin "Batas grafik wahana: buat grafik wahana dibatasin aja misalnya maksimal 10 tertinggi".
    rekap_top10 = sorted(rekap, key=lambda x: x[1], reverse=True)[:10]
    nama_wahana = [item[0] for item in rekap_top10]
    total_booking = [item[1] for item in rekap_top10]

    plt.figure(figsize=(10, 5))
    plt.bar(nama_wahana, total_booking, color="skyblue", edgecolor="black")
    plt.title("Trafik Wahana Aktif (Maks. 10 Tertinggi)")
    plt.xlabel("Nama Wahana")
    plt.ylabel("Jumlah Booking")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()