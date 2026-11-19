import utility
import crud_admin


def jeda():
    input("\nTekan Enter untuk melanjutkan...")


def menu_admin():
    while True:
        utility.clear_screen()
        print("===== Menu Admin =====")
        print("1. Tambah Adventure")
        print("2. Lihat Adventure")
        print("3. Update Adventure")
        print("4. Hapus Adventure")
        print("5. Logout")
        pilihan = input("Pilih dari 1-5: ").strip()

        if pilihan == "1":
            crud_admin.tambah_adventure()
        elif pilihan == "2":
            crud_admin.lihat_adventure()
        elif pilihan == "3":
            crud_admin.update_adventure()
        elif pilihan == "4":
            crud_admin.hapus_adventure()
        elif pilihan == "5":
            print("Logout berhasil!")
            jeda()
            return
        else:
            print("Pilihan tidak tersedia!")
            jeda()


def menu_pengguna():
    while True:
        utility.clear_screen()
        print("===== Menu Pengguna =====")
        print("1. Adventure Board")
        print("2. Logout")
        pilihan = input("Pilih 1 atau 2: ").strip()

        if pilihan == "1":
            print("\n=== ADVENTURE BOARD ===")
            crud_admin.lihat_adventure()
        elif pilihan == "2":
            print("Logout berhasil!")
            jeda()
            return
        else:
            print("Pilihan tidak tersedia!")
            jeda()