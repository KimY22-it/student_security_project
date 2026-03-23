from auth import login
from student_manager import add_student, view_students, delete_student

def show_admin_menu():
    print("\n===== MENU ADMIN =====")
    print("1. Thêm sinh viên")
    print("2. Xem danh sách sinh viên")
    print("3. Xóa sinh viên")
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

        if role == "admin":
            if choice == "1":
                add_student()
            elif choice == "2":
                view_students(role)
            elif choice == "3":
                delete_student()
            elif choice == "0":
                print("Thoát chương trình.")
                break
            else:
                print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
        else:
            if choice == "1":
                view_students(role)
            elif choice == "0":
                print("Thoát chương trình.")
                break
            else:
                print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
        
if __name__ == "__main__":
    main()