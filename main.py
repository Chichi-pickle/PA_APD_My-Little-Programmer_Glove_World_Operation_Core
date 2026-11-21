import menu
import utility
import pengguna
import admin
from datetime import datetime
from colorama import Fore, Style
import crud_admin

if __name__ == "__main__":
    WAKTU_MULAI = datetime.now()
    while True:
        pilihan_menu = menu.menu_utama()
        if pilihan_menu == "1. Login":
           users = utility.load_data("users.json")
           user = utility.login(users)
           if user: 
               if user.get("role") == "pengguna":
                        while True:
                            pilihan_pengguna = menu.menu_pengguna()
                            if pilihan_pengguna == "1. Lihat Wahana":
                              utility.tampilkan_wahana(wahana_list = utility.load_data("wahana.json"))
                              utility.clear_screen()
                            elif pilihan_pengguna == "2. Booking Wahana": 
                              wahana_list = utility.load_data("wahana.json")
                              riwayat_list = utility.load_data("history.json")
                              
                              pengguna.booking_wahana(user, wahana_list, riwayat_list, WAKTU_MULAI)
                              
                              utility.save_data("users.json", users)
                              utility.save_data("wahana.json", wahana_list)
                              utility.save_data("history.json", riwayat_list)
                              utility.clear_screen()
                            elif pilihan_pengguna  == "3. Riwayat Booking":
                              wahana_list = utility.load_data("wahana.json")
                              riwayat_list = utility.load_data("history.json")
                              
                              pengguna.riwayat_booking(user, wahana_list, riwayat_list, WAKTU_MULAI)
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
               elif user.get("role") == "admin":
                    while True:
                         pilihan_admin = menu.menu_admin()
                         if pilihan_admin == "1. Manajemen Wahana":
                              while True:
                                   pilihan_CRUD = menu.menu_CRUD()
                                   if pilihan_CRUD == "1. Tambah Wahana":
                                        crud_admin.tambah_wahana()
                                   elif pilihan_CRUD == "2. Edit harga/kapasitas":
                                        crud_admin.ubah_wahana()
                                   elif pilihan_CRUD == "3. Hapus Wahana":
                                        crud_admin.hapus_wahana()
                                   elif pilihan_CRUD == "4. Update Status":
                                        crud_admin.update_status_wahana()
                                   elif pilihan_CRUD == "5. Trafik Wahana":
                                        crud_admin.trafik_wahana()
                                   elif pilihan_CRUD == "6. Kembali":
                                        break
                                   else:
                                        print("Pilihan tidak valid. Silakan coba lagi.")
                         elif pilihan_admin == "2. Grafik Wahana":
                              admin.grafik_wahana_favorit(riwayat_list = utility.load_data("history.json"))
                         elif pilihan_admin == "3. Edit Profile":
                              admin.edit_akun_admin()
                         elif pilihan_admin == "4. Logout":
                              print("Logout")
                              break
                         else:
                              print("Pilihan tidak valid. Silakan coba lagi.") 

        elif pilihan_menu == "2. Register":
            users = utility.load_data("users.json")
            utility.register(users)
            utility.save_data("users.json", users)
            utility.clear_screen()
        elif pilihan_menu == "3. Tentang GloveWorld":
            utility.tentang_gloveworld()
            utility.clear_screen()
        elif pilihan_menu == "4. Exit":
            print("Exiting...")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
