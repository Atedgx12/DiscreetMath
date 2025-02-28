import tkinter as tk
from tkinter import ttk, messagebox
import math
import re


# -----------------------------------------------------------------------------
# 1. CREATE THE ADVANCED MATH TAB
# -----------------------------------------------------------------------------

def create_advanced_math_tab(self):
    adv_math_outer = ttk.Frame(self.notebook, style="TFrame", padding="20")
    self.notebook.add(adv_math_outer, text="Advanced Math")
    
    canvas = tk.Canvas(adv_math_outer, borderwidth=0, background=self.style.lookup("TFrame", "background"))
    v_scroll = ttk.Scrollbar(adv_math_outer, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=v_scroll.set)
    v_scroll.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    
    adv_math_frame = ttk.Frame(canvas, style="TFrame")
    adv_math_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=adv_math_frame, anchor="nw")
    
    header_frame = ttk.Frame(adv_math_frame, style="TFrame")
    header_frame.grid(row=0, column=0, columnspan=2, pady=(0,20), sticky="ew")
    header_label = ttk.Label(header_frame, text="Advanced Mathematical Operations", style="Header.TLabel")
    header_label.grid(row=0, column=0, sticky="w")
    
    # Example fix: place the "Convert" button in adv_math_frame (or whichever frame you want)
    convert_button = ttk.Button(adv_math_frame, text="Convert", command=lambda: self.calculate_number_conversion())
    convert_button.grid(row=2, column=0, pady=(15, 0), sticky="w")
    
    self.adv_notebook = ttk.Notebook(adv_math_frame, style="TNotebook")
    self.adv_notebook.grid(row=1, column=0, sticky="nsew")
    adv_math_frame.columnconfigure(0, weight=1)
    adv_math_frame.rowconfigure(1, weight=1)
    
    # Create sub-tabs
    create_set_operations_tab(self)
    create_logic_operations_tab(self)
    create_number_conversion_tab(self)


# -----------------------------------------------------------------------------
# 2. SET OPERATIONS TAB
# -----------------------------------------------------------------------------

