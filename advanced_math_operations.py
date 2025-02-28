import tkinter as tk
from tkinter import ttk, messagebox
import math
import re


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
        rb = ttk.Radiobutton(set_ops_frame, text=text, value=value, variable=self.set_op_var, 
                           command=lambda: self.update_set_visualization_preview())
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
    
    # Create initial preview

    #self.update_set_visualization_preview()

def update_set_visualization_preview(self):
    """Update the set visualization preview based on the current operation."""
    # Clear the canvas
    self.set_canvas.delete("all")
    
    # Get current operation
    operation = self.set_op_var.get()
    
    # Draw the Venn diagram based on the operation
    self.draw_set_visualization(operation, is_preview=True)


# ---------------------------------------------------------------------------
# Helper Functions for Core Mathematical Operations
# ---------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------
# Advanced Math Operations: UI Code with Scrollable Content
# ---------------------------------------------------------------------------

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
    
    create_set_operations_tab(self)
    create_logic_operations_tab(self)
    create_number_conversion_tab(self)

# -------------------------
# Set Operations Tab
# -------------------------


def calculate_set_operation(self):
    """Perform the set operation calculation with visualization."""
    try:
        import re
        
        set_a_str = self.set_a_var.get().strip()
        set_b_str = self.set_b_var.get().strip()
        pattern = r'"[^"]*"|\S+'
        set_a_elements = [elem.strip().strip('"').strip("'") for elem in re.findall(pattern, set_a_str.replace(',', ' ')) if elem.strip()]
        set_b_elements = [elem.strip().strip('"').strip("'") for elem in re.findall(pattern, set_b_str.replace(',', ' ')) if elem.strip()]
        set_a = set(set_a_elements)
        set_b = set(set_b_elements)
        operation = self.set_op_var.get()
        
        # Store the sets for visualization
        self.current_set_a = set_a
        self.current_set_b = set_b
        
        result, result_text = perform_set_operation(set_a, set_b, operation)
        self.display_set_result(set_a, set_b, result, result_text)
        
        # Update the visualization with actual data
        self.draw_set_visualization(operation, is_preview=False)
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def display_set_result(self, set_a, set_b, result, result_text):
    """Display the result of the set operation."""
    for widget in self.set_results_frame.winfo_children():
        widget.destroy()
    set_a_label = ttk.Label(self.set_results_frame, text=f"Set A: {set_a}", style="TLabel", wraplength=400)
    set_a_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
    set_b_label = ttk.Label(self.set_results_frame, text=f"Set B: {set_b}", style="TLabel", wraplength=400)
    set_b_label.grid(row=1, column=0, sticky="w", pady=(0, 5))
    result_label = ttk.Label(self.set_results_frame, text=f"{result_text}: ", style="TLabel", font=("Arial", 10, "bold"))
    result_label.grid(row=2, column=0, sticky="w", pady=(10, 0))
    if isinstance(result, bool):
        result_value = "True" if result else "False"
    elif isinstance(result, set):
        result_value = str(result) if result else "∅ (Empty Set)"
    else:
        result_value = str(result)
    result_value_label = ttk.Label(self.set_results_frame, text=result_value, style="TLabel", wraplength=500)
    result_value_label.grid(row=3, column=0, sticky="w", pady=(5, 0))

