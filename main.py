from auth import login

def show_admin_menu():
    print("\n===== MENU ADMIN =====")
    print("1. Thêm sinh viên")
    print("2. Xem danh sách sinh viên")
    print("3. Xóa sinh viên")
    print("6. Tạo tài khoản")
    print("7. Xem danh sách tài khoản")
    print("8. Xóa tài khoản")
    print("0. Thoát")

def show_user_menu():
    print("\n===== MENU USER =====")
    print("1. Xem danh sách sinh viên")
    print("0. Thoát")

def main():
    current_user = None

    while current_user is None:
        current_user = login()

    while True:
        role = current_user["role"]

        if role == "admin":
            show_admin_menu()
        else:
            show_user_menu()

        choice = input("Chọn chức năng: ")

        if choice == "0":
            print("Thoát chương trình.")
            break

        print("Bạn mới dựng khung menu, bước sau mình sẽ nối từng chức năng.")

if __name__ == "__main__":
    main()