def create_set_operations_tab(self):
    """Create the tab for set operations with visualization."""
    set_frame = ttk.Frame(self.adv_notebook, style="TFrame", padding="15")
    self.adv_notebook.add(set_frame, text="Set Operations")
    
    # Create left and right frames for inputs and visualization
    left_frame = ttk.Frame(set_frame, style="TFrame")
    left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
    
    right_frame = ttk.Frame(set_frame, style="TFrame")
    right_frame.grid(row=0, column=1, sticky="nsew")
    
    set_frame.columnconfigure(0, weight=1)
    set_frame.columnconfigure(1, weight=1)
    set_frame.rowconfigure(0, weight=1)
    
    # Set A input
    set_a_label = ttk.Label(left_frame, text="Set A (comma-separated elements):", style="TLabel")
    set_a_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
    self.set_a_var = tk.StringVar()
    set_a_entry = ttk.Entry(left_frame, textvariable=self.set_a_var, width=40)
    set_a_entry.grid(row=1, column=0, padx=(0, 10), sticky="ew")
    
    # Set B input
    set_b_label = ttk.Label(left_frame, text="Set B (comma-separated elements):", style="TLabel")
    set_b_label.grid(row=2, column=0, sticky="w", pady=(10, 5))
    self.set_b_var = tk.StringVar()
    set_b_entry = ttk.Entry(left_frame, textvariable=self.set_b_var, width=40)
    set_b_entry.grid(row=3, column=0, padx=(0, 10), sticky="ew")
    
    # Set operations selection
    set_ops_frame = ttk.Frame(left_frame, style="TFrame")
    set_ops_frame.grid(row=4, column=0, pady=(15, 0), sticky="ew")
    self.set_op_var = tk.StringVar(value="union")
    set_ops = [
        ("Union (A ∪ B)", "union"),
        ("Intersection (A ∩ B)", "intersection"),
        ("Difference (A - B)", "difference"),
        ("Symmetric Difference (A △ B)", "symmetric_difference"),
        ("Cartesian Product (A × B)", "cartesian_product"),
        ("Is Subset (A ⊆ B)", "is_subset"),
        ("Is Superset (A ⊇ B)", "is_superset"),
        ("Is Disjoint", "is_disjoint")
    ]
    
    # Create radiobuttons in a 4x2 grid
    for i, (text, value) in enumerate(set_ops):
        rb = ttk.Radiobutton(
            set_ops_frame, text=text, value=value, variable=self.set_op_var, 
            command=lambda: self.update_set_visualization_preview()
        )
        rb.grid(row=i % 4, column=i // 4, sticky="w", padx=5, pady=2)
    
    # Calculate button
    calc_button = ttk.Button(left_frame, text="Calculate", command=lambda: self.calculate_set_operation())
    calc_button.grid(row=5, column=0, pady=(15, 0), sticky="w")
    
    # Results frame
    self.set_results_frame = ttk.Frame(left_frame, style="TFrame")
    self.set_results_frame.grid(row=6, column=0, pady=(15, 0), sticky="ew")
    
    # Help text
    help_frame = ttk.Frame(left_frame, style="TFrame")
    help_frame.grid(row=7, column=0, pady=(20, 0), sticky="ew")
    help_text = (
        "• Enter elements separated by commas\n"
        "• Elements can be numbers or text\n"
        "• For text with spaces, use quotes (e.g., \"New York\")\n"
        "• Example: 1, 2, 3, 4, 5 or \"apple\", \"banana\", \"orange\""
    )
    help_label = ttk.Label(help_frame, text=help_text, style="TLabel", justify="left")
    help_label.grid(row=0, column=0, sticky="w")
    
    # Visualization frame in the right pane
    visualization_label = ttk.Label(right_frame, text="Set Operation Visualization:", style="TLabel", font=("Arial", 10, "bold"))
    visualization_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
    
    visualization_frame = ttk.Frame(right_frame, style="TFrame", relief="solid", borderwidth=1)
    visualization_frame.grid(row=1, column=0, sticky="nsew")
    right_frame.rowconfigure(1, weight=1)
    right_frame.columnconfigure(0, weight=1)
    
    # Create canvas for the visualization
    colors = self.get_theme_colors() if hasattr(self, 'get_theme_colors') else {"bg": "#f0f0f0", "fg": "#000000"}
    self.set_canvas = tk.Canvas(visualization_frame, bg=colors["bg"], width=400, height=300)
    self.set_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Optional: call self.update_set_visualization_preview() to draw an initial preview

def update_set_visualization_preview(self):
    """Update the set visualization preview based on the current operation."""
    # Clear the canvas
    self.set_canvas.delete("all")
    
    # Get current operation
    operation = self.set_op_var.get()
    
    # Draw the Venn diagram based on the operation
    self.draw_set_visualization(operation, is_preview=True)

def calculate_set_operation(self):
    """Perform the set operation calculation with visualization."""
    try:
        set_a_str = self.set_a_var.get().strip()
        set_b_str = self.set_b_var.get().strip()
        
        # Parse sets from the input strings
        pattern = r'"[^"]*"|\S+'
        set_a_elements = [elem.strip().strip('"').strip("'") 
                          for elem in re.findall(pattern, set_a_str.replace(',', ' ')) if elem.strip()]
        set_b_elements = [elem.strip().strip('"').strip("'") 
                          for elem in re.findall(pattern, set_b_str.replace(',', ' ')) if elem.strip()]
        
        set_a = set(set_a_elements)
        set_b = set(set_b_elements)
        operation = self.set_op_var.get()
        
        # Store the sets for visualization
        self.current_set_a = set_a
        self.current_set_b = set_b
        
        # 2A. Example: Show an "equation" or expression
        # For demonstration, let's show something like: (A) op (B)
        # In real usage, you might parse a complex expression like (2 + 7j) * (3 - 4j).
        # For now, we'll just store a string to show in the results:
        expression_str = f"{set_a} {operation.upper()} {set_b}"
        
        # 2B. Perform the set operation
        result, result_text = perform_set_operation(set_a, set_b, operation)
        
        # 2C. Show the textual result
        self.display_set_result(set_a, set_b, result, result_text, expression_str)
        
        # Update the visualization with actual data
        self.draw_set_visualization(operation, is_preview=False)
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def display_set_result(self, set_a, set_b, result, result_text, expression_str=None):
    """Display the result of the set operation."""
    for widget in self.set_results_frame.winfo_children():
        widget.destroy()
    
    # Show the 'equation' or expression used:
    if expression_str:
        eq_label = ttk.Label(self.set_results_frame, text=f"Expression: {expression_str}", 
                             style="TLabel", wraplength=400, font=("Arial", 10, "italic"))
        eq_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
    
    # Show sets
    set_a_label = ttk.Label(self.set_results_frame, text=f"Set A: {set_a}", style="TLabel", wraplength=400)
    set_a_label.grid(row=1, column=0, sticky="w", pady=(0, 5))
    
    set_b_label = ttk.Label(self.set_results_frame, text=f"Set B: {set_b}", style="TLabel", wraplength=400)
    set_b_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
    
    # Show the operation result
    result_label = ttk.Label(self.set_results_frame, text=f"{result_text}:", style="TLabel", font=("Arial", 10, "bold"))
    result_label.grid(row=3, column=0, sticky="w", pady=(10, 0))
    
    if isinstance(result, bool):
        result_value = "True" if result else "False"
    elif isinstance(result, set):
        result_value = str(result) if result else "∅ (Empty Set)"
    else:
        result_value = str(result)
    
    result_value_label = ttk.Label(self.set_results_frame, text=result_value, style="TLabel", wraplength=500)
    result_value_label.grid(row=4, column=0, sticky="w", pady=(5, 0))


# -----------------------------------------------------------------------------
# 3. HELPER FUNCTIONS FOR CORE MATHEMATICAL OPERATIONS
# -----------------------------------------------------------------------------

def perform_set_operation(set_a, set_b, operation):
    """Perform the set operation and return the result along with a descriptive text."""
    if operation == "union":
        return set_a | set_b, "Union (A ∪ B)"
    elif operation == "intersection":
        return set_a & set_b, "Intersection (A ∩ B)"
    elif operation == "difference":
        return set_a - set_b, "Difference (A - B)"
    elif operation == "symmetric_difference":
        return set_a ^ set_b, "Symmetric Difference (A △ B)"
    elif operation == "cartesian_product":
        return {(a, b) for a in set_a for b in set_b}, "Cartesian Product (A × B)"
    elif operation == "is_subset":
        return set_a.issubset(set_b), "Is A subset of B (A ⊆ B)"
    elif operation == "is_superset":
        return set_a.issuperset(set_b), "Is A superset of B (A ⊇ B)"
    elif operation == "is_disjoint":
        return set_a.isdisjoint(set_b), "Are A and B disjoint"
    else:
        raise ValueError(f"Unknown operation: {operation}")

def perform_logic_operation_binary(a_str, b_str, operation):
    """Perform bitwise logic operation on two binary strings."""
    max_len = max(len(a_str), len(b_str))
    a_padded = a_str.zfill(max_len)
    b_padded = b_str.zfill(max_len)
    result = ""
    for a_bit, b_bit in zip(a_padded, b_padded):
        a = int(a_bit)
        b = int(b_bit)
        if operation == "and":
            res_bit = a & b
        elif operation == "or":
            res_bit = a | b
        elif operation == "xor":
            res_bit = a ^ b
        elif operation == "nand":
            res_bit = 1 - (a & b)
        elif operation == "nor":
            res_bit = 1 - (a | b)
        elif operation == "xnor":
            res_bit = 1 - (a ^ b)
        elif operation == "not_a":
            res_bit = 1 - a
        elif operation == "implies":
            res_bit = (1 - a) | b
        else:
            raise ValueError(f"Unknown operation: {operation}")
        result += str(res_bit)
    return result

def perform_logic_operation_boolean(a_val, b_val, operation):
    """Perform logic operation for boolean values."""
    if operation == "and":
        return a_val and b_val
    elif operation == "or":
        return a_val or b_val
    elif operation == "xor":
        return a_val != b_val
    elif operation == "nand":
        return not (a_val and b_val)
    elif operation == "nor":
        return not (a_val or b_val)
    elif operation == "xnor":
        return a_val == b_val
    elif operation == "not_a":
        return not a_val
    elif operation == "implies":
        return (not a_val) or b_val
    else:
        raise ValueError(f"Unknown operation: {operation}")


# -----------------------------------------------------------------------------
# 4. LOGIC OPERATIONS TAB
# -----------------------------------------------------------------------------

def create_logic_operations_tab(self):
    """Create the tab for logical operations."""
    logic_frame = ttk.Frame(self.adv_notebook, style="TFrame", padding="15")
    self.adv_notebook.add(logic_frame, text="Logic Operations")
    
    # Input mode selection
    input_mode_frame = ttk.Frame(logic_frame, style="TFrame")
    input_mode_frame.grid(row=0, column=0, sticky="w", pady=(0, 10))
    input_mode_label = ttk.Label(input_mode_frame, text="Input Mode:", style="TLabel")
    input_mode_label.grid(row=0, column=0, sticky="w")
    self.logic_mode_var = tk.StringVar(value="binary")
    binary_rb = ttk.Radiobutton(input_mode_frame, text="Binary (0s and 1s)", value="binary",
                                variable=self.logic_mode_var, command=lambda: update_logic_interface(self))
    binary_rb.grid(row=0, column=1, sticky="w", padx=(10, 20))
    boolean_rb = ttk.Radiobutton(input_mode_frame, text="Boolean (True/False)", value="boolean",
                                 variable=self.logic_mode_var, command=lambda: update_logic_interface(self))
    boolean_rb.grid(row=0, column=2, sticky="w")
    
    # Separate frames for binary and boolean inputs
    self.logic_binary_frame = ttk.Frame(logic_frame, style="TFrame")
    self.logic_boolean_frame = ttk.Frame(logic_frame, style="TFrame")
    
    # --- Binary Interface ---
    binary_a_label = ttk.Label(self.logic_binary_frame, text="Input A (binary):", style="TLabel")
    binary_a_label.grid(row=0, column=0, sticky="w", pady=(0,5))
    self.logic_a_var = tk.StringVar(value="0")
    self.logic_a_entry = ttk.Entry(self.logic_binary_frame, textvariable=self.logic_a_var, width=40)
    self.logic_a_entry.grid(row=1, column=0, sticky="ew", pady=(0,10))
    binary_b_label = ttk.Label(self.logic_binary_frame, text="Input B (binary):", style="TLabel")
    binary_b_label.grid(row=2, column=0, sticky="w", pady=(0,5))
    self.logic_b_var = tk.StringVar(value="0")
    self.logic_b_entry = ttk.Entry(self.logic_binary_frame, textvariable=self.logic_b_var, width=40)
    self.logic_b_entry.grid(row=3, column=0, sticky="ew", pady=(0,10))
    
    # --- Boolean Interface ---
    boolean_a_label = ttk.Label(self.logic_boolean_frame, text="Input A (Boolean):", style="TLabel")
    boolean_a_label.grid(row=0, column=0, sticky="w", pady=(0,5))
    self.logic_a_true_var = tk.BooleanVar(value=False)
    self.logic_a_true_rb = ttk.Radiobutton(self.logic_boolean_frame, text="True", value=True,
                                           variable=self.logic_a_true_var)
    self.logic_a_false_rb = ttk.Radiobutton(self.logic_boolean_frame, text="False", value=False,
                                            variable=self.logic_a_true_var)
    self.logic_a_true_rb.grid(row=1, column=0, sticky="w", padx=(0,10))
    self.logic_a_false_rb.grid(row=1, column=1, sticky="w")
    
    boolean_b_label = ttk.Label(self.logic_boolean_frame, text="Input B (Boolean):", style="TLabel")
    boolean_b_label.grid(row=2, column=0, sticky="w", pady=(0,5))
    self.logic_b_true_var = tk.BooleanVar(value=False)
    self.logic_b_true_rb = ttk.Radiobutton(self.logic_boolean_frame, text="True", value=True,
                                           variable=self.logic_b_true_var)
    self.logic_b_false_rb = ttk.Radiobutton(self.logic_boolean_frame, text="False", value=False,
                                            variable=self.logic_b_true_var)
    self.logic_b_true_rb.grid(row=3, column=0, sticky="w", padx=(0,10))
    self.logic_b_false_rb.grid(row=3, column=1, sticky="w")
    
    # Common Logic Operations Selection and Calculate Button
    logic_ops_frame = ttk.Frame(logic_frame, style="TFrame")
    logic_ops_frame.grid(row=4, column=0, pady=(5, 0), sticky="ew")
    self.logic_op_var = tk.StringVar(value="and")
    logic_ops = [
        ("AND", "and"),
        ("OR", "or"),
        ("XOR", "xor"),
        ("NAND", "nand"),
        ("NOR", "nor"),
        ("XNOR", "xnor"),
        ("NOT A", "not_a"),
        ("Implies (A → B)", "implies")
    ]
    for i, (text, value) in enumerate(logic_ops):
        rb = ttk.Radiobutton(logic_ops_frame, text=text, value=value, variable=self.logic_op_var)
        rb.grid(row=i % 4, column=i // 4, sticky="w", padx=5, pady=2)
    
    calc_button = ttk.Button(logic_frame, text="Calculate", command=lambda: calculate_logic_operation(self))
    calc_button.grid(row=5, column=0, pady=(15, 0), sticky="w")
    
    self.logic_results_frame = ttk.Frame(logic_frame, style="TFrame")
    self.logic_results_frame.grid(row=6, column=0, pady=(15, 0), sticky="ew")
    
    # Display the correct interface based on the current mode
    update_logic_interface(self)

def update_logic_interface(self):
    """Update the logic input interface based on the selected mode."""
    mode = self.logic_mode_var.get()
    # Remove both interfaces
    self.logic_binary_frame.grid_forget()
    self.logic_boolean_frame.grid_forget()
    if mode == "binary":
        self.logic_binary_frame.grid(row=1, column=0, sticky="ew")
    else:
        self.logic_boolean_frame.grid(row=1, column=0, sticky="ew")

def calculate_logic_operation(self):
    """Perform the logical operation calculation."""
    try:
        mode = self.logic_mode_var.get()
        operation = self.logic_op_var.get()
        if mode == "binary":
            a_str = self.logic_a_var.get().strip()
            b_str = self.logic_b_var.get().strip()
            if not all(c in "01" for c in a_str):
                raise ValueError("Input A must contain only 0s and 1s")
            if operation != "not_a" and not all(c in "01" for c in b_str):
                raise ValueError("Input B must contain only 0s and 1s")
            if operation == "not_a":
                b_str = "0" * len(a_str)  # Dummy value for alignment
            result = perform_logic_operation_binary(a_str, b_str, operation)
            display_logic_result(self, a_str, b_str, result, operation, mode)
        else:
            a_val = self.logic_a_true_var.get()
            b_val = self.logic_b_true_var.get()
            result = perform_logic_operation_boolean(a_val, b_val, operation)
            display_logic_result(self, a_val, b_val, result, operation, mode)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def display_logic_result(self, a_val, b_val, result, operation, mode):
    """Display the result of the logic operation along with a truth table (for binary mode)."""
    for widget in self.logic_results_frame.winfo_children():
        widget.destroy()
    
    op_symbols = {
        "and": "∧",
        "or": "∨",
        "xor": "⊕",
        "nand": "⊼",
        "nor": "⊽",
        "xnor": "≡",
        "not_a": "¬",
        "implies": "→"
    }
    op_symbol = op_symbols.get(operation, operation)
    
    if mode == "binary":
        expression = f"{a_val} {op_symbol} {b_val}" if operation != "not_a" else f"{op_symbol}{a_val}"
        result_text = f"Result: {expression} = {result}"
    else:
        expression = f"{str(a_val)} {op_symbol} {str(b_val)}" if operation != "not_a" else f"{op_symbol}{str(a_val)}"
        result_text = f"Result: {expression} = {str(result)}"
    
    result_label = ttk.Label(self.logic_results_frame, text=result_text, style="TLabel", font=("Arial", 11))
    result_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
    
    if mode == "binary":
        truth_table_label = ttk.Label(self.logic_results_frame, text="Truth Table:", style="TLabel", font=("Arial", 10, "bold"))
        truth_table_label.grid(row=1, column=0, sticky="w", pady=(10, 5))
        table_frame = ttk.Frame(self.logic_results_frame, style="TFrame")
        table_frame.grid(row=2, column=0, sticky="w")
        
        ttk.Label(table_frame, text="A", style="TLabel", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=15, pady=5)
        ttk.Label(table_frame, text="B", style="TLabel", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=15, pady=5)
        ttk.Label(table_frame, text="Result", style="TLabel", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=15, pady=5)
        
        for i, (a, b) in enumerate([(0, 0), (0, 1), (1, 0), (1, 1)]):
            ttk.Label(table_frame, text=str(a), style="TLabel").grid(row=i+1, column=0, padx=15, pady=3)
            if operation != "not_a":
                ttk.Label(table_frame, text=str(b), style="TLabel").grid(row=i+1, column=1, padx=15, pady=3)
            if operation == "and":
                result_bit = a & b
            elif operation == "or":
                result_bit = a | b
            elif operation == "xor":
                result_bit = a ^ b
            elif operation == "nand":
                result_bit = 1 - (a & b)
            elif operation == "nor":
                result_bit = 1 - (a | b)
            elif operation == "xnor":
                result_bit = 1 - (a ^ b)
            elif operation == "not_a":
                result_bit = 1 - a
                ttk.Label(table_frame, text=str(result_bit), style="TLabel").grid(row=i+1, column=1, columnspan=2, padx=15, pady=3)
                continue
            elif operation == "implies":
                result_bit = (1 - a) | b
            ttk.Label(table_frame, text=str(result_bit), style="TLabel").grid(row=i+1, column=2, padx=15, pady=3)


# -----------------------------------------------------------------------------
# 5. NUMBER CONVERSION TAB
# -----------------------------------------------------------------------------

def create_number_conversion_tab(self):
    """Create the tab for number base conversions."""
    conv_frame = ttk.Frame(self.adv_notebook, style="TFrame", padding="15")
    self.adv_notebook.add(conv_frame, text="Number Conversion")
    
    # Input number
    input_label = ttk.Label(conv_frame, text="Input Number:", style="TLabel")
    input_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
    self.conv_input_var = tk.StringVar()
    
    # Instead of type="number", use a regular Entry for full alphanumeric input
    input_entry = ttk.Entry(conv_frame, textvariable=self.conv_input_var, width=40)
    input_entry.grid(row=1, column=0, columnspan=3, padx=(0, 10), sticky="ew")
    
    # From base
    from_label = ttk.Label(conv_frame, text="From Base:", style="TLabel")
    from_label.grid(row=2, column=0, sticky="w", pady=(10, 5))
    self.from_base_var = tk.StringVar(value="10")
    
    bases_frame = ttk.Frame(conv_frame, style="TFrame")
    bases_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(0, 10))
    
    common_bases = [
        ("Binary (2)", "2"),
        ("Octal (8)", "8"),
        ("Decimal (10)", "10"),
        ("Hexadecimal (16)", "16"),
    ]
    for i, (text, value) in enumerate(common_bases):
        rb = ttk.Radiobutton(bases_frame, text=text, value=value, variable=self.from_base_var)
        rb.grid(row=0, column=i, sticky="w", padx=5)
    
    # Add custom base option
    custom_rb = ttk.Radiobutton(bases_frame, text="Custom", value="custom", variable=self.from_base_var)
    custom_rb.grid(row=1, column=0, sticky="w", pady=(5, 0))
    
    self.custom_from_base_var = tk.StringVar(value="")
    custom_from_entry = ttk.Entry(bases_frame, textvariable=self.custom_from_base_var, width=5)
    custom_from_entry.grid(row=1, column=1, sticky="w", pady=(5, 0), padx=(5,0))
    
    # "Convert To" section
    to_label = ttk.Label(conv_frame, text="Convert to:", style="TLabel")
    to_label.grid(row=4, column=0, sticky="w", pady=(10, 5))
    
    to_bases_frame = ttk.Frame(conv_frame, style="TFrame")
    to_bases_frame.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(0, 10))
    
    self.to_binary_var = tk.BooleanVar(value=False)
    self.to_octal_var = tk.BooleanVar(value=False)
    self.to_decimal_var = tk.BooleanVar(value=False)
    self.to_hex_var = tk.BooleanVar(value=False)
    self.to_custom_var = tk.BooleanVar(value=False)
    
    chk_bin = ttk.Checkbutton(to_bases_frame, text="Binary (2)", variable=self.to_binary_var)
    chk_bin.grid(row=0, column=0, sticky="w", padx=5)
    chk_oct = ttk.Checkbutton(to_bases_frame, text="Octal (8)", variable=self.to_octal_var)
    chk_oct.grid(row=0, column=1, sticky="w", padx=5)
    chk_dec = ttk.Checkbutton(to_bases_frame, text="Decimal (10)", variable=self.to_decimal_var)
    chk_dec.grid(row=0, column=2, sticky="w", padx=5)
    chk_hex = ttk.Checkbutton(to_bases_frame, text="Hex (16)", variable=self.to_hex_var)
    chk_hex.grid(row=0, column=3, sticky="w", padx=5)
    
    # Custom "to" base
    chk_custom_to = ttk.Checkbutton(to_bases_frame, text="Custom", variable=self.to_custom_var)
    chk_custom_to.grid(row=1, column=0, sticky="w", padx=5, pady=(5, 0))
    
    self.custom_to_base_var = tk.StringVar(value="")
    custom_to_entry = ttk.Entry(to_bases_frame, textvariable=self.custom_to_base_var, width=5)
    custom_to_entry.grid(row=1, column=1, sticky="w", pady=(5, 0))
    
    # Convert button
    convert_btn = ttk.Button(conv_frame, text="Convert", command=lambda: self.calculate_number_conversion())
    convert_btn.grid(row=6, column=0, sticky="w", pady=(10,0))
    
    # Results
    self.conv_results_frame = ttk.Frame(conv_frame, style="TFrame")
    self.conv_results_frame.grid(row=7, column=0, columnspan=3, pady=(15, 0), sticky="ew")
    
    # Help text
    help_frame = ttk.Frame(conv_frame, style="TFrame")
    help_frame.grid(row=8, column=0, columnspan=3, pady=(20, 0), sticky="ew")
    help_text = (
        "• Enter a number in the specified base\n"
        "• For base>10, use letters A-Z for digits>9\n"
        "• Custom bases can be 2..36\n"
        "• Example: Hex uses 0-9 and A-F"
    )
    lbl_help = ttk.Label(help_frame, text=help_text, style="TLabel", justify="left")
    lbl_help.grid(row=0, column=0, sticky="w")


