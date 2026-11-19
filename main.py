import utility

if __name__ == "__main__":
    while True:
        pilihan_menu = utility.menu_utama()
        if pilihan_menu == "1. Login":
           print("Login")
        elif pilihan_menu == "2. Register":
            print("Register")
        elif pilihan_menu == "3. Tentang GloveWorld":
            print("Tentang GloveWorld")
        elif pilihan_menu == "4. Exit":
            print("Exiting...")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")