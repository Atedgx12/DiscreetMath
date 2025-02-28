import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math
import cmath
import logging
import os
import ctypes  # Required for setting the taskbar icon on Windows
from PIL import Image, ImageTk  # For image handling

logging.basicConfig(level=logging.DEBUG)

class ComplexSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Complex Solver")
        self.root.geometry("800x1000")
        self.root.minsize(800, 1000)  # Prevent the window from being resized too small
        self.root.resizable(True, True)
        
        # Load and set the .ico file as the window and taskbar icon
        self.logo_path = os.path.join(os.path.dirname(__file__), 'nomadic_tech.ico')
        self.bg_image_path = os.path.join(os.path.dirname(__file__), 'nomadic_tech.png')
        if os.path.exists(self.logo_path):
            try:
                # Set the window icon
                self.root.iconbitmap(self.logo_path)

                # Explicitly set the taskbar icon using ctypes (Windows only)
                app_id = 'nomadic_tech.complex_solver'
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

                # Set the icon for the main window (ensures consistency in the taskbar)
                self.root.call('wm', 'iconphoto', self.root._w, tk.PhotoImage(file=self.logo_path))

            except Exception as e:
                logging.error(f"Failed to set icon: {e}")

        # Optional: Load a background image if desired
        if os.path.exists(self.bg_image_path):
            bg_image = Image.open(self.bg_image_path)
            bg_image = bg_image.resize((900, 750), Image.LANCZOS)  # Resize to fit window
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            
            # Create a label with the image as the background
            bg_label = tk.Label(self.root, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            logging.warning(f"Background image not found: {self.bg_image_path}")

        self.dark_mode = tk.BooleanVar(value=True)
        self.theme = {
            "light": {
                "bg": "#f0f0f0",
                "fg": "#000000",
                "highlight": "#4a86e8",
                "accent": "#e8e8e8",
                "button": "#e0e0e0",
                "selected": "#a0c8ff",
                "yes_bg": "#d4edda",
                "yes_fg": "#155724",
                "no_bg": "#f8d7da",
                "no_fg": "#721c24"
            },
            "dark": {
                "bg": "#2d2d2d",
                "fg": "#ffffff",
                "highlight": "#5294ff",
                "accent": "#3d3d3d",
                "button": "#444444",
                "selected": "#3a6ea5",
                "yes_bg": "#165724",
                "yes_fg": "#d4edda",
                "no_bg": "#721c24",
                "no_fg": "#f8d7da"
            }
        }


        self.style = ttk.Style()
        self.setup_styles()
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=1, pady=10)
        
        # Base conversion variables
        self.to_binary_var = tk.BooleanVar(value=True)
        self.to_octal_var = tk.BooleanVar(value=True)
        self.to_decimal_var = tk.BooleanVar(value=True)
        self.to_hex_var = tk.BooleanVar(value=True)
        self.to_custom_var = tk.BooleanVar(value=False)
        self.custom_to_base_var = tk.StringVar(value="3")
        self.from_base_var = tk.StringVar(value="10")
        self.conv_input_var = tk.StringVar()
        
        # We'll define conv_results_frame = None; set it in create_number_conversion_tab
        self.conv_results_frame = None
        
        # Steps/visual
        self.show_steps_var = tk.BooleanVar(value=True)
        self.visualize_var = tk.BooleanVar(value=False)
        
        # Create the main solver tab
        self.create_complex_solver_tab()
        
        # Optionally create the number conversion tab here
        self.create_number_conversion_tab()
        
        self.history = []
        self.current_result = None
        self.current_equation = None

    def setup_styles(self):
        c = self.get_theme_colors()
        self.style.configure("TFrame", background=c["bg"])
        self.style.configure("TLabel", background=c["bg"], foreground=c["fg"], font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("Header.TLabel", background=c["bg"], foreground=c["fg"], font=("Arial", 14, "bold"))
        self.style.configure("Result.TLabel", background=c["bg"], foreground=c["fg"], font=("Arial", 10))
        self.style.configure("Step.TLabel", background=c["bg"], foreground=c["fg"], font=("Arial", 10, "italic"))
        self.style.configure("Yes.TLabel", background=c["yes_bg"], foreground=c["yes_fg"])
        self.style.configure("No.TLabel", background=c["no_bg"], foreground=c["no_fg"])
        self.style.configure("Operator.TButton", font=("Arial", 12, "bold"), width=5)
        self.style.configure("FuncOp.TButton", font=("Arial", 10), width=7)
        self.style.configure("Selected.Operator.TButton", background=c["selected"])
        self.style.configure("Selected.FuncOp.TButton", background=c["selected"])
        self.style.configure("TNotebook", background=c["bg"])
        self.style.configure("TNotebook.Tab", background=c["button"], foreground=c["fg"])
        self.style.map("TNotebook.Tab",
                       background=[("selected", c["highlight"])],
                       foreground=[("selected", "#ffffff")])
        self.style.configure("TCheckbutton", background=c["bg"], foreground=c["fg"])
        self.style.configure("TRadiobutton", background=c["bg"], foreground=c["fg"])
        self.style.configure("TEntry", fieldbackground=c["accent"])
        self.style.map("TCombobox",
                       fieldbackground=[("readonly", c["accent"])],
                       selectbackground=[("readonly", c["highlight"])])

    def get_theme_colors(self):
        return self.theme["dark"] if self.dark_mode.get() else self.theme["light"]

    def toggle_dark_mode(self):
        self.dark_mode.set(not self.dark_mode.get())
        self.setup_styles()
        self.root.configure(background=self.get_theme_colors()["bg"])

    def create_complex_solver_tab(self):
        tab_frame = ttk.Frame(self.notebook, style="TFrame", padding="20")
        self.notebook.add(tab_frame, text="Complex Solver")
        
        canvas = tk.Canvas(tab_frame, borderwidth=100, background=self.get_theme_colors()["bg"])
        v_scroll = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=v_scroll.set)
        v_scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        self.content_frame = ttk.Frame(canvas, style="TFrame")
        self.content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((10, 10), window=self.content_frame, anchor="nw")
        
        self.content_frame.grid_rowconfigure(0, weight=0)
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_rowconfigure(2, weight=1)
        self.content_frame.grid_rowconfigure(3, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        header_frame = ttk.Frame(self.content_frame, style="TFrame")
        header_frame.grid(row=0, column=0, columnspan=2, pady=(0,20), sticky="ew")
        header_label = ttk.Label(header_frame, text="Complex Number Solver", style="Header.TLabel")
        header_label.grid(row=0, column=0, sticky="w")
        dark_mode_btn = ttk.Button(header_frame, text="Toggle Dark Mode", command=self.toggle_dark_mode)
        dark_mode_btn.grid(row=0, column=1, sticky="e")
        header_frame.columnconfigure(0, weight=1)
        
        op_frame = ttk.Frame(self.content_frame, style="TFrame")
        op_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        op_frame.columnconfigure(0, weight=1)
        
        lbl_z1 = ttk.Label(op_frame, text="Complex Number (z1):", style="TLabel")
        lbl_z1.grid(row=0, column=0, sticky="w", pady=(0,5))
        
        self.z1_entry = ttk.Entry(op_frame, width=40)
        self.z1_entry.grid(row=1, column=0, padx=(0,10), sticky="ew")
        
        self.z1_placeholder_text = "e.g. 2+3j or 2,3"
        self.z1_has_typed = False
        self.z1_entry.insert(0, self.z1_placeholder_text)
        self.z1_entry.bind("<FocusIn>", self._clear_placeholder)
        self.z1_entry.bind("<FocusOut>", self._add_placeholder_if_empty)
        
        lbl_z2 = ttk.Label(op_frame, text="Second Complex Number (z2) - if needed:", style="TLabel")
        lbl_z2.grid(row=2, column=0, sticky="w", pady=(10,5))
        self.second_complex_var = tk.StringVar()
        self.second_complex_entry = ttk.Entry(op_frame, textvariable=self.second_complex_var, width=40)
        self.second_complex_entry.grid(row=3, column=0, padx=(0,10), sticky="ew")
        
        op_label = ttk.Label(op_frame, text="Operation:", style="TLabel")
        op_label.grid(row=4, column=0, sticky="w", pady=(10,5))
        self.operation_var = tk.StringVar(value="+")
        op_combo = ttk.Combobox(op_frame, textvariable=self.operation_var, state="readonly",
                                values=["+", "-", "*", "/", "^", "sqrt", "abs", "conj", "polar", "rect", "sin", "cos", "tan", "exp", "log"])
        op_combo.grid(row=5, column=0, sticky="w")
        
        solve_btn = ttk.Button(op_frame, text="Solve", command=self.solve_complex)
        solve_btn.grid(row=6, column=0, pady=(20,0), sticky="w")
        
        self.steps_frame = ttk.Frame(self.content_frame, style="TFrame")
        self.steps_frame.grid(row=2, column=0, columnspan=2, pady=(10,20), sticky="nsew")
        steps_header = ttk.Label(self.steps_frame, text="Calculation Steps:", style="Header.TLabel")
        steps_header.pack(anchor="w")
        
        self.results_frame = ttk.Frame(self.content_frame, style="TFrame")
        self.results_frame.grid(row=3, column=0, columnspan=2, pady=(10,20), sticky="nsew")
        results_header = ttk.Label(self.results_frame, text="Result:", style="Header.TLabel")
        results_header.pack(anchor="w")
        
        self.z1_entry.bind("<Return>", lambda e: self.solve_complex())
        self.second_complex_entry.bind("<Return>", lambda e: self.solve_complex())


    def _clear_placeholder(self, event):
        if not self.z1_has_typed and self.z1_entry.get() == self.z1_placeholder_text:
            self.z1_entry.delete(0, tk.END)
            self.z1_has_typed = True

    def _add_placeholder_if_empty(self, event):
        if self.z1_entry.get().strip() == "":
            self.z1_has_typed = False
            self.z1_entry.insert(0, self.z1_placeholder_text)

    def parse_complex_input(self, input_str):
        s = input_str.strip()
        if "," in s:
            parts = s.split(",")
            if len(parts) == 2:
                try:
                    return complex(float(parts[0].strip()), float(parts[1].strip()))
                except ValueError:
                    pass
        try:
            return complex(s.replace(" ", ""))
        except:
            raise ValueError("Invalid complex format (try e.g. 2+3j or 2,3).")

    def clear_complex_results(self):
        for w in self.results_frame.winfo_children():
            if w != self.results_frame.winfo_children()[0]:
                w.destroy()

    def clear_steps(self):
        for w in self.steps_frame.winfo_children():
            if w != self.steps_frame.winfo_children()[0]:
                w.destroy()

    def add_step(self, text):
        step_lbl = ttk.Label(self.steps_frame, text=text, style="Step.TLabel")
        step_lbl.pack(anchor="w")

    def add_to_history(self, operation_text, equation, result):
        self.history.append((operation_text, equation, result))

    def display_result(self, equation):
        for w in self.results_frame.winfo_children():
            if w != self.results_frame.winfo_children()[0]:
                w.destroy()
        result_lbl = ttk.Label(self.results_frame, text=equation, style="Result.TLabel", font=("Arial", 12))
        result_lbl.pack(anchor="w", pady=(5,0))

    def solve_complex(self):
        self.clear_complex_results()
        self.clear_steps()
        try:
            z1_str = self.z1_entry.get().strip()
            z2_str = self.second_complex_var.get().strip()
            operation = self.operation_var.get()
            if z1_str == self.z1_placeholder_text:
                z1_str = ""
            if not z1_str:
                messagebox.showerror("Error", "Please enter the first complex number.")
                return
            self.add_step(f"Parsing first complex number: {z1_str}")
            z1 = self.parse_complex_input(z1_str)
            self.add_step(f"z1 = {z1}")
            z2 = None
            equation = ""
            operation_text = ""
            result = None
            if operation in ['+', '-', '*', '/', '^']:
                if not z2_str:
                    messagebox.showerror("Error", "Please enter the second complex number for binary operations.")
                    return
                self.add_step(f"Parsing second complex number: {z2_str}")
                z2 = self.parse_complex_input(z2_str)
                self.add_step(f"z2 = {z2}")
                if operation == '+':
                    self.add_step(f"Calculating: {z1} + {z2}")
                    result = z1 + z2
                    operation_text = "Addition"
                    equation = f"({z1}) + ({z2}) = {result}"
                elif operation == '-':
                    self.add_step(f"Calculating: {z1} - {z2}")
                    result = z1 - z2
                    operation_text = "Subtraction"
                    equation = f"({z1}) - ({z2}) = {result}"
                elif operation == '*':
                    self.add_step(f"Calculating: {z1} * {z2}")
                    result = z1 * z2
                    operation_text = "Multiplication"
                    equation = f"({z1}) * ({z2}) = {result}"
                    if self.show_steps_var.get():
                        a, b = z1.real, z1.imag
                        c, d = z2.real, z2.imag
                        self.add_step("Using formula: (a+bi)*(c+di) = (ac - bd) + (ad + bc)i")
                        self.add_step(f"a = {a}, b = {b}, c = {c}, d = {d}")
                        self.add_step(f"Real part: {a*c - b*d}")
                        self.add_step(f"Imaginary part: {a*d + b*c}")
                elif operation == '/':
                    if z2 == 0:
                        messagebox.showerror("Error", "Division by zero.")
                        return
                    self.add_step(f"Calculating: {z1} / {z2}")
                    result = z1 / z2
                    operation_text = "Division"
                    equation = f"({z1}) / ({z2}) = {result}"
                    if self.show_steps_var.get():
                        a, b = z1.real, z1.imag
                        c, d = z2.real, z2.imag
                        self.add_step("Multiplying numerator/denominator by conjugate of denominator")
                        numerator_real = a*c + b*d
                        numerator_imag = b*c - a*d
                        denominator = c*c + d*d
                        self.add_step(f"Num real={numerator_real}, Num imag={numerator_imag}, Den={denominator}")
                elif operation == '^':
                    self.add_step(f"Calculating: {z1} ^ {z2}")
                    result = z1 ** z2
                    operation_text = "Power"
                    equation = f"({z1}) ^ ({z2}) = {result}"
                    if self.show_steps_var.get():
                        if z2.imag == 0 and z2.real.is_integer() and 0 < z2.real <= 5:
                            self.add_step("Multiplying z1 repeatedly:")
                            power = int(z2.real)
                            temp = complex(1, 0)
                            for i in range(power):
                                temp_prev = temp
                                temp *= z1
                                self.add_step(f"Step {i+1}: {temp_prev} * {z1} = {temp}")
                        else:
                            r, theta = cmath.polar(z1)
                            self.add_step("Using formula: z^w = e^(w*ln(z))")
                            self.add_step(f"Polar form of z1: r = {r}, θ = {theta}")
            else:
                if operation == 'sqrt':
                    self.add_step(f"Calculating sqrt({z1})")
                    result = cmath.sqrt(z1)
                    operation_text = "Square Root"
                    equation = f"sqrt({z1}) = {result}"
                    if self.show_steps_var.get():
                        r, theta = cmath.polar(z1)
                        self.add_step(f"Polar form: r = {r}, θ = {theta}")
                elif operation == 'abs':
                    self.add_step(f"Calculating abs({z1})")
                    result = abs(z1)
                    operation_text = "Absolute Value"
                    equation = f"|{z1}| = {result}"
                elif operation == 'conj':
                    self.add_step(f"Calculating conjugate of {z1}")
                    result = z1.conjugate()
                    operation_text = "Conjugate"
                    equation = f"conj({z1}) = {result}"
                elif operation == 'polar':
                    self.add_step(f"Converting {z1} to polar form")
                    r, theta = cmath.polar(z1)
                    result = f"{r} < {theta}"
                    operation_text = "Conversion to Polar Form"
                    equation = f"polar({z1}) = {result}"
                elif operation == 'rect':
                    self.add_step(f"Converting polar form {z1_str} to rectangular")
                    parts = z1_str.split('<')
                    if len(parts) != 2:
                        messagebox.showerror("Error", "For rect conversion, use format r<theta")
                        return
                    r = float(parts[0].strip())
                    th = float(parts[1].strip())
                    result = complex(r * math.cos(th), r * math.sin(th))
                    operation_text = "Conversion to Rectangular Form"
                    equation = f"rect({z1_str}) = {result}"
                elif operation == 'sin':
                    self.add_step(f"Calculating sin({z1})")
                    result = cmath.sin(z1)
                    operation_text = "Sine"
                    equation = f"sin({z1}) = {result}"
                elif operation == 'cos':
                    self.add_step(f"Calculating cos({z1})")
                    result = cmath.cos(z1)
                    operation_text = "Cosine"
                    equation = f"cos({z1}) = {result}"
                elif operation == 'tan':
                    self.add_step(f"Calculating tan({z1})")
                    result = cmath.tan(z1)
                    operation_text = "Tangent"
                    equation = f"tan({z1}) = {result}"
                elif operation == 'exp':
                    self.add_step(f"Calculating exp({z1})")
                    result = cmath.exp(z1)
                    operation_text = "Exponential"
                    equation = f"exp({z1}) = {result}"
                    if self.show_steps_var.get():
                        a, b = z1.real, z1.imag
                        self.add_step(f"Using Euler's formula: e^(a+bj) = e^a*(cos(b)+j*sin(b))")
                elif operation == 'log':
                    if z1 == 0:
                        messagebox.showerror("Error", "Cannot compute logarithm of zero.")
                        return
                    self.add_step(f"Calculating log({z1})")
                    result = cmath.log(z1)
                    operation_text = "Natural Logarithm"
                    equation = f"log({z1}) = {result}"
                    if self.show_steps_var.get():
                        r, theta = cmath.polar(z1)
                        self.add_step(f"Polar form: r = {r}, θ = {theta}")
                else:
                    messagebox.showerror("Error", "Unknown operation selected.")
                    return
            self.display_result(equation)
            self.add_to_history(operation_text, equation, result)
            if hasattr(self, 'add_to_visualization') and self.visualize_var.get():
                if operation in ['+', '-', '*', '/', '^']:
                    self.add_to_visualization(f"z1 ({operation_text})", z1)
                    self.add_to_visualization(f"z2 ({operation_text})", z2)
                self.add_to_visualization(f"Result ({operation_text})", result)
        except Exception as e:
            logging.exception("Error during complex solving")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def display_complex_results(self, operation_text, equation, result):
        pass

    # Combined with the second code: create_number_conversion_tab
    def create_number_conversion_tab(self):
        conv_frame = ttk.Frame(self.notebook, style="TFrame", padding="15")
        self.notebook.add(conv_frame, text="Number Conversion")

        if hasattr(self, 'logo_photo'):
            logo_label = ttk.Label(conv_frame, image=self.logo_photo)
            logo_label.grid(row=0, column=0, columnspan=4, pady=(10, 20))

        lbl_input = ttk.Label(conv_frame, text="Input Number:", style="TLabel")
        lbl_input.grid(row=1, column=0, sticky="w", pady=(0, 5))
        
        entry_input = ttk.Entry(conv_frame, textvariable=self.conv_input_var, width=40)
        entry_input.grid(row=1, column=1, columnspan=3, padx=(0, 10), sticky="ew")

        lbl_from = ttk.Label(conv_frame, text="From Base:", style="TLabel")
        lbl_from.grid(row=2, column=0, sticky="w", pady=(10, 5))

        bases_frame = ttk.Frame(conv_frame, style="TFrame")
        bases_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        common_bases = [
            ("Binary (2)", "2"),
            ("Octal (8)", "8"),
            ("Decimal (10)", "10"),
            ("Hexadecimal (16)", "16")
        ]
        for i, (txt, val) in enumerate(common_bases):
            rb = ttk.Radiobutton(bases_frame, text=txt, value=val, variable=self.from_base_var)
            rb.grid(row=0, column=i, sticky="w", padx=5)
        
        custom_base_frame = ttk.Frame(bases_frame, style="TFrame")
        custom_base_frame.grid(row=1, column=0, columnspan=4, sticky="w", pady=(5, 0))
        custom_rb = ttk.Radiobutton(custom_base_frame, text="Custom Base:", value="custom", variable=self.from_base_var)
        custom_rb.grid(row=0, column=0, sticky="w")
        custom_from_entry = ttk.Entry(custom_base_frame, textvariable=self.custom_to_base_var, width=5)
        custom_from_entry.grid(row=0, column=1, padx=(5, 0), sticky="w")

        lbl_to = ttk.Label(conv_frame, text="Convert to:", style="TLabel")
        lbl_to.grid(row=4, column=0, sticky="w", pady=(10, 5))

        to_bases_frame = ttk.Frame(conv_frame, style="TFrame")
        to_bases_frame.grid(row=5, column=0, columnspan=3, sticky="ew")

        chk_bin = ttk.Checkbutton(to_bases_frame, text="Binary", variable=self.to_binary_var)
        chk_bin.grid(row=0, column=0, sticky="w", padx=5)
        chk_oct = ttk.Checkbutton(to_bases_frame, text="Octal", variable=self.to_octal_var)
        chk_oct.grid(row=0, column=1, sticky="w", padx=5)
        chk_dec = ttk.Checkbutton(to_bases_frame, text="Decimal", variable=self.to_decimal_var)
        chk_dec.grid(row=0, column=2, sticky="w", padx=5)
        chk_hex = ttk.Checkbutton(to_bases_frame, text="Hexadecimal", variable=self.to_hex_var)
        chk_hex.grid(row=0, column=3, sticky="w", padx=5)

        chk_cust = ttk.Checkbutton(to_bases_frame, text="Custom Base:", variable=self.to_custom_var)
        chk_cust.grid(row=1, column=0, sticky="w", padx=5, pady=(5, 0))
        custom_to_entry = ttk.Entry(to_bases_frame, textvariable=self.custom_to_base_var, width=5)
        custom_to_entry.grid(row=1, column=1, sticky="w", pady=(5, 0))

        btn_calc = ttk.Button(conv_frame, text="Convert", command=self.calculate_number_conversion)
        btn_calc.grid(row=6, column=0, pady=(15, 0), sticky="w")

        self.conv_results_frame = ttk.Frame(conv_frame, style="TFrame")
        self.conv_results_frame.grid(row=7, column=0, columnspan=3, pady=(15, 0), sticky="ew")

        help_frame = ttk.Frame(conv_frame, style="TFrame")
        help_frame.grid(row=8, column=0, columnspan=3, pady=(20, 0), sticky="ew")
        help_text = (
            "• Enter a number in the specified base\n"
            "• For hexadecimal, use 0-9 and A-F\n"
            "• Custom bases can be 2..36\n"
            "• For base>10, use letters A-Z for digits>9"
        )
        lbl_help = ttk.Label(help_frame, text=help_text, style="TLabel", justify="left")
        lbl_help.grid(row=0, column=0, sticky="w")

    def calculate_number_conversion(self):
        try:
            for w in self.conv_results_frame.winfo_children():
                w.destroy()
            
            inp = self.conv_input_var.get().strip()
            if not inp:
                raise ValueError("Please enter a number to convert.")
            fbase = self.from_base_var.get()
            if fbase == "custom":
                fbase = self.custom_to_base_var.get()
            fbase = int(fbase)
            if fbase < 2 or fbase > 36:
                raise ValueError("Base must be 2..36.")
            
            dec_val = int(inp, fbase)
            results = []
            if self.to_binary_var.get():
                results.append(("Binary(2)", bin(dec_val)[2:]))
            if self.to_octal_var.get():
                results.append(("Octal(8)", oct(dec_val)[2:]))
            if self.to_decimal_var.get():
                results.append(("Decimal(10)", str(dec_val)))
            if self.to_hex_var.get():
                results.append(("Hex(16)", hex(dec_val)[2:].upper()))
            if self.to_custom_var.get():
                cbase = int(self.custom_to_base_var.get())
                if cbase < 2 or cbase > 36:
                    raise ValueError("Custom base must be 2..36.")
                digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                v = dec_val
                out = ""
                while v > 0:
                    out = digits[v % cbase] + out
                    v //= cbase
                if out == "":
                    out = "0"
                results.append((f"Custom({cbase})", out))
            
            self.display_conversion_results(inp, fbase, results)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def display_conversion_results(self, inp, fbase, results):
        for w in self.conv_results_frame.winfo_children():
            w.destroy()
        
        lbl_in = ttk.Label(self.conv_results_frame,
                           text=f"Input: {inp} (Base {fbase})",
                           style="TLabel", font=("Arial",10,"bold"))
        lbl_in.grid(row=0, column=0, sticky="w", pady=(0,10))
        
        for i,(bn,val) in enumerate(results):
            lbl_b = ttk.Label(self.conv_results_frame, text=f"{bn}:", style="TLabel")
            lbl_b.grid(row=i+1, column=0, sticky="w", pady=(0,5))
            lbl_v = ttk.Label(self.conv_results_frame, text=val, style="TLabel")
            lbl_v.grid(row=i+1, column=1, sticky="w", padx=(10,0), pady=(0,5))