def draw_set_visualization(self, operation, is_preview=True):
    """Draw a visual representation of the set operation."""
    # Clear the canvas
    self.set_canvas.delete("all")
    
    # Get canvas dimensions
    canvas_width = self.set_canvas.winfo_width()
    canvas_height = self.set_canvas.winfo_height()
    
    # If the canvas size is not available yet, use default dimensions
    if canvas_width < 50:  # Arbitrary small value to check if size is set
        canvas_width = 400
    if canvas_height < 50:
        canvas_height = 300
    
    # Set up colors
    colors = self.get_theme_colors() if hasattr(self, 'get_theme_colors') else {
        "bg": "#f0f0f0", "fg": "#000000", "highlight": "#4a86e8"
    }
    set_a_color = "#4a86e8"  # Blue
    set_b_color = "#e8b22a"  # Gold
    intersection_color = "#5eb84d"  # Green
    text_color = colors["fg"]
    
    # Circle parameters
    radius = min(canvas_width, canvas_height) * 0.25
    center_x1 = canvas_width * 0.35
    center_x2 = canvas_width * 0.65
    center_y = canvas_height * 0.5
    
    # Draw title
    title_text = self.get_set_operation_title(operation)
    self.set_canvas.create_text(canvas_width / 2, 20, text=title_text, fill=text_color, font=("Arial", 12, "bold"))
    
    # Draw the circles and labels based on the operation
    if operation in ["union", "intersection", "difference", "symmetric_difference", "is_subset", "is_superset", "is_disjoint"]:
        # Draw Venn diagram
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
        self.set_canvas.create_text(center_x1 - radius * 0.5, center_y - radius * 0.7, text="Set A", fill=text_color, font=("Arial", 10, "bold"))
        self.set_canvas.create_text(center_x2 + radius * 0.5, center_y - radius * 0.7, text="Set B", fill=text_color, font=("Arial", 10, "bold"))
        
        # Fill in the appropriate regions based on the operation
        if not is_preview:
            self.fill_venn_diagram(operation, center_x1, center_x2, center_y, radius, set_a_color, set_b_color, intersection_color)
        else:
            # Preview coloring for each operation
            self.preview_venn_diagram(operation, center_x1, center_x2, center_y, radius, set_a_color, set_b_color, intersection_color)
    
    elif operation == "cartesian_product":
        # For Cartesian product, show a different visualization
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
    """Create a preview of the Venn diagram based on the operation."""
    # Calculate transparency for preview
    alpha = 60  # Transparency level (0-255)
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
    
    # Draw the intersection with a different color
    # Calculate intersection area
    d = math.sqrt((cx1 - cx2) ** 2 + (cy - cy) ** 2)
    if d < 2 * radius:  # If the circles overlap
        # For operations, highlight different areas
        if operation == "intersection":
            # Just color the intersection
            self.set_canvas.create_arc(cx1 - radius, cy - radius, cx1 + radius, cy + radius,
                              start=math.degrees(math.acos((cx1 - cx2) / d)),
                              extent=180 - 2 * math.degrees(math.acos((cx1 - cx2) / d)),
                              style="chord", outline="", fill=color_intersection_transparent, tags="intersection")
            
            self.set_canvas.create_arc(cx2 - radius, cy - radius, cx2 + radius, cy + radius,
                              start=180 + math.degrees(math.acos((cx1 - cx2) / d)),
                              extent=180 - 2 * math.degrees(math.acos((cx1 - cx2) / d)),
                              style="chord", outline="", fill=color_intersection_transparent, tags="intersection")
            
            # Clear fills for A and B to show only intersection
            self.set_canvas.delete("fill_a")
            self.set_canvas.delete("fill_b")
        
        elif operation == "difference":
            # A - B: Remove B from A's preview
            self.set_canvas.delete("fill_b")
        
        elif operation == "symmetric_difference":
            # A △ B: Show A and B but remove intersection
            # We need to remove the intersection
            self.set_canvas.create_arc(cx1 - radius, cy - radius, cx1 + radius, cy + radius,
                              start=math.degrees(math.acos((cx1 - cx2) / d)),
                              extent=180 - 2 * math.degrees(math.acos((cx1 - cx2) / d)),
                              style="chord", outline="", fill=color_a_transparent, tags="intersection")
            
            self.set_canvas.create_arc(cx2 - radius, cy - radius, cx2 + radius, cy + radius,
                              start=180 + math.degrees(math.acos((cx1 - cx2) / d)),
                              extent=180 - 2 * math.degrees(math.acos((cx1 - cx2) / d)),
                              style="chord", outline="", fill=color_b_transparent, tags="intersection")
        
        elif operation == "is_subset":
            # For is_subset, show A inside B
            self.set_canvas.delete("circle_a")
            self.set_canvas.delete("circle_b")
            self.set_canvas.delete("fill_a")
            self.set_canvas.delete("fill_b")
            
            # Draw B as a larger circle
            self.set_canvas.create_oval(
                cx2 - radius, cy - radius, 
                cx2 + radius, cy + radius, 
                outline=self.set_canvas.cget("bg"), width=2, fill=color_b_transparent, tags="circle_b"
            )
            
            # Draw A as a smaller circle inside B
            smaller_radius = radius * 0.6
            self.set_canvas.create_oval(
                cx2 - smaller_radius, cy - smaller_radius, 
                cx2 + smaller_radius, cy + smaller_radius, 
                outline=self.set_canvas.cget("bg"), width=2, fill=color_a_transparent, tags="circle_a"
            )
            
            # Updated labels
            self.set_canvas.create_text(cx2, cy - smaller_radius - 15, text="Set A", fill=self.set_canvas.cget("fg"), font=("Arial", 10, "bold"))
            self.set_canvas.create_text(cx2, cy + radius + 15, text="Set B", fill=self.set_canvas.cget("fg"), font=("Arial", 10, "bold"))
        
        elif operation == "is_superset":
            # For is_superset, show B inside A
            self.set_canvas.delete("circle_a")
            self.set_canvas.delete("circle_b")
            self.set_canvas.delete("fill_a")
            self.set_canvas.delete("fill_b")
            
            # Draw A as a larger circle
            self.set_canvas.create_oval(
                cx1 - radius, cy - radius, 
                cx1 + radius, cy + radius, 
                outline=self.set_canvas.cget("bg"), width=2, fill=color_a_transparent, tags="circle_a"
            )
            
            # Draw B as a smaller circle inside A
            smaller_radius = radius * 0.6
            self.set_canvas.create_oval(
                cx1 - smaller_radius, cy - smaller_radius, 
                cx1 + smaller_radius, cy + smaller_radius, 
                outline=self.set_canvas.cget("bg"), width=2, fill=color_b_transparent, tags="circle_b"
            )
            
            # Updated labels
            self.set_canvas.create_text(cx1, cy - radius - 15, text="Set A", fill=self.set_canvas.cget("fg"), font=("Arial", 10, "bold"))
            self.set_canvas.create_text(cx1, cy, text="Set B", fill=self.set_canvas.cget("fg"), font=("Arial", 10, "bold"))
        
        elif operation == "is_disjoint":
            # For is_disjoint, show separated circles
            self.set_canvas.delete("circle_a")
            self.set_canvas.delete("circle_b")
            self.set_canvas.delete("fill_a")
            self.set_canvas.delete("fill_b")
            
            # Draw circles far apart
            separation = radius * 2.5
            
            # Draw A
            self.set_canvas.create_oval(
                cx1 - radius - separation/2, cy - radius, 
                cx1 + radius - separation/2, cy + radius, 
                outline=self.set_canvas.cget("bg"), width=2, fill=color_a_transparent, tags="circle_a"
            )
            
            # Draw B
            self.set_canvas.create_oval(
                cx2 - radius + separation/2, cy - radius, 
                cx2 + radius + separation/2, cy + radius, 
                outline=self.set_canvas.cget("bg"), width=2, fill=color_b_transparent, tags="circle_b"
            )
            
            # Updated labels
            self.set_canvas.create_text(cx1 - separation/2, cy - radius - 15, text="Set A", fill=self.set_canvas.cget("fg"), font=("Arial", 10, "bold"))
            self.set_canvas.create_text(cx2 + separation/2, cy - radius - 15, text="Set B", fill=self.set_canvas.cget("fg"), font=("Arial", 10, "bold"))