def calculate_number_conversion(self):
    """Validate and convert the input from the selected base to chosen target bases."""
    try:
        inp = self.conv_input_var.get().strip()
        if not inp:
            raise ValueError("Please enter a number to convert.")
        
        # Determine the from-base
        base_str = self.from_base_var.get()
        if base_str == "custom":
            base_str = self.custom_from_base_var.get().strip()
            if not base_str:
                raise ValueError("Please enter a custom 'from' base.")
        
        fbase = int(base_str)
        if fbase < 2 or fbase > 36:
            raise ValueError("Source base must be between 2 and 36.")
        
        # 1. Validate that 'inp' only contains valid digits for base 'fbase'
        valid_digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:fbase]
        # We'll check uppercase version to match A-Z
        inp_upper = inp.upper()
        for ch in inp_upper:
            # Allow negative sign if it's the first character
            if ch == '-' and inp_upper.index(ch) == 0:
                continue
            if ch not in valid_digits:
                raise ValueError(f"Invalid character '{ch}' for base {fbase}. Allowed digits: {valid_digits}")
        
        # 2. Convert the input to a decimal integer
        dec_val = int(inp, fbase)
        
        # 3. Build results
        results = []
        if self.to_binary_var.get():
            results.append(("Binary(2)", self.convert_standard(dec_val, bin)))
        if self.to_octal_var.get():
            results.append(("Octal(8)", self.convert_standard(dec_val, oct)))
        if self.to_decimal_var.get():
            results.append(("Decimal(10)", str(dec_val)))
        if self.to_hex_var.get():
            results.append(("Hex(16)", self.convert_standard(dec_val, hex, upper=True)))
        
        if self.to_custom_var.get():
            custom_to = self.custom_to_base_var.get().strip()
            if not custom_to:
                raise ValueError("Please enter a custom 'to' base.")
            cbase = int(custom_to)
            if cbase < 2 or cbase > 36:
                raise ValueError("Custom base must be between 2 and 36.")
            custom_str = self.convert_to_custom_base(dec_val, cbase)
            results.append((f"Custom({cbase})", custom_str))
        
        self.display_conversion_results(inp, fbase, results)
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def convert_standard(self, number, convert_func, upper=False):
    """
    Converts number using a built-in conversion function (bin, oct, hex) while handling negatives.
    """
    if number < 0:
        converted = "-" + convert_func(-number)[2:]
    else:
        converted = convert_func(number)[2:]
    return converted.upper() if upper else converted

