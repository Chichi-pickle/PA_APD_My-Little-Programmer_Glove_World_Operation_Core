import menu
import utility
import pengguna
import admin
import crud_admin
from datetime import datetime

if __name__ == "__main__":
    WAKTU_MULAI = datetime.now()
    while True:
        # [PERUBAHAN] Membersihkan layar di awal setiap putaran menu utama menggunakan clear_screen_langsung().
        # [MEKANISME] Memanggil os.system('cls' / 'clear') secara langsung tanpa menunggu tekan Enter agar tampilan menu tidak menumpuk saat kembali dari sub-menu atau keluar program.
        # [NOTULENSI] Notulensi Konsul 2 (21 Nov 2026) - poin "Clear screen di bagian yang diperlukan".
        utility.clear_screen_langsung()
        pilihan_menu = menu.menu_utama()

        if pilihan_menu == "1. Login":
            users = utility.load_data("users.json")
            user = utility.login(users)
            utility.clear_screen()

            if user:
                if user.get("role") == "pengguna":
                    while True:
                        # [PERUBAHAN] Membersihkan layar sebelum menampilkan menu pengguna.
                        # [MEKANISME] Memanggil clear_screen_langsung() agar menu pengguna tampil bersih di bagian atas terminal.
                        # [NOTULENSI] Notulensi Konsul 2 (21 Nov 2026) - poin "Clear screen di bagian yang diperlukan".
                        utility.clear_screen_langsung()
                        pilihan_pengguna = menu.menu_pengguna()

                        if pilihan_pengguna == "1. Lihat Wahana":
                            utility.tampilkan_wahana(wahana_list=utility.load_data("wahana.json"))
                            utility.clear_screen()

                        elif pilihan_pengguna == "2. Booking Wahana":
                            wahana_list = utility.load_data("wahana.json")
                            riwayat_list = utility.load_data("history.json")

                            pengguna.booking_wahana(user, wahana_list, riwayat_list, WAKTU_MULAI)

                            # [PERUBAHAN] Menyimpan users.json dan history.json (serta mempertahankan wahana.json tetap utuh).
                            # [MEKANISME] Menulis perubahan saldo koin pengguna ke users.json dan data booking baru (serta status riwayat yang ter-update) ke history.json tanpa mengubah kapasitas dasar di wahana.json.
                            # [NOTULENSI] Notulensi Konsul 2 (21 Nov 2026) - poin "Database dan kapasitas dipertahankan" & "sistem booking wahana".
                            utility.save_data("users.json", users)
                            utility.save_data("wahana.json", wahana_list)
                            utility.save_data("history.json", riwayat_list)
                            utility.clear_screen()

                        elif pilihan_pengguna == "3. Riwayat Booking":
                            wahana_list = utility.load_data("wahana.json")
                            riwayat_list = utility.load_data("history.json")

                            pengguna.riwayat_booking(user, wahana_list, riwayat_list, WAKTU_MULAI)

                            # [PERUBAHAN] Menyimpan riwayat_list ke history.json setelah riwayat_booking dijalankan.
                            # [MEKANISME] Jika di dalam riwayat_booking ada transaksi yang statusnya berubah dari 'aktif' menjadi 'tidak aktif' karena melewati tanggal_main, perubahan tersebut langsung tersimpan ke database.
                            # [NOTULENSI] Notulensi Konsul 2 (21 Nov 2026) - poin "apabila datetime now lebih besar daripada tanggal main maka statusnya akan otomatis berubah jadi tidak aktif".
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
                        # [PERUBAHAN] Membersihkan layar sebelum menampilkan menu admin.
                        # [MEKANISME] Memanggil clear_screen_langsung() agar terminal tetap rapi setiap kali kembali ke menu admin.
                        # [NOTULENSI] Notulensi Konsul 2 (21 Nov 2026) - poin "Clear screen di bagian yang diperlukan".
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
                            # [PERUBAHAN] Menyimpan riwayat_list setelah grafik dibuka/diperbarui.
                            # [MEKANISME] Menjaga sinkronisasi data riwayat di history.json jika ada penyesuaian data sebelum digambarkan ke grafik.
                            # [NOTULENSI] Notulensi Konsul 2 (21 Nov 2026) - poin "Batas grafik wahana" & "Database dan kapasitas dipertahankan".
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
            # [PERUBAHAN] Hanya memanggil save_data("users.json", users) jika registrasi tidak dibatalkan.
            # [MEKANISME] 'register()' mengembalikan True jika akun baru ditambahkan dan False jika user memilih batal/keluar, sehingga tidak ada penulisan file mubazir saat batal.
            # [NOTULENSI] Notulensi Konsul 2 (21 Nov 2026) - poin "Keluar menu di register".
            if berhasil_daftar:
                utility.save_data("users.json", users)
            utility.clear_screen()

        elif pilihan_menu == "3. Tentang GloveWorld":
            utility.clear_screen_langsung()
            wahana_list = utility.load_data("wahana.json")
            # [PERUBAHAN] Mengirimkan wahana_list ke utility.tentang_gloveworld() agar tampilan daftar wahana diringkas dulu (3 wahana) dengan opsi baca selengkapnya.
            # [MEKANISME] 'tentang_gloveworld(wahana_list)' menampilkan profil GloveWorld dan 3 wahana ringkas terlebih dahulu, lalu menawarkan pilihan InquirerPy untuk melihat semua wahana atau kembali.
            # [NOTULENSI] Notulensi Konsul 2 (21 Nov 2026) - poin "Ringkas tampilan daftar wahana di bagian tentang gloveworld".
            utility.tentang_gloveworld(wahana_list=wahana_list)
            utility.clear_screen()

        elif pilihan_menu == "4. Exit":
            utility.clear_screen_langsung()
            print("Terimakasih telah menggunakan layanan kami, sampai jumpa lagi!!")
            break