def fill_venn_diagram(self, operation, cx1, cx2, cy, radius, color_a, color_b, color_intersection):
    """Fill the Venn diagram based on the sets and operation."""
    if not hasattr(self, 'current_set_a') or not hasattr(self, 'current_set_b'):
        # If we don't have actual sets, use the preview
        self.preview_venn_diagram(operation, cx1, cx2, cy, radius, color_a, color_b, color_intersection)
        return
    
    set_a = self.current_set_a
    set_b = self.current_set_b
    
    # Calculate color transparencies
    alpha = 100  # Transparency level (0-255)
    color_a_transparent = f"{color_a}{alpha:02x}"
    color_b_transparent = f"{color_b}{alpha:02x}"
    color_intersection_transparent = f"{color_intersection}{alpha:02x}"
    
    # Get highlight color for empty sets
    colors = self.get_theme_colors() if hasattr(self, 'get_theme_colors') else {"bg": "#f0f0f0", "fg": "#000000"}
    empty_color = f"{colors['bg']}{alpha:02x}"
    
    # Draw elements differently based on the operation
    if operation == "union":
        # Draw both circles and their elements
        self.draw_set_elements(set_a, cx1, cy, radius, color_a_transparent)
        self.draw_set_elements(set_b, cx2, cy, radius, color_b_transparent)
        self.draw_set_elements(set_a.intersection(set_b), (cx1 + cx2) / 2, cy, radius / 2, color_intersection_transparent)
    
    elif operation == "intersection":
        # Just show the intersection
        intersection = set_a.intersection(set_b)
        if intersection:
            self.draw_set_elements(intersection, (cx1 + cx2) / 2, cy, radius / 2, color_intersection_transparent)
        else:
            # Draw a clear indication that intersection is empty
            self.set_canvas.create_text((cx1 + cx2) / 2, cy, text="∅ (Empty Set)", 
                                        fill=colors["fg"], font=("Arial", 12, "bold"))
    
    elif operation == "difference":
        # A - B
        difference = set_a - set_b
        if difference:
            self.draw_set_elements(difference, cx1 - radius / 3, cy, radius * 0.6, color_a_transparent)
        else:
            # Draw a clear indication that difference is empty
            self.set_canvas.create_text(cx1 - radius / 3, cy, text="∅ (Empty Set)", 
                                        fill=colors["fg"], font=("Arial", 12, "bold"))
    
    elif operation == "symmetric_difference":
        # A △ B
        sym_diff = set_a.symmetric_difference(set_b)
        if sym_diff:
            self.draw_set_elements(set_a - set_b, cx1 - radius / 3, cy, radius * 0.6, color_a_transparent)
            self.draw_set_elements(set_b - set_a, cx2 + radius / 3, cy, radius * 0.6, color_b_transparent)
        else:
            # Draw a clear indication that symmetric difference is empty
            self.set_canvas.create_text((cx1 + cx2) / 2, cy, text="∅ (Empty Set)", 
                                        fill=colors["fg"], font=("Arial", 12, "bold"))
    
    elif operation == "is_subset":
        # Special visualization for subset relationship
        is_subset = set_a.issubset(set_b)
        result_text = "YES" if is_subset else "NO"
        result_color = color_intersection_transparent if is_subset else color_a_transparent
        
        # Draw the result prominently
        self.set_canvas.create_text((cx1 + cx2) / 2, cy - radius / 2, 
                                    text=f"Is A subset of B? {result_text}", 
                                    fill=colors["fg"], font=("Arial", 14, "bold"))
        
        # Draw nested circles if it's a subset
        if is_subset:
            self.set_canvas.delete("circle_a")
            self.set_canvas.delete("circle_b")
            
            # Draw B as the larger circle
            self.set_canvas.create_oval(
                cx2 - radius, cy - radius, 
                cx2 + radius, cy + radius, 
                outline=colors["fg"], width=2, fill=color_b_transparent, tags="circle_b"
            )
            
            # Draw A as a smaller circle inside B
            smaller_radius = radius * 0.6
            self.set_canvas.create_oval(
                cx2 - smaller_radius, cy - smaller_radius, 
                cx2 + smaller_radius, cy + smaller_radius, 
                outline=colors["fg"], width=2, fill=color_a_transparent, tags="circle_a"
            )
            
            # Draw set elements
            self.draw_set_elements(set_b - set_a, cx2, cy - smaller_radius - 20, radius * 0.4, color_b_transparent)
            self.draw_set_elements(set_a, cx2, cy, smaller_radius * 0.8, color_a_transparent)
        else:
            # Show that A has elements outside B
            self.draw_set_elements(set_a - set_b, cx1 - radius / 3, cy, radius * 0.6, color_a_transparent)
    
    elif operation == "is_superset":
        # Special visualization for superset relationship
        is_superset = set_a.issuperset(set_b)
        result_text = "YES" if is_superset else "NO"
        result_color = color_intersection_transparent if is_superset else color_b_transparent
        
        # Draw the result prominently
        self.set_canvas.create_text((cx1 + cx2) / 2, cy - radius / 2, 
                                    text=f"Is A superset of B? {result_text}", 
                                    fill=colors["fg"], font=("Arial", 14, "bold"))
        
        # Draw nested circles if it's a superset
        if is_superset:
            self.set_canvas.delete("circle_a")
            self.set_canvas.delete("circle_b")
            
            # Draw A as the larger circle
            self.set_canvas.create_oval(
                cx1 - radius, cy - radius, 
                cx1 + radius, cy + radius, 
                outline=colors["fg"], width=2, fill=color_a_transparent, tags="circle_a"
            )
            
            # Draw B as a smaller circle inside A
            smaller_radius = radius * 0.6
            self.set_canvas.create_oval(
                cx1 - smaller_radius, cy - smaller_radius, 
                cx1 + smaller_radius, cy + smaller_radius, 
                outline=colors["fg"], width=2, fill=color_b_transparent, tags="circle_b"
            )
            
            # Draw set elements
            self.draw_set_elements(set_a - set_b, cx1, cy - smaller_radius - 20, radius * 0.4, color_a_transparent)
            self.draw_set_elements(set_b, cx1, cy, smaller_radius * 0.8, color_b_transparent)
        else:
            # Show that B has elements outside A
            self.draw_set_elements(set_b - set_a, cx2 + radius / 3, cy, radius * 0.6, color_b_transparent)
    
    elif operation == "is_disjoint":
        # Special visualization for disjointness
        is_disjoint = set_a.isdisjoint(set_b)
        result_text = "YES" if is_disjoint else "NO"
        
        # Draw the result prominently
        self.set_canvas.create_text((cx1 + cx2) / 2, cy - radius / 2, 
                                    text=f"Are A and B disjoint? {result_text}", 
                                    fill=colors["fg"], font=("Arial", 14, "bold"))
        
        if is_disjoint:
            # Draw circles far apart
            separation = radius * 2.5
            
            self.set_canvas.delete("circle_a")
            self.set_canvas.delete("circle_b")
            
            # Draw A
            self.set_canvas.create_oval(
                cx1 - radius - separation/2, cy - radius, 
                cx1 + radius - separation/2, cy + radius, 
                outline=colors["fg"], width=2, fill=color_a_transparent, tags="circle_a"
            )
            
            # Draw B
            self.set_canvas.create_oval(
                cx2 - radius + separation/2, cy - radius, 
                cx2 + radius + separation/2, cy + radius, 
                outline=colors["fg"], width=2, fill=color_b_transparent, tags="circle_b"
            )
            
            # Draw set elements
            self.draw_set_elements(set_a, cx1 - separation/2, cy, radius * 0.8, color_a_transparent)
            self.draw_set_elements(set_b, cx2 + separation/2, cy, radius * 0.8, color_b_transparent)
        else:
            # Show the intersection
            intersection = set_a.intersection(set_b)
            self.draw_set_elements(set_a - set_b, cx1 - radius / 3, cy, radius * 0.6, color_a_transparent)
            self.draw_set_elements(set_b - set_a, cx2 + radius / 3, cy, radius * 0.6, color_b_transparent)
            self.draw_set_elements(intersection, (cx1 + cx2) / 2, cy, radius / 2, color_intersection_transparent)