def convert_to_custom_base(self, number, base):
    """
    Convert an integer to a string representation in the specified base (2 to 36),
    handling negative numbers appropriately.
    """
    if number == 0:
        return "0"
    
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sign = "-" if number < 0 else ""
    number = abs(number)
    result = ""
    
    while number:
        result = digits[number % base] + result
        number //= base
    
    return sign + result

def display_conversion_results(self, inp, fbase, results):
    """Display the results of the number conversion."""
    for w in self.conv_results_frame.winfo_children():
        w.destroy()
    
    lbl_in = ttk.Label(self.conv_results_frame, text=f"Input: {inp} (Base {fbase})",
                       style="TLabel", font=("Arial",10,"bold"))
    lbl_in.grid(row=0, column=0, sticky="w", pady=(0,10))
    
    for i, (bn, val) in enumerate(results):
        lbl_b = ttk.Label(self.conv_results_frame, text=f"{bn}:", style="TLabel")
        lbl_b.grid(row=i+1, column=0, sticky="w", pady=(0,5))
        lbl_v = ttk.Label(self.conv_results_frame, text=val, style="TLabel")
        lbl_v.grid(row=i+1, column=1, sticky="w", padx=(10,0), pady=(0,5))


# -----------------------------------------------------------------------------
# 6. DRAW FUNCTIONS FOR SET VISUALIZATION
# -----------------------------------------------------------------------------

