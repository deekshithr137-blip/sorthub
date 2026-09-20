
import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import threading


class SortLab:
    def __init__(self, root):
        self.root = root
        self.root.title("SortLab - Sorting Visualizer")
        self.root.geometry("1200x650")
        self.root.configure(bg="#0F2A43")

        self.array = []
        self.original_array = []
        self.is_sorting = False
        self.speed = 0.08
        self.account_email = ""
        self.account_password = ""
        self.account_name = ""
        self.account_phone = ""
        self.is_logged_in = False

        # Main container
        container = tk.Frame(
            root,
            bg="#0F2A43"
        )
        container.pack(fill="both", expand=True, padx=20, pady=20)

        sidebar = tk.Frame(
            container,
            bg="#102F4D",
            width=200,
            padx=14,
            pady=18
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        sidebar_title = tk.Label(
            sidebar,
            text="Navigation",
            font=("Arial", 14, "bold"),
            bg="#102F4D",
            fg="#EAF3FA"
        )
        sidebar_title.pack(anchor="w", pady=(0, 12))

        self.active_nav = "Home"
        self.nav_buttons = {}
        for label in ["Home", "Profile", "Settings", "Logout"]:
            button = tk.Button(
                sidebar,
                text=label,
                width=18,
                height=2,
                bg="#1A3E63" if label != "Home" else "#FFD166",
                fg="#000000" if label == "Home" else "#EAF3FA",
                font=("Arial", 10, "bold"),
                relief="flat",
                cursor="hand2",
                command=lambda current=label: self.select_nav_item(current)
            )
            button.pack(fill="x", pady=5)
            self.nav_buttons[label] = button

        main_panel = tk.Frame(
            container,
            bg="#15385A",
            padx=20,
            pady=20
        )
        main_panel.pack(side="left", fill="both", expand=True)
        self.main_panel = main_panel

        # =============================================
        # HOME PAGE FRAME (Sorting Visualizer)
        # =============================================
        self.home_frame = tk.Frame(main_panel, bg="#15385A")

        # SortLab logo
        logo_frame = tk.Frame(self.home_frame, bg="#15385A")
        logo_frame.pack(pady=(0, 5))

        logo = tk.Canvas(
            logo_frame,
            width=54,
            height=42,
            bg="#15385A",
            highlightthickness=0
        )
        logo.pack(side="left", padx=(0, 10))
        logo.create_rectangle(4, 25, 13, 38, fill="#FFD166", outline="")
        logo.create_rectangle(18, 17, 27, 38, fill="#EF476F", outline="")
        logo.create_rectangle(32, 7, 41, 38, fill="#5C92C4", outline="")

        logo_text = tk.Label(
            logo_frame,
            text="SORTLAB",
            font=("Arial", 22, "bold"),
            bg="#15385A",
            fg="#EAF3FA"
        )
        logo_text.pack(side="left")

        # Title
        title = tk.Label(
            self.home_frame,
            text="SortLab",
            font=("Arial", 28, "bold"),
            bg="#15385A",
            fg="#EAF3FA"
        )
        title.pack()

        subtitle = tk.Label(
            self.home_frame,
            text="Interactive Sorting Algorithm Visualizer",
            font=("Arial", 14),
            bg="#15385A",
            fg="#EAF3FA"
        )
        subtitle.pack(pady=(0, 15))

        # Controls
        controls = tk.Frame(self.home_frame, bg="#15385A")
        controls.pack(pady=10)

        self.play_button = tk.Button(
            controls,
            text="Play",
            command=self.start_sort,
            bg="#FFD166",
            fg="#000000",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=8,
            relief="flat",
            cursor="hand2"
        )
        self.play_button.grid(row=0, column=0, padx=5)

        self.reset_button = tk.Button(
            controls,
            text="Reset",
            command=self.reset_array,
            font=("Arial", 11),
            padx=15,
            pady=8,
            relief="flat",
            cursor="hand2"
        )
        self.reset_button.grid(row=0, column=1, padx=5)

        new_button = tk.Button(
            controls,
            text="New Array",
            command=self.new_array,
            font=("Arial", 11),
            padx=15,
            pady=8,
            relief="flat",
            cursor="hand2"
        )
        new_button.grid(row=0, column=2, padx=5)

        # Algorithm selection
        tk.Label(
            controls,
            text="Algorithm:",
            bg="#15385A",
            fg="#EAF3FA",
            font=("Arial", 11)
        ).grid(row=0, column=3, padx=(20, 5))

        self.algorithm = ttk.Combobox(
            controls,
            values=[
                "Bubble Sort",
                "Selection Sort",
                "Insertion Sort",
                "Merge Sort",
                "Quick Sort"
            ],
            state="readonly",
            width=18
        )
        self.algorithm.current(0)
        self.algorithm.grid(row=0, column=4, padx=5)

        tk.Label(
            controls,
            text="Data:",
            bg="#15385A",
            fg="#EAF3FA",
            font=("Arial", 11)
        ).grid(row=0, column=5, padx=(20, 5))

        self.data_type = ttk.Combobox(
            controls,
            values=["Numbers", "Letters"],
            state="readonly",
            width=12
        )
        self.data_type.current(0)
        self.data_type.grid(row=0, column=6, padx=5)
        self.data_type.bind("<<ComboboxSelected>>", self.new_array)

        # Speed
        tk.Label(
            controls,
            text="Speed:",
            bg="#15385A",
            fg="#EAF3FA",
            font=("Arial", 11)
        ).grid(row=0, column=7, padx=(20, 5))

        self.speed_scale = tk.Scale(
            controls,
            from_=1,
            to=10,
            orient="horizontal",
            bg="#15385A",
            fg="#EAF3FA",
            highlightthickness=0,
            command=self.change_speed
        )
        self.speed_scale.set(5)
        self.speed_scale.grid(row=0, column=8)

        tk.Label(
            controls,
            text="Custom values:",
            bg="#15385A",
            fg="#EAF3FA",
            font=("Arial", 11)
        ).grid(row=1, column=0, columnspan=2, padx=5, pady=(10, 0), sticky="e")

        self.custom_values = ttk.Entry(controls, width=55)
        self.custom_values.grid(
            row=1,
            column=2,
            columnspan=5,
            padx=5,
            pady=(10, 0),
            sticky="ew"
        )

        apply_button = tk.Button(
            controls,
            text="Use Values",
            command=self.use_custom_values,
            font=("Arial", 11),
            padx=12,
            pady=5,
            relief="flat",
            cursor="hand2"
        )
        apply_button.grid(row=1, column=7, columnspan=2, padx=5, pady=(10, 0))

        # Visualizer
        self.canvas = tk.Canvas(
            self.home_frame,
            height=350,
            bg="#102F4D",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, pady=20)

        # Information
        info_frame = tk.Frame(self.home_frame, bg="#15385A")
        info_frame.pack(fill="x")

        tk.Label(
            info_frame,
            text="Algorithm Information",
            font=("Arial", 15, "bold"),
            bg="#15385A",
            fg="#EAF3FA"
        ).pack()

        self.info_label = tk.Label(
            info_frame,
            text="Bubble Sort: Repeatedly compares adjacent elements and swaps them.",
            font=("Arial", 11),
            bg="#15385A",
            fg="#EAF3FA"
        )
        self.info_label.pack(pady=5)

        self.stats_label = tk.Label(
            info_frame,
            text="Comparisons: 0    Swaps: 0",
            font=("Arial", 11),
            bg="#15385A",
            fg="#FFD166"
        )
        self.stats_label.pack()

        self.algorithm.bind("<<ComboboxSelected>>", self.update_info)

        # =============================================
        # PROFILE PAGE FRAME
        # =============================================
        self.profile_frame = tk.Frame(main_panel, bg="#15385A")
        self.build_profile_page()

        # =============================================
        # SETTINGS PAGE FRAME
        # =============================================
        self.settings_frame = tk.Frame(main_panel, bg="#15385A")
        self.build_settings_page()

        # =============================================
        # Page list for switching
        # =============================================
        self.pages = {
            "Home": self.home_frame,
            "Profile": self.profile_frame,
            "Settings": self.settings_frame,
        }

        # Show Home first
        self.select_nav_item("Home")

        # Create initial array
        self.new_array()

    # -------------------------
    # Page switching
    # -------------------------

    def show_page(self, page_name):
        """Hide all pages and show the selected one."""
        for name, frame in self.pages.items():
            frame.pack_forget()
        if page_name in self.pages:
            self.pages[page_name].pack(fill="both", expand=True)

    def select_nav_item(self, item):
        self.active_nav = item

        for label, button in self.nav_buttons.items():
            if label == item:
                button.config(
                    bg="#FFD166",
                    fg="#000000",
                    font=("Arial", 10, "bold")
                )
            else:
                button.config(
                    bg="#1A3E63",
                    fg="#EAF3FA",
                    font=("Arial", 10, "bold")
                )

        if not hasattr(self, "pages"):
            return

        if item == "Home":
            self.show_page("Home")
        elif item == "Profile":
            self.refresh_profile_page()
            self.show_page("Profile")
        elif item == "Settings":
            self.show_page("Settings")
        elif item == "Logout":
            confirm = messagebox.askyesno(
                "Confirm Logout",
                "Are you sure you want to logout?"
            )
            if confirm:
                self.is_logged_in = False
                self.root.withdraw()
                self.open_login_page(first_page=True)

    # -------------------------
    # Profile Page
    # -------------------------

    def build_profile_page(self):
        """Build the profile page with signup details."""
        # Title
        tk.Label(
            self.profile_frame,
            text="My Profile",
            font=("Arial", 26, "bold"),
            bg="#15385A",
            fg="#EAF3FA"
        ).pack(pady=(30, 5))

        tk.Label(
            self.profile_frame,
            text="Your account details from signup",
            font=("Arial", 11),
            bg="#15385A",
            fg="#8BAEC7"
        ).pack(pady=(0, 25))

        # Profile card
        card = tk.Frame(self.profile_frame, bg="#102F4D", padx=40, pady=30)
        card.pack(padx=80, pady=10, fill="x")

        # Avatar with initials
        self.profile_avatar = tk.Canvas(
            card, width=80, height=80,
            bg="#102F4D", highlightthickness=0
        )
        self.profile_avatar.pack(pady=(0, 10))

        # Name
        self.profile_name_label = tk.Label(
            card, text="", font=("Arial", 20, "bold"),
            bg="#102F4D", fg="#EAF3FA"
        )
        self.profile_name_label.pack(pady=(0, 3))

        # Status badge
        self.profile_status_label = tk.Label(
            card, text="", font=("Arial", 10, "bold"),
            bg="#102F4D"
        )
        self.profile_status_label.pack(pady=(0, 20))

        # Separator
        sep = tk.Frame(card, bg="#2A5E8F", height=1)
        sep.pack(fill="x", pady=(0, 20))

        # Detail rows
        details_frame = tk.Frame(card, bg="#102F4D")
        details_frame.pack(fill="x")

        self.profile_detail_labels = {}
        detail_items = [
            ("Email", "email_icon"),
            ("Phone", "phone_icon"),
            ("Password", "lock_icon"),
        ]

        for i, (label_text, icon_key) in enumerate(detail_items):
            row = tk.Frame(details_frame, bg="#102F4D")
            row.pack(fill="x", pady=8)

            tk.Label(
                row, text=f"  {label_text}:",
                font=("Arial", 12, "bold"),
                bg="#102F4D", fg="#8BAEC7",
                width=14, anchor="w"
            ).pack(side="left", padx=(20, 10))

            value_label = tk.Label(
                row, text="",
                font=("Arial", 12),
                bg="#102F4D", fg="#EAF3FA",
                anchor="w"
            )
            value_label.pack(side="left", fill="x", expand=True)
            self.profile_detail_labels[label_text] = value_label

    def refresh_profile_page(self):
        """Update profile page with current account data."""
        # Update avatar
        self.profile_avatar.delete("all")
        initials = "?"
        if self.account_name:
            parts = self.account_name.split()
            initials = "".join(p[0].upper() for p in parts[:2])
        self.profile_avatar.create_oval(5, 5, 75, 75, fill="#FFD166", outline="")
        self.profile_avatar.create_text(
            40, 40, text=initials,
            fill="#0F2A43", font=("Arial", 24, "bold")
        )

        # Update name
        name = self.account_name or "Not available"
        self.profile_name_label.config(text=name)

        # Update status
        if self.is_logged_in:
            self.profile_status_label.config(text="Logged In", fg="#06D6A0")
        else:
            self.profile_status_label.config(text="Not Logged In", fg="#EF476F")

        # Update details
        email = self.account_email or "Not available"
        phone = self.account_phone or "Not provided"
        password_masked = "*" * min(len(self.account_password), 10) if self.account_password else "Not available"

        self.profile_detail_labels["Email"].config(text=email)
        self.profile_detail_labels["Phone"].config(text=phone)
        self.profile_detail_labels["Password"].config(text=password_masked)

    # -------------------------
    # Settings Page
    # -------------------------

    def build_settings_page(self):
        """Build the settings page with configurable options."""
        # Title
        tk.Label(
            self.settings_frame,
            text="Settings",
            font=("Arial", 26, "bold"),
            bg="#15385A",
            fg="#EAF3FA"
        ).pack(pady=(30, 5))

        tk.Label(
            self.settings_frame,
            text="Customize your SortLab experience",
            font=("Arial", 11),
            bg="#15385A",
            fg="#8BAEC7"
        ).pack(pady=(0, 25))

        # Settings card
        card = tk.Frame(self.settings_frame, bg="#102F4D", padx=40, pady=25)
        card.pack(padx=80, pady=10, fill="x")

        # --- Theme setting ---
        row1 = tk.Frame(card, bg="#102F4D")
        row1.pack(fill="x", pady=10)

        tk.Label(
            row1, text="Theme",
            font=("Arial", 13, "bold"),
            bg="#102F4D", fg="#EAF3FA"
        ).pack(anchor="w")
        tk.Label(
            row1, text="Choose the app color theme",
            font=("Arial", 9),
            bg="#102F4D", fg="#8BAEC7"
        ).pack(anchor="w", pady=(0, 6))

        self.theme_var = tk.StringVar(value="Dark Blue")
        theme_menu = ttk.Combobox(
            row1,
            textvariable=self.theme_var,
            values=["Dark Blue", "Midnight", "Ocean", "Slate"],
            state="readonly", width=20
        )
        theme_menu.pack(anchor="w")
        theme_menu.bind("<<ComboboxSelected>>", self.apply_theme)

        # Separator
        tk.Frame(card, bg="#2A5E8F", height=1).pack(fill="x", pady=12)

        # --- Default array size ---
        row2 = tk.Frame(card, bg="#102F4D")
        row2.pack(fill="x", pady=10)

        tk.Label(
            row2, text="Default Array Size",
            font=("Arial", 13, "bold"),
            bg="#102F4D", fg="#EAF3FA"
        ).pack(anchor="w")
        tk.Label(
            row2, text="Number of elements generated for new arrays",
            font=("Arial", 9),
            bg="#102F4D", fg="#8BAEC7"
        ).pack(anchor="w", pady=(0, 6))

        size_frame = tk.Frame(row2, bg="#102F4D")
        size_frame.pack(anchor="w")

        self.array_size_var = tk.IntVar(value=30)
        self.array_size_scale = tk.Scale(
            size_frame,
            from_=5, to=60,
            orient="horizontal",
            variable=self.array_size_var,
            bg="#102F4D", fg="#EAF3FA",
            highlightthickness=0, length=200,
            troughcolor="#1A3E63"
        )
        self.array_size_scale.pack(side="left")

        self.size_display = tk.Label(
            size_frame, text="30",
            font=("Arial", 12, "bold"),
            bg="#102F4D", fg="#FFD166", width=4
        )
        self.size_display.pack(side="left", padx=10)
        self.array_size_scale.config(command=self.update_size_display)

        # Separator
        tk.Frame(card, bg="#2A5E8F", height=1).pack(fill="x", pady=12)

        # --- Default algorithm ---
        row3 = tk.Frame(card, bg="#102F4D")
        row3.pack(fill="x", pady=10)

        tk.Label(
            row3, text="Default Algorithm",
            font=("Arial", 13, "bold"),
            bg="#102F4D", fg="#EAF3FA"
        ).pack(anchor="w")
        tk.Label(
            row3, text="Algorithm selected when the app starts",
            font=("Arial", 9),
            bg="#102F4D", fg="#8BAEC7"
        ).pack(anchor="w", pady=(0, 6))

        self.default_algo_var = tk.StringVar(value="Bubble Sort")
        algo_menu = ttk.Combobox(
            row3,
            textvariable=self.default_algo_var,
            values=["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort"],
            state="readonly", width=20
        )
        algo_menu.pack(anchor="w")

        # Separator
        tk.Frame(card, bg="#2A5E8F", height=1).pack(fill="x", pady=12)

        # --- Sound toggle ---
        row4 = tk.Frame(card, bg="#102F4D")
        row4.pack(fill="x", pady=10)

        tk.Label(
            row4, text="Sound Effects",
            font=("Arial", 13, "bold"),
            bg="#102F4D", fg="#EAF3FA"
        ).pack(anchor="w")
        tk.Label(
            row4, text="Play sounds during sorting animations",
            font=("Arial", 9),
            bg="#102F4D", fg="#8BAEC7"
        ).pack(anchor="w", pady=(0, 6))

        self.sound_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            row4, text="Enable sound",
            variable=self.sound_var,
            bg="#102F4D", fg="#EAF3FA",
            activebackground="#102F4D",
            activeforeground="#EAF3FA",
            selectcolor="#1A3E63",
            font=("Arial", 10)
        ).pack(anchor="w")

        # Apply button
        tk.Button(
            self.settings_frame,
            text="Apply Settings",
            command=self.apply_settings,
            bg="#FFD166", fg="#000000",
            font=("Arial", 12, "bold"),
            padx=25, pady=8,
            relief="flat", cursor="hand2"
        ).pack(pady=20)

        # About section
        about_frame = tk.Frame(self.settings_frame, bg="#102F4D", padx=30, pady=15)
        about_frame.pack(padx=80, fill="x")

        tk.Label(
            about_frame, text="About SortLab",
            font=("Arial", 13, "bold"),
            bg="#102F4D", fg="#EAF3FA"
        ).pack(anchor="w")
        tk.Label(
            about_frame,
            text="SortLab v1.0 — Interactive Sorting Algorithm Visualizer\nBuilt with Python & Tkinter",
            font=("Arial", 9),
            bg="#102F4D", fg="#8BAEC7",
            justify="left"
        ).pack(anchor="w", pady=(4, 0))

    def update_size_display(self, value):
        self.size_display.config(text=str(int(float(value))))

    def apply_settings(self):
        """Apply settings to the app."""
        # Apply default algorithm
        algo = self.default_algo_var.get()
        algo_list = ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort"]
        if algo in algo_list:
            self.algorithm.current(algo_list.index(algo))
            self.update_info()

        messagebox.showinfo("Settings", "Settings applied successfully!")

    def apply_theme(self, event=None):
        """Apply the selected color theme."""
        themes = {
            "Dark Blue":  {"bg": "#0F2A43", "panel": "#15385A", "sidebar": "#102F4D", "card": "#102F4D"},
            "Midnight":   {"bg": "#0D1B2A", "panel": "#1B2838", "sidebar": "#0D1B2A", "card": "#1B2838"},
            "Ocean":      {"bg": "#0A2E3C", "panel": "#133A4B", "sidebar": "#0A2E3C", "card": "#133A4B"},
            "Slate":      {"bg": "#1A1A2E", "panel": "#16213E", "sidebar": "#1A1A2E", "card": "#16213E"},
        }
        theme = themes.get(self.theme_var.get(), themes["Dark Blue"])
        self.root.configure(bg=theme["bg"])

    # -------------------------
    # Array functions
    # -------------------------

    def open_signup_page(self, first_page=False):
        signup_window = tk.Toplevel(self.root)
        signup_window.title("SortLab - Sign Up")
        signup_window.geometry("430x400")
        signup_window.configure(bg="#15385A")
        signup_window.resizable(False, False)

        if first_page:
            signup_window.protocol("WM_DELETE_WINDOW", self.root.destroy)

        tk.Label(
            signup_window,
            text="Create your SortLab account",
            font=("Arial", 20, "bold"),
            bg="#15385A",
            fg="#EAF3FA"
        ).pack(pady=(25, 5))

        tk.Label(
            signup_window,
            text="Save your sorting preferences and continue learning.",
            font=("Arial", 10),
            bg="#15385A",
            fg="#EAF3FA"
        ).pack(pady=(0, 18))

        form = tk.Frame(signup_window, bg="#15385A")
        form.pack(fill="x", padx=45)

        def toggle_password(field, button):
            if field.cget("show") == "*":
                field.config(show="")
                button.config(text="Hide")
            else:
                field.config(show="*")
                button.config(text="Show")

        fields = {}
        field_names = [
            ("Email", ""),
            ("Phone number (optional)", ""),
            ("Password", "*"),
            ("Confirm password", "*")
        ]

        for row, (label_text, mask) in enumerate(field_names):
            tk.Label(
                form,
                text=label_text,
                font=("Arial", 10, "bold"),
                bg="#15385A",
                fg="#EAF3FA"
            ).grid(row=row, column=0, sticky="w", pady=(0, 4))

            field = tk.Entry(
                form,
                width=25,
                show=mask,
                font=("Arial", 10)
            )
            field.grid(row=row, column=1, pady=(0, 10), padx=(12, 0))
            fields[label_text] = field

            if mask:
                eye_button = tk.Button(
                    form,
                    text="Show",
                    width=6,
                    font=("Arial", 8),
                    relief="flat",
                    cursor="hand2"
                )
                eye_button.grid(row=row, column=2, padx=(5, 0), pady=(0, 10))
                eye_button.config(
                    command=lambda current_field=field, current_button=eye_button:
                    toggle_password(current_field, current_button)
                )

        terms = tk.BooleanVar(value=False)
        tk.Checkbutton(
            form,
            text="I agree to the Terms & Conditions",
            variable=terms,
            bg="#15385A",
            fg="#EAF3FA",
            activebackground="#15385A",
            activeforeground="#EAF3FA",
            selectcolor="#102F4D",
            font=("Arial", 9)
        ).grid(row=len(field_names), column=0, columnspan=2, sticky="w", pady=(2, 14))

        def create_account():
            email = fields["Email"].get().strip()
            password = fields["Password"].get()
            confirm_password = fields["Confirm password"].get()

            if not email or not password or not confirm_password:
                messagebox.showerror(
                    "Missing information",
                    "Please complete your email and password fields.",
                    parent=signup_window
                )
                return

            if "@" not in email or "." not in email.split("@")[-1]:
                messagebox.showerror(
                    "Invalid email",
                    "Please enter a valid email address.",
                    parent=signup_window
                )
                return

            if len(password) < 6:
                messagebox.showerror(
                    "Password too short",
                    "Password must contain at least 6 characters.",
                    parent=signup_window
                )
                return

            if password != confirm_password:
                messagebox.showerror(
                    "Passwords do not match",
                    "Please enter the same password twice.",
                    parent=signup_window
                )
                return

            if not terms.get():
                messagebox.showerror(
                    "Terms required",
                    "Please agree to the Terms & Conditions.",
                    parent=signup_window
                )
                return

            self.account_name = email.split("@")[0]
            self.account_email = email
            self.account_phone = fields["Phone number (optional)"].get().strip()
            self.account_password = password

            messagebox.showinfo(
                "Account created",
                f"Welcome to SortLab!",
                parent=signup_window
            )
            signup_window.destroy()
            self.open_login_page(first_page=first_page)

        tk.Button(
            signup_window,
            text="Create Account",
            command=create_account,
            bg="#FFD166",
            fg="#000000",
            font=("Arial", 11, "bold"),
            padx=18,
            pady=8,
            relief="flat",
            cursor="hand2"
        ).pack(pady=8)

    def open_login_page(self, first_page=False):
        login_window = tk.Toplevel(self.root)
        login_window.title("SortLab - Login")
        login_window.geometry("400x380")
        login_window.configure(bg="#15385A")
        login_window.resizable(False, False)

        if first_page:
            login_window.protocol("WM_DELETE_WINDOW", self.root.destroy)

        # Sign Up link at the top
        signup_bar = tk.Frame(login_window, bg="#102F4D")
        signup_bar.pack(fill="x", padx=0, pady=0)

        tk.Label(
            signup_bar,
            text="Don't have an account?",
            font=("Arial", 9),
            bg="#102F4D",
            fg="#8BAEC7"
        ).pack(side="left", padx=(15, 5), pady=8)

        tk.Button(
            signup_bar,
            text="Sign Up",
            font=("Arial", 9, "bold"),
            bg="#FFD166",
            fg="#000000",
            relief="flat",
            cursor="hand2",
            padx=10,
            command=lambda: [login_window.destroy(), self.open_signup_page(first_page=first_page)]
        ).pack(side="left", pady=8)

        tk.Label(
            login_window,
            text="Welcome back",
            font=("Arial", 22, "bold"),
            bg="#15385A",
            fg="#EAF3FA"
        ).pack(pady=(20, 6))

        tk.Label(
            login_window,
            text="Log in to open SortLab",
            font=("Arial", 10),
            bg="#15385A",
            fg="#EAF3FA"
        ).pack(pady=(0, 22))

        form = tk.Frame(login_window, bg="#15385A")
        form.pack()

        tk.Label(
            form,
            text="Email",
            font=("Arial", 10, "bold"),
            bg="#15385A",
            fg="#EAF3FA"
        ).grid(row=0, column=0, sticky="w", pady=(0, 6))

        email_field = tk.Entry(form, width=30, font=("Arial", 10))
        email_field.grid(row=0, column=1, padx=(15, 0), pady=(0, 10))

        tk.Label(
            form,
            text="Password",
            font=("Arial", 10, "bold"),
            bg="#15385A",
            fg="#EAF3FA"
        ).grid(row=1, column=0, sticky="w", pady=(0, 6))

        password_field = tk.Entry(
            form,
            width=24,
            show="*",
            font=("Arial", 10)
        )
        password_field.grid(row=1, column=1, padx=(15, 0), pady=(0, 16))

        def toggle_login_password():
            if password_field.cget("show") == "*":
                password_field.config(show="")
                eye_button.config(text="Hide")
            else:
                password_field.config(show="*")
                eye_button.config(text="Show")

        eye_button = tk.Button(
            form,
            text="Show",
            command=toggle_login_password,
            width=6,
            font=("Arial", 8),
            relief="flat",
            cursor="hand2"
        )
        eye_button.grid(row=1, column=2, padx=(5, 0), pady=(0, 16))

        def login():
            email = email_field.get().strip()
            password = password_field.get()

            if not email or not password:
                messagebox.showerror(
                    "Missing information",
                    "Please enter your email and password.",
                    parent=login_window
                )
                return

            if not self.account_email:
                messagebox.showerror(
                    "No account found",
                    "No account exists yet. Please sign up first.",
                    parent=login_window
                )
                return

            if email != self.account_email:
                messagebox.showerror(
                    "Login failed",
                    "This email is not registered. Please sign up first.",
                    parent=login_window
                )
                return

            if password != self.account_password:
                messagebox.showerror(
                    "Login failed",
                    "Incorrect password. Please try again.",
                    parent=login_window
                )
                return

            self.is_logged_in = True
            login_window.destroy()
            self.root.deiconify()

        tk.Button(
            login_window,
            text="Login",
            command=login,
            bg="#FFD166",
            fg="#000000",
            font=("Arial", 11, "bold"),
            padx=25,
            pady=8,
            relief="flat",
            cursor="hand2"
        ).pack(pady=4)

        email_field.focus_set()

    def new_array(self, event=None):
        if self.is_sorting:
            return

        if self.data_type.get() == "Letters":
            self.array = random.sample(
                list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
                20
            )
        else:
            self.array = [
                random.randint(10, 100)
                for _ in range(30)
            ]

        self.original_array = self.array.copy()
        self.comparisons = 0
        self.swaps = 0

        self.draw_array()

    def use_custom_values(self):
        if self.is_sorting:
            return

        raw_values = self.custom_values.get().replace(",", " ").split()

        if not raw_values:
            messagebox.showerror(
                "Missing values",
                "Enter numbers or letters separated by spaces or commas."
            )
            return

        if self.data_type.get() == "Letters":
            values = [value.upper() for value in raw_values]

            if any(len(value) != 1 or not value.isalpha() for value in values):
                messagebox.showerror(
                    "Invalid letters",
                    "Enter single letters, such as A, D, B, C."
                )
                return
        else:
            try:
                values = [int(value) for value in raw_values]
            except ValueError:
                messagebox.showerror(
                    "Invalid numbers",
                    "Enter whole numbers, such as 42, 7, 19."
                )
                return

        self.array = values
        self.original_array = self.array.copy()
        self.comparisons = 0
        self.swaps = 0
        self.custom_values.delete(0, tk.END)
        self.custom_values.insert(0, ", ".join(map(str, values)))
        self.draw_array()

    def reset_array(self):
        if self.is_sorting:
            return

        self.array = self.original_array.copy()
        self.comparisons = 0
        self.swaps = 0

        self.custom_values.delete(0, tk.END)
        self.custom_values.insert(
            0,
            ", ".join(map(str, self.array))
        )

        self.draw_array()

    # -------------------------
    # Drawing
    # -------------------------

    def draw_array(self, active=None, minimum=None):
        self.canvas.delete("all")

        if not self.array:
            return

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width <= 1:
            width = 1100

        bar_width = width / len(self.array)

        for i, value in enumerate(self.array):
            x1 = i * bar_width + 2
            x2 = (i + 1) * bar_width - 2

            if isinstance(value, str):
                visual_value = ord(value) - ord("A") + 1
                bar_height = (visual_value / 26) * (height - 30)
            else:
                bar_height = (value / 100) * (height - 30)

            y1 = height - bar_height
            y2 = height

            color = "#5C92C4"

            if active and i in active:
                color = "#FFD166"

            if minimum is not None and i == minimum:
                color = "#EF476F"

            self.canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                outline=""
            )

            self.canvas.create_text(
                (x1 + x2) / 2,
                max(y1 - 10, 12),
                text=str(value),
                fill="#EAF3FA",
                font=("Arial", 8, "bold")
            )

    def update_display(self, active=None, minimum=None):
        self.draw_array(active, minimum)

        self.stats_label.config(
            text=f"Comparisons: {self.comparisons}    "
                 f"Swaps: {self.swaps}"
        )

        self.root.update()

        time.sleep(self.speed)

    # -------------------------
    # Speed
    # -------------------------

    def change_speed(self, value):
        level = int(float(value))

        # Higher value = faster
        self.speed = 0.20 - (level * 0.018)

    # -------------------------
    # Start sorting
    # -------------------------

    def start_sort(self):
        if self.is_sorting:
            return

        self.is_sorting = True
        self.play_button.config(state="disabled")
        self.reset_button.config(state="disabled")

        thread = threading.Thread(
            target=self.sort_array,
            daemon=True
        )
        thread.start()

    def sort_array(self):
        algorithm = self.algorithm.get()

        self.comparisons = 0
        self.swaps = 0

        if algorithm == "Bubble Sort":
            self.bubble_sort()

        elif algorithm == "Selection Sort":
            self.selection_sort()

        elif algorithm == "Insertion Sort":
            self.insertion_sort()

        elif algorithm == "Merge Sort":
            self.merge_sort(0, len(self.array) - 1)

        elif algorithm == "Quick Sort":
            self.quick_sort(0, len(self.array) - 1)

        self.draw_array()

        self.is_sorting = False
        self.root.after(
            0,
            self.finish_sorting
        )

    def finish_sorting(self):
        self.play_button.config(state="normal")
        self.reset_button.config(state="normal")

    # -------------------------
    # Bubble Sort
    # -------------------------

    def bubble_sort(self):
        n = len(self.array)

        for i in range(n):
            for j in range(0, n - i - 1):

                self.comparisons += 1
                self.update_display(active=[j, j + 1])

                if self.array[j] > self.array[j + 1]:
                    self.array[j], self.array[j + 1] = (
                        self.array[j + 1],
                        self.array[j]
                    )

                    self.swaps += 1
                    self.update_display(active=[j, j + 1])

    # -------------------------
    # Selection Sort
    # -------------------------

    def selection_sort(self):
        n = len(self.array)

        for i in range(n):
            minimum = i

            for j in range(i + 1, n):

                self.comparisons += 1
                self.update_display(
                    active=[j],
                    minimum=minimum
                )

                if self.array[j] < self.array[minimum]:
                    minimum = j

            if minimum != i:
                self.array[i], self.array[minimum] = (
                    self.array[minimum],
                    self.array[i]
                )

                self.swaps += 1

                self.update_display(
                    active=[i, minimum]
                )

    # -------------------------
    # Insertion Sort
    # -------------------------

    def insertion_sort(self):
        n = len(self.array)

        for i in range(1, n):
            key = self.array[i]
            j = i - 1

            while j >= 0:

                self.comparisons += 1
                self.update_display(active=[j, j + 1])

                if self.array[j] > key:
                    self.array[j + 1] = self.array[j]
                    self.swaps += 1
                    j -= 1

                    self.update_display(active=[j + 1])
                else:
                    break

            self.array[j + 1] = key
            self.update_display(active=[j + 1])

    # -------------------------
    # Merge Sort
    # -------------------------

    def merge_sort(self, left, right):
        if left >= right:
            return

        middle = (left + right) // 2

        self.merge_sort(left, middle)
        self.merge_sort(middle + 1, right)

        self.merge(left, middle, right)

    def merge(self, left, middle, right):

        left_part = self.array[left:middle + 1]
        right_part = self.array[middle + 1:right + 1]

        i = 0
        j = 0
        k = left

        while i < len(left_part) and j < len(right_part):

            self.comparisons += 1
            self.update_display(active=[k])

            if left_part[i] <= right_part[j]:
                self.array[k] = left_part[i]
                i += 1
            else:
                self.array[k] = right_part[j]
                j += 1

            self.swaps += 1
            k += 1

        while i < len(left_part):
            self.array[k] = left_part[i]
            i += 1
            k += 1

            self.update_display(active=[k - 1])

        while j < len(right_part):
            self.array[k] = right_part[j]
            j += 1
            k += 1

            self.update_display(active=[k - 1])

    # -------------------------
    # Quick Sort
    # -------------------------

    def quick_sort(self, low, high):
        if low < high:

            pivot_index = self.partition(low, high)

            self.quick_sort(low, pivot_index - 1)
            self.quick_sort(pivot_index + 1, high)

    def partition(self, low, high):

        pivot = self.array[high]
        i = low - 1

        for j in range(low, high):

            self.comparisons += 1
            self.update_display(active=[j, high])

            if self.array[j] < pivot:
                i += 1

                self.array[i], self.array[j] = (
                    self.array[j],
                    self.array[i]
                )

                self.swaps += 1
                self.update_display(active=[i, j])

        self.array[i + 1], self.array[high] = (
            self.array[high],
            self.array[i + 1]
        )

        self.swaps += 1
        self.update_display(active=[i + 1, high])

        return i + 1

    # -------------------------
    # Information
    # -------------------------

    def update_info(self, event=None):

        algorithm = self.algorithm.get()

        descriptions = {
            "Bubble Sort":
                "Bubble Sort: Repeatedly compares adjacent elements and swaps them.",

            "Selection Sort":
                "Selection Sort: Finds the smallest element and places it at the beginning.",

            "Insertion Sort":
                "Insertion Sort: Builds the sorted array one element at a time.",

            "Merge Sort":
                "Merge Sort: Divides the array and merges sorted sections.",

            "Quick Sort":
                "Quick Sort: Uses a pivot to divide the array into smaller sections."
        }

        self.info_label.config(
            text=descriptions[algorithm]
        )


# -------------------------
# Run application
# -------------------------

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = SortLab(root)
    app.open_login_page(first_page=True)
    root.mainloop()