def create_number_conversion_tab(self):
    # Create a new tab for Number Conversion
    conv_frame = ttk.Frame(self.notebook, style="TFrame", padding="15")
    self.notebook.add(conv_frame, text="Number Conversion")
    
    # ========== ROW 0: "Input Number" label + entry ==========
    lbl_input = ttk.Label(conv_frame, text="Input Number:", style="TLabel")
    lbl_input.grid(row=0, column=0, sticky="w", pady=(0, 5))
    
    entry_input = ttk.Entry(conv_frame, textvariable=self.conv_input_var, width=40)
    entry_input.grid(row=0, column=1, columnspan=3, padx=(0, 10), sticky="ew")
    
    # ========== ROW 1: "From Base" label + radio buttons (common bases + custom) ==========
    lbl_from = ttk.Label(conv_frame, text="From Base:", style="TLabel")
    lbl_from.grid(row=1, column=0, sticky="w", pady=(10, 5))
    
    # Frame to hold the "From Base" radio buttons
    from_bases_frame = ttk.Frame(conv_frame, style="TFrame")
    from_bases_frame.grid(row=1, column=1, columnspan=3, sticky="w", padx=10, pady=(10, 5))
    
    common_bases = [
        ("Binary (2)", "2"),
        ("Octal (8)", "8"),
        ("Decimal (10)", "10"),
        ("Hex (16)", "16")
    ]
    for i, (label, val) in enumerate(common_bases):
        rb = ttk.Radiobutton(from_bases_frame, text=label, value=val, variable=self.from_base_var)
        rb.grid(row=0, column=i, sticky="w", padx=5)
    
    # Custom base for "From Base"
    custom_rb = ttk.Radiobutton(from_bases_frame, text="Custom:", value="custom", variable=self.from_base_var)
    custom_rb.grid(row=1, column=0, sticky="w", pady=(5, 0))
    
    custom_from_entry = ttk.Entry(from_bases_frame, textvariable=self.custom_to_base_var, width=5)
    custom_from_entry.grid(row=1, column=1, sticky="w", pady=(5, 0), padx=(5,0))
    
    # ========== ROW 2: "Convert to" label + checkbuttons + "Convert" button together ==========
    lbl_to = ttk.Label(conv_frame, text="Convert to:", style="TLabel")
    lbl_to.grid(row=2, column=0, sticky="w", pady=(10, 5))
    
    to_bases_frame = ttk.Frame(conv_frame, style="TFrame")
    to_bases_frame.grid(row=2, column=1, columnspan=2, sticky="w", padx=10, pady=(10, 5))
    
    chk_bin = ttk.Checkbutton(to_bases_frame, text="Binary", variable=self.to_binary_var)
    chk_bin.grid(row=0, column=0, sticky="w", padx=5)
    
    chk_oct = ttk.Checkbutton(to_bases_frame, text="Octal", variable=self.to_octal_var)
    chk_oct.grid(row=0, column=1, sticky="w", padx=5)
    
    chk_dec = ttk.Checkbutton(to_bases_frame, text="Decimal", variable=self.to_decimal_var)
    chk_dec.grid(row=0, column=2, sticky="w", padx=5)
    
    chk_hex = ttk.Checkbutton(to_bases_frame, text="Hex", variable=self.to_hex_var)
    chk_hex.grid(row=0, column=3, sticky="w", padx=5)
    
    # Optional custom "to" base
    chk_cust = ttk.Checkbutton(to_bases_frame, text="Custom:", variable=self.to_custom_var)
    chk_cust.grid(row=1, column=0, sticky="w", padx=5, pady=(5, 0))
    
    custom_to_entry = ttk.Entry(to_bases_frame, textvariable=self.custom_to_base_var, width=5)
    custom_to_entry.grid(row=1, column=1, sticky="w", pady=(5, 0))
    
    # Place the "Convert" button in the same row as "Convert to"
    btn_convert = ttk.Button(conv_frame, text="Convert", command=self.calculate_number_conversion)
    # Adjust row=2, col=3 so it’s in the same row but the next column to the right
    btn_convert.grid(row=2, column=3, padx=(10,0), pady=(10,0), sticky="w")
    
    # ========== ROW 3: Results frame ==========
    self.conv_results_frame = ttk.Frame(conv_frame, style="TFrame")
    self.conv_results_frame.grid(row=3, column=0, columnspan=4, pady=(15, 0), sticky="ew")
    
    # ========== ROW 4: Help text ==========
    help_frame = ttk.Frame(conv_frame, style="TFrame")
    help_frame.grid(row=4, column=0, columnspan=4, pady=(20, 0), sticky="ew")
    
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
        inp = self.conv_input_var.get().strip()
        if not inp:
            raise ValueError("Please enter a number to convert.")
        
        # Determine the "from" base
        fbase = self.from_base_var.get()
        if fbase == "custom":
            fbase = self.custom_from_base_var.get()
        fbase = int(fbase)
        if fbase < 2 or fbase > 36:
            raise ValueError("Source base must be between 2 and 36.")
        
        # Convert the input to a decimal integer
        dec_val = int(inp, fbase)
        
        results = []
        
        # Standard conversions
        if self.to_binary_var.get():
            results.append(("Binary(2)", self.convert_standard(dec_val, bin)))
        if self.to_octal_var.get():
            results.append(("Octal(8)", self.convert_standard(dec_val, oct)))
        if self.to_decimal_var.get():
            results.append(("Decimal(10)", str(dec_val)))
        if self.to_hex_var.get():
            results.append(("Hex(16)", self.convert_standard(dec_val, hex, upper=True)))
        
        # Custom target base conversion
        if self.to_custom_var.get():
            cbase = int(self.custom_to_base_var.get())
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
    for w in self.conv_results_frame.winfo_children():
        w.destroy()
    lbl_in = ttk.Label(self.conv_results_frame, text=f"Input: {inp} (Base {fbase})", style="TLabel", font=("Arial",10,"bold"))
    lbl_in.grid(row=0, column=0, sticky="w", pady=(0,10))
    for i,(bn,val) in enumerate(results):
        lbl_b = ttk.Label(self.conv_results_frame, text=f"{bn}:", style="TLabel")
        lbl_b.grid(row=i+1, column=0, sticky="w", pady=(0,5))
        lbl_v = ttk.Label(self.conv_results_frame, text=val, style="TLabel")
        lbl_v.grid(row=i+1, column=1, sticky="w", padx=(10,0), pady=(0,5))
        