def draw_set_visualization(self, operation, is_preview=True):
    """Draw a visual representation of the set operation."""
    self.set_canvas.delete("all")
    
    canvas_width = self.set_canvas.winfo_width()
    canvas_height = self.set_canvas.winfo_height()
    
    if canvas_width < 50:
        canvas_width = 400
    if canvas_height < 50:
        canvas_height = 300
    
    colors = self.get_theme_colors() if hasattr(self, 'get_theme_colors') else {
        "bg": "#f0f0f0", "fg": "#000000", "highlight": "#4a86e8"
    }
    set_a_color = "#4a86e8"
    set_b_color = "#e8b22a"
    intersection_color = "#5eb84d"
    text_color = colors["fg"]
    
    radius = min(canvas_width, canvas_height) * 0.25
    center_x1 = canvas_width * 0.35
    center_x2 = canvas_width * 0.65
    center_y = canvas_height * 0.5
    
    # Draw title
    title_text = self.get_set_operation_title(operation)
    self.set_canvas.create_text(
        canvas_width / 2, 20,
        text=title_text, fill=text_color, font=("Arial", 12, "bold")
    )
    
    if operation in [
        "union", "intersection", "difference", "symmetric_difference",
        "is_subset", "is_superset", "is_disjoint"
    ]:
        oval1 = self.set_canvas.create_oval(
            center_x1 - radius, center_y - radius, 
            center_x1 + radius, center_y + radius, 
            outline=text_color, width=2, fill="", tags="circle_a"
        )
        oval2 = self.set_canvas.create_oval(
            center_x2 - radius, center_y - radius, 
            center_x2 + radius, center_y + radius, 
            outline=text_color, width=2, fill="", tags="circle_b"
        )
        
        # Create set labels
        self.set_canvas.create_text(
            center_x1 - radius * 0.5, center_y - radius * 0.7,
            text="Set A", fill=text_color, font=("Arial", 10, "bold")
        )
        self.set_canvas.create_text(
            center_x2 + radius * 0.5, center_y - radius * 0.7,
            text="Set B", fill=text_color, font=("Arial", 10, "bold")
        )
        
        if not is_preview:
            self.fill_venn_diagram(
                operation, center_x1, center_x2, center_y, radius,
                set_a_color, set_b_color, intersection_color
            )
        else:
            self.preview_venn_diagram(
                operation, center_x1, center_x2, center_y, radius,
                set_a_color, set_b_color, intersection_color
            )
    
    elif operation == "cartesian_product":
        self.draw_cartesian_product(canvas_width, canvas_height, text_color, is_preview)


def get_set_operation_title(self, operation):
    """Get the title for the set operation visualization."""
    operation_titles = {
        "union": "Union (A ∪ B)",
        "intersection": "Intersection (A ∩ B)",
        "difference": "Difference (A - B)",
        "symmetric_difference": "Symmetric Difference (A △ B)",
        "cartesian_product": "Cartesian Product (A × B)",
        "is_subset": "Is A subset of B? (A ⊆ B)",
        "is_superset": "Is A superset of B? (A ⊇ B)",
        "is_disjoint": "Are A and B disjoint?"
    }
    return operation_titles.get(operation, operation.capitalize())

