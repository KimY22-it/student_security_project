
import customtkinter as ctk
from tkinter import messagebox, ttk
from auth import check_login
from student_manager import (
    get_students_for_display,
    add_student_data,
    delete_student_by_code
)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

PRIMARY = "#2563eb"
PRIMARY_HOVER = "#1d4ed8"
SECONDARY = "#475569"
SECONDARY_HOVER = "#334155"
DANGER = "#dc2626"
DANGER_HOVER = "#b91c1c"
NEUTRAL = "#6b7280"
NEUTRAL_HOVER = "#4b5563"
BG = "#f3f6fb"
CARD = "#ffffff"
TEXT = "#111827"
SUBTEXT = "#6b7280"


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def center_child_window(child, parent, width, height):
    parent.update_idletasks()

    parent_x = parent.winfo_x()
    parent_y = parent.winfo_y()
    parent_width = parent.winfo_width()
    parent_height = parent.winfo_height()

    x = parent_x + (parent_width // 2) - (width // 2)
    y = parent_y + (parent_height // 2) - (height // 2)

    child.geometry(f"{width}x{height}+{x}+{y}")

class AddStudentDialog(ctk.CTkToplevel):
    def __init__(self, parent, on_success=None):
        super().__init__(parent)
        self.on_success = on_success

        self.title("Thêm sinh viên")
        center_child_window(self, parent, 520, 560)
        self.resizable(False, False)
        self.configure(fg_color=BG)

        self.build_ui()
        self.lift()
        self.focus()

        self.transient(parent)
        self.grab_set()
        self.attributes("-topmost", True)
        self.after(100, lambda: self.attributes("-topmost", False))

    def build_ui(self):
        card = ctk.CTkFrame(self, fg_color=CARD, corner_radius=18)
        card.pack(fill="both", expand=True, padx=18, pady=18)

        ctk.CTkLabel(
            card, text="Thêm sinh viên",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=TEXT
        ).pack(pady=(20, 8))

        self.student_code = self._entry(card, "Mã sinh viên")
        self.full_name = self._entry(card, "Họ tên")
        self.class_name = self._entry(card, "Lớp")
        self.email = self._entry(card, "Email")
        self.phone = self._entry(card, "Số điện thoại")
        self.cccd = self._entry(card, "CCCD")
        self.address = self._entry(card, "Địa chỉ")

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(pady=18)

        ctk.CTkButton(
            btn_row, text="Lưu",
            width=150, height=42, corner_radius=12,
            fg_color=PRIMARY, hover_color=PRIMARY_HOVER,
            command=self.handle_save
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            btn_row, text="Đóng",
            width=150, height=42, corner_radius=12,
            fg_color=NEUTRAL, hover_color=NEUTRAL_HOVER,
            command=self.destroy
        ).pack(side="left", padx=8)

    def _entry(self, parent, placeholder):
        entry = ctk.CTkEntry(
            parent,
            width=380,
            height=42,
            placeholder_text=placeholder,
            corner_radius=12
        )
        entry.pack(pady=7)
        return entry

    def handle_save(self):
        success, message = add_student_data(
            self.student_code.get(),
            self.full_name.get(),
            self.class_name.get(),
            self.email.get(),
            self.phone.get(),
            self.cccd.get(),
            self.address.get()
        )

        if success:
            messagebox.showinfo("Thông báo", message)
            if self.on_success:
                self.on_success()
            self.destroy()
        else:
            messagebox.showerror("Lỗi", message)


class DeleteStudentDialog(ctk.CTkToplevel):
    def __init__(self, parent, on_success=None):
        super().__init__(parent)
        self.on_success = on_success

        self.title("Xóa sinh viên")
        center_child_window(self, parent, 420, 240)
        self.resizable(False, False)
        self.configure(fg_color=BG)

        self.build_ui()
        self.lift()
        self.focus()

        self.transient(parent)
        self.grab_set()
        self.attributes("-topmost", True)
        self.after(100, lambda: self.attributes("-topmost", False))

    def build_ui(self):
        card = ctk.CTkFrame(self, fg_color=CARD, corner_radius=18)
        card.pack(fill="both", expand=True, padx=18, pady=18)

        ctk.CTkLabel(
            card, text="Xóa sinh viên",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=TEXT
        ).pack(pady=(20, 8))

        ctk.CTkLabel(
            card, text="Nhập mã sinh viên cần xóa",
            font=ctk.CTkFont(size=13),
            text_color=SUBTEXT
        ).pack(pady=(0, 10))

        self.student_code = ctk.CTkEntry(
            card, width=280, height=42,
            placeholder_text="Mã sinh viên",
            corner_radius=12
        )
        self.student_code.pack(pady=10)

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(pady=12)

        ctk.CTkButton(
            btn_row, text="Xóa",
            width=120, height=40, corner_radius=12,
            fg_color=DANGER, hover_color=DANGER_HOVER,
            command=self.handle_delete
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            btn_row, text="Đóng",
            width=120, height=40, corner_radius=12,
            fg_color=NEUTRAL, hover_color=NEUTRAL_HOVER,
            command=self.destroy
        ).pack(side="left", padx=8)

    def handle_delete(self):
        code = self.student_code.get().strip()
        if code == "":
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã sinh viên.")
            return

        success, message = delete_student_by_code(code)
        if success:
            messagebox.showinfo("Thông báo", message)
            if self.on_success:
                self.on_success()
            self.destroy()
        else:
            messagebox.showerror("Lỗi", message)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Hệ thống quản lý sinh viên an toàn")
        center_window(self, 1180, 720)
        self.resizable(False, False)
        self.configure(fg_color=BG)

        self.current_user = None
        self.students_cache = []
        self.show_password = False

        self.build_login_screen()

    # ---------------- LOGIN SCREEN ----------------
    def build_login_screen(self):
        self.clear_window()

        wrapper = ctk.CTkFrame(self, fg_color=BG)
        wrapper.pack(fill="both", expand=True)

        card = ctk.CTkFrame(
            wrapper,
            fg_color=CARD,
            corner_radius=24,
            width=420,
            height=420
        )
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            card,
            text="Hệ thống quản lý\nsinh viên an toàn",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=TEXT,
            justify="center"
        ).place(relx=0.5, y=60, anchor="center")

        ctk.CTkLabel(
            card,
            text="Quản lý thông tin sinh viên với cơ chế mã hóa\nvà che giấu dữ liệu theo phân quyền người dùng.",
            font=ctk.CTkFont(size=13),
            text_color=SUBTEXT,
            justify="center"
        ).place(relx=0.5, y=125, anchor="center")

        self.username_entry = ctk.CTkEntry(
            card,
            width=300,
            height=44,
            placeholder_text="Tên đăng nhập",
            corner_radius=12
        )
        self.username_entry.place(relx=0.5, y=190, anchor="center")

        self.password_entry = ctk.CTkEntry(
            card,
            width=300,
            height=44,
            placeholder_text="Mật khẩu",
            show="*",
            corner_radius=12
        )
        self.password_entry.place(relx=0.5, y=245, anchor="center")

        self.toggle_btn = ctk.CTkButton(
            card,
            text="Hiện",
            width=44,
            height=24,
            corner_radius=8,
            fg_color="transparent",
            hover=False,
            text_color=SUBTEXT,
            command=self.toggle_password
        )
        self.toggle_btn.place(x=300, y=233)

        login_btn = ctk.CTkButton(
            card,
            text="Đăng nhập",
            width=300,
            height=44,
            corner_radius=12,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            command=self.handle_login
        )
        login_btn.place(relx=0.5, y=315, anchor="center")

        ctk.CTkLabel(
            card,
            text="Tài khoản mẫu: admin1 / 123456 | user1 / 123456",
            font=ctk.CTkFont(size=12),
            text_color=SUBTEXT
        ).place(relx=0.5, y=385, anchor="center")

        self.username_entry.bind("<Return>", lambda event: self.handle_login())
        self.password_entry.bind("<Return>", lambda event: self.handle_login())

    def toggle_password(self):
        self.show_password = not self.show_password

        if self.show_password:
            self.password_entry.configure(show="")
            self.toggle_btn.configure(text="Ẩn")
        else:
            self.password_entry.configure(show="*")
            self.toggle_btn.configure(text="Hiện")

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if username == "" or password == "":
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.")
            return

        user = check_login(username, password)
        if user is None:
            messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu.")
            return

        self.current_user = user
        self.build_dashboard()

    # ---------------- DASHBOARD ----------------
    def build_dashboard(self):
        self.clear_window()

        self.topbar = ctk.CTkFrame(self, fg_color=CARD, corner_radius=0, height=70)
        self.topbar.pack(fill="x")

        ctk.CTkLabel(
            self.topbar,
            text="Hệ thống quản lý sinh viên an toàn",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=TEXT
        ).pack(side="left", padx=24, pady=18)

        user_info = f"{self.current_user['username']} ({self.current_user['role']})"
        ctk.CTkLabel(
            self.topbar,
            text=user_info,
            font=ctk.CTkFont(size=14),
            text_color=SUBTEXT
        ).pack(side="right", padx=(0, 16), pady=22)

        logout_btn = ctk.CTkButton(
            self.topbar,
            text="Đăng xuất",
            width=110,
            height=36,
            corner_radius=10,
            fg_color=NEUTRAL,
            hover_color=NEUTRAL_HOVER,
            command=self.logout
        )
        logout_btn.pack(side="right", padx=12, pady=16)

        self.body = ctk.CTkFrame(self, fg_color=BG)
        self.body.pack(fill="both", expand=True, padx=18, pady=18)

        self.action_bar = ctk.CTkFrame(self.body, fg_color="transparent")
        self.action_bar.pack(fill="x", pady=(0, 14))

        ctk.CTkButton(
            self.action_bar,
            text="Xem danh sách sinh viên",
            width=210,
            height=42,
            corner_radius=12,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            command=self.load_students_into_table
        ).pack(side="left", padx=6)

        if self.current_user["role"] == "admin":
            ctk.CTkButton(
                self.action_bar,
                text="Thêm sinh viên",
                width=150,
                height=42,
                corner_radius=12,
                fg_color=SECONDARY,
                hover_color=SECONDARY_HOVER,
                command=self.open_add_student_dialog
            ).pack(side="left", padx=6)

            ctk.CTkButton(
                self.action_bar,
                text="Xóa sinh viên",
                width=150,
                height=42,
                corner_radius=12,
                fg_color=DANGER,
                hover_color=DANGER_HOVER,
                command=self.open_delete_student_dialog
            ).pack(side="left", padx=6)

        self.content_card = ctk.CTkFrame(self.body, fg_color=CARD, corner_radius=18)
        self.content_card.pack(fill="both", expand=True)

        self.build_table_area()

    def build_table_area(self):
        header_frame = ctk.CTkFrame(self.content_card, fg_color="transparent")
        header_frame.pack(fill="x", padx=18, pady=(18, 10))

        ctk.CTkLabel(
            header_frame,
            text="Danh sách sinh viên",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=TEXT
        ).pack(side="left")

        self.search_entry = ctk.CTkEntry(
            header_frame,
            width=260,
            height=40,
            placeholder_text="Tìm theo mã sinh viên hoặc họ tên",
            corner_radius=12
        )
        self.search_entry.pack(side="right", padx=(10, 0))
        self.search_entry.bind("<Return>", lambda event: self.search_students())

        search_btn = ctk.CTkButton(
            header_frame,
            text="Tìm kiếm",
            width=100,
            height=40,
            corner_radius=12,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            command=self.search_students
        )
        search_btn.pack(side="right", padx=6)

        refresh_btn = ctk.CTkButton(
            header_frame,
            text="Làm mới",
            width=100,
            height=40,
            corner_radius=12,
            fg_color=SECONDARY,
            hover_color=SECONDARY_HOVER,
            command=self.load_students_into_table
        )
        refresh_btn.pack(side="right", padx=6)

        table_wrapper = ctk.CTkFrame(self.content_card, fg_color="transparent")
        table_wrapper.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            rowheight=30,
            font=("Segoe UI", 10),
            background="white",
            fieldbackground="white",
            borderwidth=0
        )
        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )

        columns = ("student_code", "full_name", "class_name", "email", "phone", "cccd", "address", "create_at")
        self.tree = ttk.Treeview(table_wrapper, columns=columns, show="headings")

        self.tree.heading("student_code", text="Mã SV")
        self.tree.heading("full_name", text="Họ tên")
        self.tree.heading("class_name", text="Lớp")
        self.tree.heading("email", text="Email")
        self.tree.heading("phone", text="SĐT")
        self.tree.heading("cccd", text="CCCD")
        self.tree.heading("address", text="Địa chỉ")
        self.tree.heading("create_at", text="Ngày tạo")

        self.tree.column("student_code", width=90, anchor="center")
        self.tree.column("full_name", width=150)
        self.tree.column("class_name", width=80, anchor="center")
        self.tree.column("email", width=190)
        self.tree.column("phone", width=110, anchor="center")
        self.tree.column("cccd", width=130, anchor="center")
        self.tree.column("address", width=230)
        self.tree.column("create_at", width=140, anchor="center")

        scrollbar = ttk.Scrollbar(table_wrapper, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_students_into_table(self):
        self.students_cache = get_students_for_display(self.current_user["role"])
        self.render_students(self.students_cache)

    def render_students(self, students):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for student in students:
            self.tree.insert("", "end", values=(
                student["student_code"],
                student["full_name"],
                student["class_name"],
                student["email"],
                student["phone"],
                student["cccd"],
                student["address"],
                student["create_at"]
            ))

    def search_students(self):
        keyword = self.search_entry.get().strip().lower()

        if keyword == "":
            self.render_students(self.students_cache)
            return

        filtered = []
        for student in self.students_cache:
            code = student["student_code"].lower()
            name = student["full_name"].lower()
            if keyword in code or keyword in name:
                filtered.append(student)

        self.render_students(filtered)

    def open_add_student_dialog(self):
        AddStudentDialog(self, on_success=self.load_students_into_table)

    def open_delete_student_dialog(self):
        DeleteStudentDialog(self, on_success=self.load_students_into_table)

    def logout(self):
        self.current_user = None
        self.students_cache = []
        self.build_login_screen()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()