def draw_set_elements(self, set_elements, center_x, center_y, max_radius, color):
    """Draw the elements of a set in a circular arrangement."""
    if not set_elements:
        return
    
    num_elements = len(set_elements)
    max_display = 8  # Maximum number of elements to display
    
    if num_elements <= max_display:
        elements_to_display = list(set_elements)
    else:
        # Select a subset of elements to display
        elements_to_display = list(set_elements)[:max_display-1] + ["..."]
    
    # Draw a filled circle as the set background
    self.set_canvas.create_oval(
        center_x - max_radius, center_y - max_radius,
        center_x + max_radius, center_y + max_radius,
        outline="", fill=color
    )
    
    # Draw elements in a circular arrangement
    displayed_count = len(elements_to_display)
    
    # Get text color - use the foreground color from the theme if available
    colors = self.get_theme_colors() if hasattr(self, 'get_theme_colors') else {"fg": "#000000"}
    text_color = colors["fg"]
    
    for i, element in enumerate(elements_to_display):
        # Calculate angle and position
        angle = 2 * math.pi * i / displayed_count
        
        # Adjust radius to keep elements within the circle
        element_radius = max_radius * 0.7
        
        x = center_x + element_radius * math.cos(angle)
        y = center_y + element_radius * math.sin(angle)
        
        # Draw the element text
        element_text = str(element)
        max_text_length = 10  # Truncate text if too long
        if len(element_text) > max_text_length and element_text != "...":
            element_text = element_text[:max_text_length-3] + "..."
        
        self.set_canvas.create_text(x, y, text=element_text, fill=text_color, font=("Arial", 9))