def preview_venn_diagram(self, operation, cx1, cx2, cy, radius, color_a, color_b, color_intersection):
    """
    Create a preview of the Venn diagram based on the operation.
    This uses semi-transparent fills to illustrate the region(s)
    that would be highlighted for each operation.
    """
    import math
    
    # Calculate transparency for preview (0-255)
    alpha = 60  
    color_a_transparent = f"{color_a}{alpha:02x}"
    color_b_transparent = f"{color_b}{alpha:02x}"
    color_intersection_transparent = f"{color_intersection}{alpha:02x}"
    
    # Draw both circles with transparency
    self.set_canvas.create_oval(
        cx1 - radius, cy - radius, 
        cx1 + radius, cy + radius, 
        outline="", fill=color_a_transparent, tags="fill_a"
    )
    self.set_canvas.create_oval(
        cx2 - radius, cy - radius, 
        cx2 + radius, cy + radius, 
        outline="", fill=color_b_transparent, tags="fill_b"
    )
    
    # Calculate the distance between circle centers
    d = math.sqrt((cx1 - cx2) ** 2 + (cy - cy) ** 2)
    
    # If circles overlap (distance < 2*radius), highlight certain areas
    if d < 2 * radius:
        if operation == "intersection":
            # Show only the intersection
            self.set_canvas.create_arc(cx1 - radius, cy - radius, cx1 + radius, cy + radius,
                                       start=math.degrees(math.acos((cx1 - cx2) / d)),
                                       extent=180 - 2 * math.degrees(math.acos((cx1 - cx2) / d)),
                                       style="chord", outline="", fill=color_intersection_transparent)
            self.set_canvas.create_arc(cx2 - radius, cy - radius, cx2 + radius, cy + radius,
                                       start=180 + math.degrees(math.acos((cx1 - cx2) / d)),
                                       extent=180 - 2 * math.degrees(math.acos((cx1 - cx2) / d)),
                                       style="chord", outline="", fill=color_intersection_transparent)
            
            # Remove the original circle fills, leaving only intersection
            self.set_canvas.delete("fill_a")
            self.set_canvas.delete("fill_b")
        
        elif operation == "difference":
            # A - B: Remove B from A
            self.set_canvas.delete("fill_b")
        
        elif operation == "symmetric_difference":
            # A △ B: Show both A and B, but remove intersection
            self.set_canvas.create_arc(cx1 - radius, cy - radius, cx1 + radius, cy + radius,
                                       start=math.degrees(math.acos((cx1 - cx2) / d)),
                                       extent=180 - 2 * math.degrees(math.acos((cx1 - cx2) / d)),
                                       style="chord", outline="", fill=color_a_transparent)
            self.set_canvas.create_arc(cx2 - radius, cy - radius, cx2 + radius, cy + radius,
                                       start=180 + math.degrees(math.acos((cx1 - cx2) / d)),
                                       extent=180 - 2 * math.degrees(math.acos((cx1 - cx2) / d)),
                                       style="chord", outline="", fill=color_b_transparent)
        
        elif operation == "is_subset":
            # Show A fully inside B (smaller circle in bigger circle)
            self.set_canvas.delete("circle_a")
            self.set_canvas.delete("circle_b")
            self.set_canvas.delete("fill_a")
            self.set_canvas.delete("fill_b")
            
            # Draw B as a large circle
            self.set_canvas.create_oval(
                cx2 - radius, cy - radius, 
                cx2 + radius, cy + radius, 
                outline=self.set_canvas.cget("bg"), width=2, fill=color_b_transparent
            )
            # Draw A as a smaller circle inside B
            smaller_radius = radius * 0.6
            self.set_canvas.create_oval(
                cx2 - smaller_radius, cy - smaller_radius, 
                cx2 + smaller_radius, cy + smaller_radius, 
                outline=self.set_canvas.cget("bg"), width=2, fill=color_a_transparent
            )
        
        elif operation == "is_superset":
            # Show B fully inside A
            self.set_canvas.delete("circle_a")
            self.set_canvas.delete("circle_b")
            self.set_canvas.delete("fill_a")
            self.set_canvas.delete("fill_b")
            
            # Draw A as a large circle
            self.set_canvas.create_oval(
                cx1 - radius, cy - radius, 
                cx1 + radius, cy + radius, 
                outline=self.set_canvas.cget("bg"), width=2, fill=color_a_transparent
            )
            # Draw B as a smaller circle inside A
            smaller_radius = radius * 0.6
            self.set_canvas.create_oval(
                cx1 - smaller_radius, cy - smaller_radius, 
                cx1 + smaller_radius, cy + smaller_radius, 
                outline=self.set_canvas.cget("bg"), width=2, fill=color_b_transparent
            )
        
        elif operation == "is_disjoint":
            # Show circles far apart
            self.set_canvas.delete("circle_a")
            self.set_canvas.delete("circle_b")
            self.set_canvas.delete("fill_a")
            self.set_canvas.delete("fill_b")
            
            separation = radius * 2.5
            # Draw A
            self.set_canvas.create_oval(
                cx1 - radius - separation/2, cy - radius,
                cx1 + radius - separation/2, cy + radius,
                outline=self.set_canvas.cget("bg"), width=2, fill=color_a_transparent
            )
            # Draw B
            self.set_canvas.create_oval(
                cx2 - radius + separation/2, cy - radius,
                cx2 + radius + separation/2, cy + radius,
                outline=self.set_canvas.cget("bg"), width=2, fill=color_b_transparent
            )


