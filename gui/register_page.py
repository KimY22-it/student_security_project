import customtkinter as ctk
from tkinter import messagebox
from validation import validate_registration_input

# Colors matching the login page
PRIMARY = "#2563eb"
PRIMARY_HOVER = "#1d4ed8"
BG = "#f3f6fb"
CARD = "#ffffff"
TEXT = "#111827"
SUBTEXT = "#6b7280"
BORDER = "#e5e7eb"

class RegisterPage(ctk.CTkFrame):
    def __init__(self, master, on_back_click, on_register_submit=None, **kwargs):
        super().__init__(master, fg_color=BG, **kwargs)
        self.on_back_click = on_back_click
        self.on_register_submit = on_register_submit
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
            width=500,
            height=720 # Tăng chiều cao để chứa thêm trường
        )
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        ctk.CTkLabel(
            card,
            text="Đăng ký tài khoản",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=TEXT,
            justify="center"
        ).place(relx=0.5, y=50, anchor="center")

        # Subtitle
        ctk.CTkLabel(
            card,
            text="Vui lòng điền đầy đủ thông tin bên dưới.",
            font=ctk.CTkFont(size=14),
            text_color=SUBTEXT,
            justify="center"
        ).place(relx=0.5, y=100, anchor="center")

        # Form fields container
        form_frame = ctk.CTkFrame(card, fg_color="transparent")
        form_frame.place(relx=0.5, y=360, anchor="center", relwidth=0.8)

        # Fields
        self.username_entry = self.create_input(form_frame, "Tên đăng nhập", 0)
        
        # Password
        self.password_entry = self.create_input(form_frame, "Mật khẩu", 1, show="*")

        # Confirm Password
        self.confirm_password_entry = self.create_input(form_frame, "Xác nhận mật khẩu", 2, show="*")

        # Toggle Button (Place inside Password entry, exactly like Login Page)
        # Tọa độ tương đối để nút nằm đè lên ô Password
        self.toggle_btn = ctk.CTkButton(
            form_frame,
            text="Hiện",
            width=46,
            height=28,
            corner_radius=8,
            fg_color="#f9f9fa",
            hover_color="#f3f4f6",
            text_color=SUBTEXT,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.toggle_password
        )
        # 320 là chiều rộng của entry trong Login, ở đây relwidth=0.8 của 400 (500*0.8) là 400.
        # Chúng ta sẽ đặt nó ở phía bên phải của form_frame
        self.toggle_btn.place(x=320, y=70) # 56 là vị trí y tương ứng với hàng Password

        self.fullname_entry = self.create_input(form_frame, "Họ và tên", 4)
        
        # Gender ComboBox
        gender_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        gender_frame.grid(row=5, column=0, pady=7, sticky="ew")
        gender_frame.columnconfigure(0, weight=1)

        self.gender_combo = ctk.CTkComboBox(
            gender_frame,
            values=["Nam", "Nữ", "Khác"],
            font=ctk.CTkFont(size=14),
            corner_radius=14,
            border_color=BORDER,
            border_width=1,
            height=44,
            state="readonly",
            fg_color="#F8FAFC",          
            button_color="#F8FAFC",      
            dropdown_fg_color="#FFFFFF", 
            dropdown_hover_color="#EAF2FF",
            dropdown_text_color="#1F2937",
            text_color="#111827"
        )
        self.gender_combo.set("Nam")
        self.gender_combo.pack(fill="x", padx=2)

        self.email_entry = self.create_input(form_frame, "Email", 6)
        self.cccd_entry = self.create_input(form_frame, "CCCD", 7)
        self.phone_entry = self.create_input(form_frame, "Số điện thoại", 8)

        form_frame.columnconfigure(0, weight=1)

        # Register Button
        register_btn = ctk.CTkButton(
            card,
            text="Xác nhận đăng ký",
            width=320,
            height=48,
            corner_radius=12,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            command=self.handle_register
        )
        register_btn.place(relx=0.5, y=620, anchor="center")

        # Back prompt
        back_frame = ctk.CTkFrame(card, fg_color="transparent")
        back_frame.place(relx=0.5, y=670, anchor="center")
        
        ctk.CTkLabel(
            back_frame,
            text="Đã có tài khoản?",
            font=ctk.CTkFont(size=13),
            text_color=SUBTEXT
        ).pack(side="left")
        
        ctk.CTkButton(
            back_frame,
            text="Đăng nhập",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=PRIMARY,
            fg_color="transparent",
            hover_color="#f3f4f6",
            width=0,
            height=20,
            command=self.on_back_click
        ).pack(side="left", padx=5)

    def toggle_password(self):
        self.show_password = not self.show_password
        show_char = "" if self.show_password else "*"
        self.password_entry.configure(show=show_char)
        self.confirm_password_entry.configure(show=show_char)
        self.toggle_btn.configure(text="Ẩn" if self.show_password else "Hiện")

    def create_input(self, parent, placeholder, row, show=""):
        entry = ctk.CTkEntry(
            parent,
            height=42,
            placeholder_text=placeholder,
            font=ctk.CTkFont(size=14),
            corner_radius=12,
            border_color=BORDER,
            border_width=1,
            show=show
        )
        entry.grid(row=row, column=0, pady=7, sticky="ew")
        return entry

    def handle_register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        fullname = self.fullname_entry.get().strip()
        gender = self.gender_combo.get()
        email = self.email_entry.get().strip()
        cccd = self.cccd_entry.get().strip()
        phone = self.phone_entry.get().strip()

        if password != confirm_password:
            messagebox.showwarning("Lỗi nhập liệu", "Mật khẩu xác nhận không khớp.")
            return

        # Gọi hàm validation toàn diện
        is_valid, msg = validate_registration_input(
            username, password, fullname, email, cccd, phone
        )

        if not is_valid:
            messagebox.showwarning("Lỗi nhập liệu", msg)
            return

        if self.on_register_submit:
            data = {
                "username": username,
                "password": password,
                "fullname": fullname,
                "gender": gender,
                "email": email,
                "cccd": cccd,
                "phone": phone
            }
            self.on_register_submit(data)
        else:
            # Placeholder action if API is not yet available
            messagebox.showinfo("Thông báo", f"Đăng ký thành công cho {fullname}!\nTính năng liên kết Backend đang được phát triển.")
            self.on_back_click()