def draw_cartesian_product(self, canvas_width, canvas_height, text_color, is_preview=True):
    """Draw a visualization of the Cartesian product."""
    # For Cartesian product, we'll use a grid visualization
    if is_preview:
        # Just show a grid sample for preview
        width = canvas_width * 0.8
        height = canvas_height * 0.6
        x_start = (canvas_width - width) / 2
        y_start = (canvas_height - height) / 2 + 30  # Extra space for title
        
        # Draw a grid
        grid_size = 5
        cell_width = width / grid_size
        cell_height = height / grid_size
        
        # Draw grid lines
        for i in range(grid_size + 1):
            # Vertical lines
            self.set_canvas.create_line(
                x_start + i * cell_width, y_start,
                x_start + i * cell_width, y_start + height,
                fill=text_color
            )
            
            # Horizontal lines
            self.set_canvas.create_line(
                x_start, y_start + i * cell_height,
                x_start + width, y_start + i * cell_height,
                fill=text_color
            )
        
        # Draw labels
        self.set_canvas.create_text(x_start - 20, y_start + height / 2,
                          text="Set A", fill=text_color, font=("Arial", 10, "bold"))
        self.set_canvas.create_text(x_start + width / 2, y_start - 20,
                          text="Set B", fill=text_color, font=("Arial", 10, "bold"))
        
        # Draw axis arrows
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
        
        # Add explanation text
        self.set_canvas.create_text(canvas_width / 2, canvas_height - 30,
                          text="Cartesian Product: All possible pairs (a,b) where a ∈ A and b ∈ B",
                          fill=text_color, font=("Arial", 9))
    else:
        # Show actual grid with elements
        if not hasattr(self, 'current_set_a') or not hasattr(self, 'current_set_b'):
            # If we don't have actual sets, use preview
            self.draw_cartesian_product(canvas_width, canvas_height, text_color, True)
            return
        
        set_a = self.current_set_a
        set_b = self.current_set_b
        
        # Limit the number of elements to display
        max_elements = 8
        set_a_display = list(set_a)[:max_elements]
        set_b_display = list(set_b)[:max_elements]
        
        if not set_a_display or not set_b_display:
            # If either set is empty, show message
            self.set_canvas.create_text(canvas_width / 2, canvas_height / 2,
                              text="Cartesian Product: ∅ (Empty Set)\n\nOne or both sets are empty",
                              fill=text_color, font=("Arial", 12, "bold"), justify=tk.CENTER)
            return
        
        # Calculate grid dimensions
        width = canvas_width * 0.8
        height = canvas_height * 0.6
        x_start = (canvas_width - width) / 2
        y_start = (canvas_height - height) / 2 + 30  # Extra space for title
        
        # Draw grid
        rows = len(set_b_display)
        cols = len(set_a_display)
        
        cell_width = width / cols
        cell_height = height / rows
        
        # Draw grid lines
        for i in range(cols + 1):
            # Vertical lines
            self.set_canvas.create_line(
                x_start + i * cell_width, y_start,
                x_start + i * cell_width, y_start + height,
                fill=text_color
            )
        
        for i in range(rows + 1):
            # Horizontal lines
            self.set_canvas.create_line(
                x_start, y_start + i * cell_height,
                x_start + width, y_start + i * cell_height,
                fill=text_color
            )
        
        # Draw A elements (column headers)
        for i, a in enumerate(set_a_display):
            a_str = str(a)
            # Truncate if too long
            if len(a_str) > 8:
                a_str = a_str[:5] + "..."
            
            self.set_canvas.create_text(
                x_start + i * cell_width + cell_width / 2,
                y_start - 15,
                text=a_str, fill=text_color, font=("Arial", 9)
            )
        
        # Draw B elements (row headers)
        for i, b in enumerate(set_b_display):
            b_str = str(b)
            # Truncate if too long
            if len(b_str) > 8:
                b_str = b_str[:5] + "..."
            
            self.set_canvas.create_text(
                x_start - 15,
                y_start + i * cell_height + cell_height / 2,
                text=b_str, fill=text_color, font=("Arial", 9)
            )
        
        # Draw ordered pairs in cells
        colors = self.get_theme_colors() if hasattr(self, 'get_theme_colors') else {
            "highlight": "#4a86e8"
        }
        pair_color = colors.get("highlight", "#4a86e8")
        
        for i, a in enumerate(set_a_display):
            for j, b in enumerate(set_b_display):
                pair_text = f"({a},{b})"
                
                # Truncate if too long
                if len(pair_text) > 12:
                    a_str = str(a)
                    b_str = str(b)
                    if len(a_str) > 5:
                        a_str = a_str[:3] + ".."
                    if len(b_str) > 5:
                        b_str = b_str[:3] + ".."
                    pair_text = f"({a_str},{b_str})"
                
                self.set_canvas.create_text(
                    x_start + i * cell_width + cell_width / 2,
                    y_start + j * cell_height + cell_height / 2,
                    text=pair_text, fill=pair_color, font=("Arial", 8)
                )
        
        # Draw axis labels
        self.set_canvas.create_text(x_start - 40, y_start + height / 2,
                          text="Set B", fill=text_color, font=("Arial", 10, "bold"))
        self.set_canvas.create_text(x_start + width / 2, y_start - 35,
                          text="Set A", fill=text_color, font=("Arial", 10, "bold"))
        
        # Add information about total number of pairs
        total_pairs = len(set_a) * len(set_b)
        displayed_pairs = len(set_a_display) * len(set_b_display)
        
        if total_pairs > displayed_pairs:
            self.set_canvas.create_text(canvas_width / 2, canvas_height - 20,
                              text=f"Showing {displayed_pairs} of {total_pairs} total pairs. (Limited display for clarity)",
                              fill=text_color, font=("Arial", 9))
        else:
            self.set_canvas.create_text(canvas_width / 2, canvas_height - 20,
                              text=f"Total pairs: {total_pairs}",
                              fill=text_color, font=("Arial", 9))