def fill_venn_diagram(self, operation, cx1, cx2, cy, radius, color_a, color_b, color_intersection):
    """
    Fill the Venn diagram based on the sets (self.current_set_a and self.current_set_b)
    and the operation. Each region is colored or labeled as appropriate.
    """
    if not hasattr(self, 'current_set_a') or not hasattr(self, 'current_set_b'):
        # If we don't have actual sets, use the preview
        self.preview_venn_diagram(operation, cx1, cx2, cy, radius, color_a, color_b, color_intersection)
        return
    
    set_a = self.current_set_a
    set_b = self.current_set_b
    
    # Define color transparency
    alpha = 100  # 0-255
    color_a_transparent = f"{color_a}{alpha:02x}"
    color_b_transparent = f"{color_b}{alpha:02x}"
    color_intersection_transparent = f"{color_intersection}{alpha:02x}"
    
    # For empty sets, we might show them differently
    colors = self.get_theme_colors() if hasattr(self, 'get_theme_colors') else {"bg": "#f0f0f0", "fg": "#000000"}
    
    if operation == "union":
        # Show A, B, and intersection
        self.draw_set_elements(set_a, cx1, cy, radius, color_a_transparent)
        self.draw_set_elements(set_b, cx2, cy, radius, color_b_transparent)
        intersect = set_a.intersection(set_b)
        self.draw_set_elements(intersect, (cx1 + cx2)/2, cy, radius*0.5, color_intersection_transparent)
    
    elif operation == "intersection":
        # Only show intersection
        intersect = set_a.intersection(set_b)
        if intersect:
            self.draw_set_elements(intersect, (cx1 + cx2)/2, cy, radius*0.5, color_intersection_transparent)
        else:
            self.set_canvas.create_text((cx1 + cx2)/2, cy, text="∅ (Empty Set)",
                                        fill=colors["fg"], font=("Arial", 12, "bold"))
    
    elif operation == "difference":
        # A - B
        diff = set_a - set_b
        if diff:
            self.draw_set_elements(diff, cx1 - radius/3, cy, radius*0.6, color_a_transparent)
        else:
            self.set_canvas.create_text(cx1 - radius/3, cy, text="∅ (Empty Set)",
                                        fill=colors["fg"], font=("Arial", 12, "bold"))
    
    elif operation == "symmetric_difference":
        # A △ B
        sym_diff = set_a.symmetric_difference(set_b)
        if sym_diff:
            a_only = set_a - set_b
            b_only = set_b - set_a
            self.draw_set_elements(a_only, cx1 - radius/3, cy, radius*0.6, color_a_transparent)
            self.draw_set_elements(b_only, cx2 + radius/3, cy, radius*0.6, color_b_transparent)
        else:
            self.set_canvas.create_text((cx1 + cx2)/2, cy, text="∅ (Empty Set)",
                                        fill=colors["fg"], font=("Arial", 12, "bold"))
    
    elif operation == "is_subset":
        is_subset = set_a.issubset(set_b)
        answer = "YES" if is_subset else "NO"
        self.set_canvas.create_text((cx1 + cx2)/2, cy - radius/2,
                                    text=f"Is A subset of B? {answer}",
                                    fill=colors["fg"], font=("Arial", 14, "bold"))
        
        if is_subset:
            # Show nested circles
            self.set_canvas.delete("circle_a")
            self.set_canvas.delete("circle_b")
            
            # Draw B as the large circle
            self.set_canvas.create_oval(
                cx2 - radius, cy - radius,
                cx2 + radius, cy + radius,
                outline=colors["fg"], width=2, fill=color_b_transparent
            )
            # A inside B
            smaller_radius = radius * 0.6
            self.set_canvas.create_oval(
                cx2 - smaller_radius, cy - smaller_radius,
                cx2 + smaller_radius, cy + smaller_radius,
                outline=colors["fg"], width=2, fill=color_a_transparent
            )
            # Elements
            self.draw_set_elements(set_b - set_a, cx2, cy - smaller_radius - 20, radius*0.4, color_b_transparent)
            self.draw_set_elements(set_a, cx2, cy, smaller_radius*0.8, color_a_transparent)
        else:
            # Show that A has elements not in B
            outside = set_a - set_b
            self.draw_set_elements(outside, cx1 - radius/3, cy, radius*0.6, color_a_transparent)
    
    elif operation == "is_superset":
        is_superset = set_a.issuperset(set_b)
        answer = "YES" if is_superset else "NO"
        self.set_canvas.create_text((cx1 + cx2)/2, cy - radius/2,
                                    text=f"Is A superset of B? {answer}",
                                    fill=colors["fg"], font=("Arial", 14, "bold"))
        
        if is_superset:
            self.set_canvas.delete("circle_a")
            self.set_canvas.delete("circle_b")
            
            # Draw A as the large circle
            self.set_canvas.create_oval(
                cx1 - radius, cy - radius,
                cx1 + radius, cy + radius,
                outline=colors["fg"], width=2, fill=color_a_transparent
            )
            # B inside A
            smaller_radius = radius * 0.6
            self.set_canvas.create_oval(
                cx1 - smaller_radius, cy - smaller_radius,
                cx1 + smaller_radius, cy + smaller_radius,
                outline=colors["fg"], width=2, fill=color_b_transparent
            )
            # Elements
            self.draw_set_elements(set_a - set_b, cx1, cy - smaller_radius - 20, radius*0.4, color_a_transparent)
            self.draw_set_elements(set_b, cx1, cy, smaller_radius*0.8, color_b_transparent)
        else:
            # Show that B has elements not in A
            outside = set_b - set_a
            self.draw_set_elements(outside, cx2 + radius/3, cy, radius*0.6, color_b_transparent)
    
    elif operation == "is_disjoint":
        is_disjoint = set_a.isdisjoint(set_b)
        answer = "YES" if is_disjoint else "NO"
        self.set_canvas.create_text((cx1 + cx2)/2, cy - radius/2,
                                    text=f"Are A and B disjoint? {answer}",
                                    fill=colors["fg"], font=("Arial", 14, "bold"))
        
        if is_disjoint:
            # Show circles far apart
            self.set_canvas.delete("circle_a")
            self.set_canvas.delete("circle_b")
            
            separation = radius * 2.5
            # A
            self.set_canvas.create_oval(
                cx1 - radius - separation/2, cy - radius,
                cx1 + radius - separation/2, cy + radius,
                outline=colors["fg"], width=2, fill=color_a_transparent
            )
            # B
            self.set_canvas.create_oval(
                cx2 - radius + separation/2, cy - radius,
                cx2 + radius + separation/2, cy + radius,
                outline=colors["fg"], width=2, fill=color_b_transparent
            )
            # Elements
            self.draw_set_elements(set_a, cx1 - separation/2, cy, radius*0.8, color_a_transparent)
            self.draw_set_elements(set_b, cx2 + separation/2, cy, radius*0.8, color_b_transparent)
        else:
            # They do intersect
            intersection = set_a.intersection(set_b)
            self.draw_set_elements(set_a - set_b, cx1 - radius/3, cy, radius*0.6, color_a_transparent)
            self.draw_set_elements(set_b - set_a, cx2 + radius/3, cy, radius*0.6, color_b_transparent)
            self.draw_set_elements(intersection, (cx1 + cx2)/2, cy, radius*0.5, color_intersection_transparent)


