import customtkinter as ctk
from tkinter import messagebox
from client_api import login

# Colors
PRIMARY = "#2563eb"
PRIMARY_HOVER = "#1d4ed8"
BG = "#f3f6fb"
CARD = "#ffffff"
TEXT = "#111827"
SUBTEXT = "#6b7280"
BORDER = "#e5e7eb"

class LoginPage(ctk.CTkFrame):
    def __init__(self, master, on_login_success, on_register_click=None, **kwargs):
        super().__init__(master, fg_color=BG, **kwargs)
        self.on_login_success = on_login_success
        self.on_register_click = on_register_click
        self.show_password = False

        self.build_ui()

    def build_ui(self):
        # Center card
        card = ctk.CTkFrame(
            self,
            fg_color=CARD,
            corner_radius=24,
            border_width=1,
            border_color=BORDER,
            width=460,
            height=480
        )
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        ctk.CTkLabel(
            card,
            text="Hệ thống quản lý\nthông tin cá nhân an toàn",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=TEXT,
            justify="center"
        ).place(relx=0.5, y=70, anchor="center")

        # Subtitle
        ctk.CTkLabel(
            card,
            text="Đăng nhập để vào hệ thống quản lý dữ liệu an toàn.",
            font=ctk.CTkFont(size=14),
            text_color=SUBTEXT,
            justify="center"
        ).place(relx=0.5, y=140, anchor="center")

        # Username Field
        self.username_entry = ctk.CTkEntry(
            card,
            width=320,
            height=48,
            placeholder_text="Tên đăng nhập",
            font=ctk.CTkFont(size=14),
            corner_radius=12,
            border_color=BORDER,
            border_width=1
        )
        self.username_entry.place(relx=0.5, y=210, anchor="center")

        # Password Field
        self.password_entry = ctk.CTkEntry(
            card,
            width=320,
            height=48,
            placeholder_text="Mật khẩu",
            show="*",
            font=ctk.CTkFont(size=14),
            corner_radius=12,
            border_color=BORDER,
            border_width=1
        )
        self.password_entry.place(relx=0.5, y=275, anchor="center")

        # Toggle password visibility button
        self.toggle_btn = ctk.CTkButton(
            card,
            text="Hiện",
            width=48,
            height=28,
            corner_radius=8,
            fg_color="#f9f9fa",
            hover_color="#f3f4f6",
            text_color=SUBTEXT,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.toggle_password
        )
        # Positioned inside the password entry
        self.toggle_btn.place(x=310, y=261)

        # Login Button
        login_btn = ctk.CTkButton(
            card,
            text="Đăng nhập",
            width=320,
            height=48,
            corner_radius=12,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            command=self.handle_login
        )
        login_btn.place(relx=0.5, y=355, anchor="center")

        # Register prompt
        register_frame = ctk.CTkFrame(card, fg_color="transparent")
        register_frame.place(relx=0.5, y=410, anchor="center")
        
        ctk.CTkLabel(
            register_frame,
            text="Bạn chưa có tài khoản?",
            font=ctk.CTkFont(size=13),
            text_color=SUBTEXT
        ).pack(side="left")
        
        ctk.CTkButton(
            register_frame,
            text="Đăng ký ngay",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=PRIMARY,
            fg_color="transparent",
            hover_color="#f3f4f6",
            width=0,
            height=20,
            command=self.handle_register_click
        ).pack(side="left", padx=5)

        # Footer text
        ctk.CTkLabel(
            card,
            text="© 2026 Information Security Project",
            font=ctk.CTkFont(size=12),
            text_color="#9ca3af",
        ).place(relx=0.5, y=450, anchor="center")

        # Bind enter key
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

        if not username or not password:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.")
            return

        # Vô hiệu hóa nút trong lúc đăng nhập
        response = login(username, password)

        if not response["success"]:
            messagebox.showerror("Lỗi", response["message"])
            return

        # Gọi callback và truyền user info sang Main App
        if self.on_login_success:
            self.on_login_success(response)

    def handle_register_click(self):
        if self.on_register_click:
            self.on_register_click()