# -------------------------
# Logic Operations Tab
# -------------------------

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
    binary_rb = ttk.Radiobutton(input_mode_frame, text="Binary (0s and 1s)", value="binary", variable=self.logic_mode_var, command=lambda: update_logic_interface(self))
    binary_rb.grid(row=0, column=1, sticky="w", padx=(10, 20))
    boolean_rb = ttk.Radiobutton(input_mode_frame, text="Boolean (True/False)", value="boolean", variable=self.logic_mode_var, command=lambda: update_logic_interface(self))
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
    self.logic_a_true_rb = ttk.Radiobutton(self.logic_boolean_frame, text="True", value=True, variable=self.logic_a_true_var)
    self.logic_a_false_rb = ttk.Radiobutton(self.logic_boolean_frame, text="False", value=False, variable=self.logic_a_true_var)
    self.logic_a_true_rb.grid(row=1, column=0, sticky="w", padx=(0,10))
    self.logic_a_false_rb.grid(row=1, column=1, sticky="w")
    boolean_b_label = ttk.Label(self.logic_boolean_frame, text="Input B (Boolean):", style="TLabel")
    boolean_b_label.grid(row=2, column=0, sticky="w", pady=(0,5))
    self.logic_b_true_var = tk.BooleanVar(value=False)
    self.logic_b_true_rb = ttk.Radiobutton(self.logic_boolean_frame, text="True", value=True, variable=self.logic_b_true_var)
    self.logic_b_false_rb = ttk.Radiobutton(self.logic_boolean_frame, text="False", value=False, variable=self.logic_b_true_var)
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