def draw_set_elements(self, set_elements, center_x, center_y, max_radius, color):
    """
    Draw the elements of a set in a circular arrangement, filling a circle of
    radius max_radius at the specified center.
    """
    import math
    
    if not set_elements:
        return
    
    # Decide how many elements to display
    num_elements = len(set_elements)
    max_display = 8
    if num_elements <= max_display:
        elements_to_display = list(set_elements)
    else:
        # Show partial, with "..." for the remainder
        elements_to_display = list(set_elements)[:max_display - 1] + ["..."]
    
    # Draw a filled circle as the set's background region
    self.set_canvas.create_oval(
        center_x - max_radius, center_y - max_radius,
        center_x + max_radius, center_y + max_radius,
        outline="", fill=color
    )
    
    # Draw each element's label around the circle
    displayed_count = len(elements_to_display)
    
    # Use the theme's foreground color if available
    colors = self.get_theme_colors() if hasattr(self, 'get_theme_colors') else {"fg": "#000000"}
    text_color = colors["fg"]
    
    for i, element in enumerate(elements_to_display):
        angle = 2 * math.pi * i / displayed_count
        # Keep them somewhat inside the circle
        element_radius = max_radius * 0.7
        x = center_x + element_radius * math.cos(angle)
        y = center_y + element_radius * math.sin(angle)
        
        element_text = str(element)
        if len(element_text) > 10 and element_text != "...":
            element_text = element_text[:7] + "..."
        
        self.set_canvas.create_text(x, y, text=element_text, fill=text_color, font=("Arial", 9))


def draw_cartesian_product(self, canvas_width, canvas_height, text_color, is_preview=True):
    """
    Draw a visualization of the Cartesian product (A × B).
    If is_preview=True, show a sample grid; otherwise, draw actual elements from
    self.current_set_a and self.current_set_b.
    """
    import math
    
    if is_preview:
        # Show a generic grid sample
        width = canvas_width * 0.8
        height = canvas_height * 0.6
        x_start = (canvas_width - width) / 2
        y_start = (canvas_height - height) / 2 + 30
        
        grid_size = 5
        cell_width = width / grid_size
        cell_height = height / grid_size
        
        # Draw grid lines
        for i in range(grid_size + 1):
            self.set_canvas.create_line(
                x_start + i * cell_width, y_start,
                x_start + i * cell_width, y_start + height,
                fill=text_color
            )
            self.set_canvas.create_line(
                x_start, y_start + i * cell_height,
                x_start + width, y_start + i * cell_height,
                fill=text_color
            )
        
        self.set_canvas.create_text(
            x_start - 20, y_start + height / 2,
            text="Set A", fill=text_color, font=("Arial", 10, "bold")
        )
        self.set_canvas.create_text(
            x_start + width / 2, y_start - 20,
            text="Set B", fill=text_color, font=("Arial", 10, "bold")
        )
        
        # Axis arrows
        self.set_canvas.create_line(
            x_start - 30, y_start + height / 2,
            x_start - 10, y_start + height / 2,
            fill=text_color, arrow=tk.LAST
        )
        self.set_canvas.create_line(
            x_start + width / 2, y_start - 30,
            x_start + width / 2, y_start - 10,
            fill=text_color, arrow=tk.LAST
        )
        
        self.set_canvas.create_text(
            canvas_width / 2, canvas_height - 30,
            text="Cartesian Product: All possible pairs (a, b) for a ∈ A, b ∈ B",
            fill=text_color, font=("Arial", 9)
        )
    else:
        # Actual grid with elements from current_set_a and current_set_b
        if not hasattr(self, 'current_set_a') or not hasattr(self, 'current_set_b'):
            # If we don't have sets, fallback to preview
            self.draw_cartesian_product(canvas_width, canvas_height, text_color, True)
            return
        
        set_a = self.current_set_a
        set_b = self.current_set_b
        
        # Limit displayed elements
        max_elements = 8
        set_a_display = list(set_a)[:max_elements]
        set_b_display = list(set_b)[:max_elements]
        
        if not set_a_display or not set_b_display:
            # If either set is empty
            self.set_canvas.create_text(
                canvas_width / 2, canvas_height / 2,
                text="Cartesian Product: ∅ (Empty Set)\nOne or both sets are empty",
                fill=text_color, font=("Arial", 12, "bold"), justify=tk.CENTER
            )
            return
        
        # Dimensions for the grid
        width = canvas_width * 0.8
        height = canvas_height * 0.6
        x_start = (canvas_width - width) / 2
        y_start = (canvas_height - height) / 2 + 30
        
        rows = len(set_b_display)
        cols = len(set_a_display)
        
        cell_width = width / cols
        cell_height = height / rows
        
        # Draw grid lines
        for i in range(cols + 1):
            self.set_canvas.create_line(
                x_start + i * cell_width, y_start,
                x_start + i * cell_width, y_start + height,
                fill=text_color
            )
        for i in range(rows + 1):
            self.set_canvas.create_line(
                x_start, y_start + i * cell_height,
                x_start + width, y_start + i * cell_height,
                fill=text_color
            )
        
        # Draw A headers
        for i, a in enumerate(set_a_display):
            a_str = str(a)
            if len(a_str) > 8:
                a_str = a_str[:5] + "..."
            self.set_canvas.create_text(
                x_start + i * cell_width + cell_width/2,
                y_start - 15,
                text=a_str, fill=text_color, font=("Arial", 9)
            )
        
        # Draw B headers
        for j, b in enumerate(set_b_display):
            b_str = str(b)
            if len(b_str) > 8:
                b_str = b_str[:5] + "..."
            self.set_canvas.create_text(
                x_start - 15,
                y_start + j * cell_height + cell_height/2,
                text=b_str, fill=text_color, font=("Arial", 9)
            )
        
        # Draw each pair
        colors = self.get_theme_colors() if hasattr(self, 'get_theme_colors') else {"highlight": "#4a86e8"}
        pair_color = colors.get("highlight", "#4a86e8")
        
        for i, a in enumerate(set_a_display):
            for j, b in enumerate(set_b_display):
                pair_text = f"({a},{b})"
                # Truncate if too long
                if len(pair_text) > 12:
                    a_str = str(a)[:3] + ".." if len(str(a)) > 5 else str(a)
                    b_str = str(b)[:3] + ".." if len(str(b)) > 5 else str(b)
                    pair_text = f"({a_str},{b_str})"
                
                self.set_canvas.create_text(
                    x_start + i * cell_width + cell_width/2,
                    y_start + j * cell_height + cell_height/2,
                    text=pair_text, fill=pair_color, font=("Arial", 8)
                )
        
        # Axis labels
        self.set_canvas.create_text(
            x_start - 40, y_start + height/2,
            text="Set B", fill=text_color, font=("Arial", 10, "bold")
        )
        self.set_canvas.create_text(
            x_start + width/2, y_start - 35,
            text="Set A", fill=text_color, font=("Arial", 10, "bold")
        )
        
        # Show how many pairs in total
        total_pairs = len(set_a) * len(set_b)
        displayed_pairs = len(set_a_display) * len(set_b_display)
        if total_pairs > displayed_pairs:
            self.set_canvas.create_text(
                canvas_width/2, canvas_height - 20,
                text=f"Showing {displayed_pairs} of {total_pairs} total pairs. (Limited for clarity)",
                fill=text_color, font=("Arial", 9)
            )
        else:
            self.set_canvas.create_text(
                canvas_width/2, canvas_height - 20,
                text=f"Total pairs: {total_pairs}",
                fill=text_color, font=("Arial", 9)
            )
