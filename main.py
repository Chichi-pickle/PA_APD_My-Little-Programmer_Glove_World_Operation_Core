import menu
import utility
import pengguna
import admin
import crud_admin
from datetime import datetime

if __name__ == "__main__":
    WAKTU_MULAI = datetime.now()
    while True:
        utility.clear_screen_langsung()
        pilihan_menu = menu.menu_utama()

        if pilihan_menu == "1. Login":
            users = utility.load_data("users.json")
            user = utility.login(users)
            utility.clear_screen()

            if user:
                if user.get("role") == "pengguna":
                    while True:
                        utility.clear_screen_langsung()
                        pilihan_pengguna = menu.menu_pengguna()

                        if pilihan_pengguna == "1. Lihat Wahana":
                            utility.tampilkan_wahana(wahana_list=utility.load_data("wahana.json"))
                            utility.clear_screen()

                        elif pilihan_pengguna == "2. Booking Wahana":
                            wahana_list = utility.load_data("wahana.json")
                            riwayat_list = utility.load_data("history.json")

                            pengguna.booking_wahana(user, wahana_list, riwayat_list, WAKTU_MULAI)

                            utility.save_data("users.json", users)
                            utility.save_data("wahana.json", wahana_list)
                            utility.save_data("history.json", riwayat_list)
                            utility.clear_screen()

                        elif pilihan_pengguna == "3. Riwayat Booking":
                            wahana_list = utility.load_data("wahana.json")
                            riwayat_list = utility.load_data("history.json")

                            pengguna.riwayat_booking(user, wahana_list, riwayat_list, WAKTU_MULAI)

                            utility.save_data("history.json", riwayat_list)
                            utility.clear_screen()

                        elif pilihan_pengguna == "4. Edit Profile":
                            pengguna.edit_akun_pengunjung(
                                user,
                                cek_username_ganda=lambda username_baru, user_aktif: any(
                                    u.get("username") == username_baru and u.get("id", u.get("username")) != user_aktif
                                    for u in users
                                ),
                            )
                            utility.save_data("users.json", users)
                            utility.clear_screen()

                        elif pilihan_pengguna == "5. Top-up Koin":
                            pengguna.top_up(user)
                            utility.save_data("users.json", users)
                            utility.clear_screen()

                        elif pilihan_pengguna == "6. Logout":
                            print("Terimakasih telah menggunakan layanan kami, sampai jumpa lagi!!")
                            utility.clear_screen()
                            break

                        else:
                            print("Pilihan tidak valid. Silakan coba lagi.")
                            utility.clear_screen()

                elif user.get("role") == "admin":
                    while True:
                        utility.clear_screen_langsung()
                        pilihan_admin = menu.menu_admin()

                        if pilihan_admin == "1. Manajemen Wahana":
                            while True:
                                utility.clear_screen_langsung()
                                pilihan_CRUD = menu.menu_CRUD()

                                if pilihan_CRUD == "1. Tambah Wahana":
                                    utility.tampilkan_wahana(wahana_list=utility.load_data("wahana.json"))
                                    crud_admin.tambah_wahana()
                                    utility.clear_screen()

                                elif pilihan_CRUD == "2. Edit harga/kapasitas":
                                    utility.tampilkan_wahana(wahana_list=utility.load_data("wahana.json"))
                                    crud_admin.ubah_wahana()
                                    utility.clear_screen()

                                elif pilihan_CRUD == "3. Hapus Wahana":
                                    utility.tampilkan_wahana(wahana_list=utility.load_data("wahana.json"))
                                    crud_admin.hapus_wahana()
                                    utility.clear_screen()

                                elif pilihan_CRUD == "4. Update Status":
                                    utility.tampilkan_wahana(wahana_list=utility.load_data("wahana.json"))
                                    crud_admin.update_status_wahana()
                                    utility.clear_screen()

                                elif pilihan_CRUD == "5. Tampilkan Wahana":
                                    utility.tampilkan_wahana(wahana_list=utility.load_data("wahana.json"))
                                    utility.clear_screen()

                                elif pilihan_CRUD == "6. Kembali":
                                    break

                                else:
                                    print("Pilihan tidak valid. Silakan coba lagi.")
                                    utility.clear_screen()

                        elif pilihan_admin == "2. Grafik Wahana":
                            riwayat_list = utility.load_data("history.json")
                            admin.grafik_wahana_favorit(riwayat_list=riwayat_list)
                            utility.save_data("history.json", riwayat_list)
                            utility.clear_screen()

                        elif pilihan_admin == "3. Edit Profile":
                            admin.edit_akun_admin(
                                user,
                                cek_username_ganda=lambda username_baru, user_aktif: any(
                                    u.get("username") == username_baru and u.get("id", u.get("username")) != user_aktif
                                    for u in users
                                ),
                            )
                            utility.save_data("users.json", users)
                            utility.clear_screen()

                        elif pilihan_admin == "4. Logout":
                            print("Logout admin berhasil.")
                            utility.clear_screen()
                            break

        elif pilihan_menu == "2. Register":
            utility.clear_screen_langsung()
            users = utility.load_data("users.json")
            berhasil_daftar = utility.register(users)
            if berhasil_daftar:
                utility.save_data("users.json", users)
            utility.clear_screen()

        elif pilihan_menu == "3. Tentang GloveWorld":
            utility.clear_screen_langsung()
            wahana_list = utility.load_data("wahana.json")
            utility.tentang_gloveworld(wahana_list=wahana_list)
            utility.clear_screen()

        elif pilihan_menu == "4. Exit":
            utility.clear_screen_langsung()
            print("Terimakasih telah menggunakan layanan kami, sampai jumpa lagi!!")
            break