# -------------------------
# Number Conversion Tab
# -------------------------

def create_number_conversion_tab(self):
    """Create the tab for number base conversions."""
    conv_frame = ttk.Frame(self.adv_notebook, style="TFrame", padding="15")
    self.adv_notebook.add(conv_frame, text="Number Conversion")
    
    # Input number
    input_label = ttk.Label(conv_frame, text="Input Number:", style="TLabel")
    input_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
    self.conv_input_var = tk.StringVar()
    input_entry = ttk.Entry(conv_frame, textvariable=self.conv_input_var, width=40)
    input_entry.grid(row=1, column=0, columnspan=3, padx=(0, 10), sticky="ew")
    
    # From base
    from_label = ttk.Label(conv_frame, text="From Base:", style="TLabel")
    from_label.grid(row=2, column=0, sticky="w", pady=(10, 5))
    self.from_base_var = tk.StringVar(value="10")
    # Make sure to create all the base selection UI elements
    bases_frame = ttk.Frame(conv_frame, style="TFrame")
    bases_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(0, 10))
    common_bases = [
        ("Binary (2)", "2"),
        ("Octal (8)", "8"),
        ("Decimal (10)", "10"),
        ("Hexadecimal (16)", "16")
    ]
    for i, (text, value) in enumerate(common_bases):
        rb = ttk.Radiobutton(bases_frame, text=text, value=value, variable=self.from_base_var)
        rb.grid(row=0, column=i, sticky="w", padx=5)