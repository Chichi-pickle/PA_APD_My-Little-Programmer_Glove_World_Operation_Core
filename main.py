from utility import menu_CRUD

def main():
    while True:
        pilihan = menu_CRUD()
        if pilihan == "1. Tambah Wahana":
            print("Anda memilih untuk menambah wahana.")
            # Tambahkan logika untuk menambah wahana di sini
        elif pilihan == "2. Edit harga/kapasitas":
            print("Anda memilih untuk mengedit harga/kapasitas wahana.")
            # Tambahkan logika untuk mengedit harga/kapasitas di sini
        elif pilihan == "3. Hapus Wahana":
            print("Anda memilih untuk menghapus wahana.")
            # Tambahkan logika untuk menghapus wahana di sini
        elif pilihan == "4. Update Status":
            print("Anda memilih untuk memperbarui status wahana.")
            # Tambahkan logika untuk memperbarui status di sini
        elif pilihan == "5. Kembali ke Menu Admin":
            print("Kembali ke Menu Admin.")
            break  # Keluar dari loop dan kembali ke menu admin
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
  main()
