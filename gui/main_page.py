import customtkinter as ctk
from tkinter import messagebox, ttk
from client_api import register, logout
from gui.login_page import LoginPage
from gui.register_page import RegisterPage

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
BORDER = "#e5e7eb"

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.current_info = None
        self.current_info_list = None
        self.current_user = None

        self.title("Hệ thống quản lý thông tin cá nhân an toàn")
        center_window(self, 1180, 720)
        self.resizable(False, False)
        self.configure(fg_color=BG)

        self.build_login_screen()

    # ---------------- LOGIN SCREEN ----------------
    def build_login_screen(self):
        self.clear_window()

        login_page = LoginPage(
            self, 
            on_login_success=self.on_login_success,
            on_register_click=self.build_register_screen
        )
        login_page.pack(fill="both", expand=True)

    def build_register_screen(self):
        self.clear_window()

        register_page = RegisterPage(
            self,
            on_back_click=self.build_login_screen,
            on_register_submit=self.on_register_submit
        )
        register_page.pack(fill="both", expand=True)

    def on_login_success(self, response):
        self.current_user = response.get("user")
        self.current_info = response.get("info")
        self.current_info_list = response.get("info_list")
        self.build_dashboard()  

    def on_register_submit(self, data):
        response = register(data)
        if response["success"]:
            messagebox.showinfo("Thông báo", response["message"])
            self.build_login_screen()
        else:
            messagebox.showerror("Lỗi", response["message"])
    
    # ---------------- DASHBOARD ----------------
    def build_dashboard(self):
        self.clear_window()

        self.topbar = ctk.CTkFrame(self, fg_color=CARD, corner_radius=0, height=70)
        self.topbar.pack(fill="x")

        ctk.CTkLabel(
            self.topbar,
            text="Hệ thống quản lý thông tin cá nhân an toàn",
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

        if self.current_user["role"] == "admin":
            self.build_admin_dashboard()
        else:
            self.build_user_dashboard()

    def build_user_dashboard(self):
        # Căn giữa lời chào
        ctk.CTkLabel(
            self.body,
            text=f"Xin chào, {self.current_info['fullname']}!",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=TEXT
        ).pack(pady=(40, 25))

        # Card thông tin - thu nhỏ chiều rộng và căn giữa
        # Để Card căn giữa chính xác, ta đặt nó vào một khung chứa không giãn
        info_container = ctk.CTkFrame(
            self.body, 
            fg_color=CARD, 
            corner_radius=20, 
            border_width=1, 
            border_color=BORDER,
            width=500,
            height=400
        )
        info_container.pack(pady=10)
        info_container.pack_propagate(False) # Giữ cố định kích thước card

        ctk.CTkLabel(
            info_container,
            text="Thông tin cá nhân",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=PRIMARY
        ).pack(pady=(35, 25))

        info = self.current_info  
        if info:
            fields = [
                ("Họ và tên", info["fullname"]),
                ("Giới tính", info["gender"]),
                ("Email", info["email"]),
                ("Số điện thoại", info["phone"]),
                ("Số CCCD", info["cccd"]),
            ]

            # Container để căn lề nội dung bên trong card
            fields_frame = ctk.CTkFrame(info_container, fg_color="transparent")
            fields_frame.pack(fill="both", expand=True, padx=40)

            for label_text, value_text in fields:
                row = ctk.CTkFrame(fields_frame, fg_color="transparent")
                row.pack(fill="x", pady=6)
                
                ctk.CTkLabel(
                    row, text=f"{label_text}:", 
                    font=ctk.CTkFont(size=14, weight="bold"), 
                    text_color=SECONDARY, width=130, anchor="w"
                ).pack(side="left")
                
                ctk.CTkLabel(
                    row, text=value_text, 
                    font=ctk.CTkFont(size=14), 
                    text_color=TEXT, anchor="w"
                ).pack(side="left", padx=10)
        else:
            ctk.CTkLabel(info_container, text="❌ Lỗi: Không thể tải thông tin.", text_color=DANGER).pack(expand=True)


    def _stat_card(self, parent, title, value, column):
        card = ctk.CTkFrame(parent, fg_color=CARD, corner_radius=20, border_width=1, border_color=BORDER, height=100)
        card.grid(row=0, column=column, padx=10, sticky="ew")
        card.grid_propagate(False)
        
        ctk.CTkLabel(
            card, text=title,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=SUBTEXT
        ).pack(pady=(15, 0))
        
        ctk.CTkLabel(
            card, text=value,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=PRIMARY
        ).pack(pady=(0, 15))



    def build_admin_dashboard(self):
        self.content_card = ctk.CTkFrame(self.body, fg_color="transparent")
        self.content_card.pack(fill="both", expand=True)

        stats_frame = ctk.CTkFrame(self.content_card, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 20))
        stats_frame.columnconfigure(0, weight=1)

        info_list = self.current_info_list or []
        total_users = len(info_list)
        self._stat_card(stats_frame, "👥 Tổng số người dùng hệ thống", str(total_users), 0)

        # 2. Main Data Table Card
        table_container = ctk.CTkFrame(self.content_card, fg_color=CARD, corner_radius=24, border_width=1, border_color=BORDER)
        table_container.pack(fill="both", expand=True)

        header_frame = ctk.CTkFrame(table_container, fg_color="transparent")
        header_frame.pack(fill="x", padx=24, pady=(24, 15))

        title_subframe = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_subframe.pack(side="left")

        ctk.CTkLabel(
            title_subframe,
            text="Danh sách thông tin hệ thống",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=TEXT
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_subframe,
            text="Dữ liệu định dạng ENC:: được mã hóa",
            font=ctk.CTkFont(size=13),
            text_color=SUBTEXT
        ).pack(anchor="w")

        table_wrapper = ctk.CTkFrame(table_container, fg_color="transparent")
        table_wrapper.pack(fill="both", expand=True, padx=24, pady=(0, 24))

        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            rowheight=48,
            font=("Segoe UI", 10),
            background="white",
            fieldbackground="white",
            borderwidth=0,
            selectionbackground=PRIMARY,
            selectionforeground="white"
        )
        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 11, "bold"),
            background="#f8fafc",
            foreground=TEXT,
            relief="flat"
        )
        style.map("Treeview.Heading", background=[('active', '#f1f5f9')])

        columns = ("username", "fullname", "gender", "email", "phone", "cccd")
        self.tree = ttk.Treeview(table_wrapper, columns=columns, show="headings")

        headers = {
            "username": "Tài khoản",
            "fullname": "Họ và tên",
            "gender": "Giới tính",
            "email": "Email (Mã hoá)",
            "phone": "SĐT (Mã hoá)",
            "cccd": "CCCD (Mã hoá)"
        }

        for col, text in headers.items():
            self.tree.heading(col, text=text)
            anchor = "center" if col in ["gender", "username"] else "w"
            self.tree.column(col, anchor=anchor)

        self.tree.column("username", width=120)
        self.tree.column("fullname", width=160)
        self.tree.column("gender", width=100)
        self.tree.column("email", width=200)
        self.tree.column("phone", width=200)
        self.tree.column("cccd", width=200)

        scrollbar = ttk.Scrollbar(table_wrapper, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Load data
        self.load_all_info_into_table()

    def load_all_info_into_table(self):
        info_list = self.current_info_list or []

        for item in self.tree.get_children():
            self.tree.delete(item)

        for info in info_list:
            self.tree.insert("", "end", values=(
                info["username"],
                info["fullname"],
                info["gender"],
                info["email"],
                info["phone"],
                info["cccd"]    
            ))

    def logout(self):
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn đăng xuất không?")
        if confirm:
            response = logout()
            self.current_user = None
            self.current_info = None
            self.current_info_list = None
            if response["success"]:
                self.build_login_screen()
            else:
                messagebox.showerror("Lỗi", response["message"])    

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()
