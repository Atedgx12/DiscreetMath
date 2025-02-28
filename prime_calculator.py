import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math
import cmath
import fractions
import re
import logging

logging.basicConfig(level=logging.DEBUG)

def create_number_properties_tab(self):
    """Create the Number Properties tab with the analyzer functionality and scrolling."""
    # Create the outer frame for the tab
    props_outer = ttk.Frame(self.notebook, style="TFrame", padding="20")
    self.notebook.add(props_outer, text="Number Properties")
    
    # Create a canvas and scrollbar for scrolling
    canvas = tk.Canvas(props_outer, borderwidth=0, background=self.style.lookup("TFrame", "background"))
    v_scroll = ttk.Scrollbar(props_outer, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=v_scroll.set)
    
    # Pack scrollbar and canvas
    v_scroll.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    
    # Create a frame inside the canvas for the content
    props_frame = ttk.Frame(canvas, style="TFrame")
    props_frame.bind(
        "<Configure>",
        lambda event: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=props_frame, anchor="nw")
    
    # Header
    header_frame = ttk.Frame(props_frame, style="TFrame")
    header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
    header_label = ttk.Label(header_frame, text="Number Property Analyzer", style="Header.TLabel")
    header_label.grid(row=0, column=0, sticky="w")
    
    # Toggle dark mode button if the method exists
    if hasattr(self, 'toggle_dark_mode'):
        dark_mode_btn = ttk.Button(header_frame, text="Toggle Dark Mode", command=self.toggle_dark_mode)
        dark_mode_btn.grid(row=0, column=1, sticky="e")
    
    header_frame.columnconfigure(0, weight=1)
    
    # Input frame
    input_frame = ttk.Frame(props_frame, style="TFrame")
    input_frame.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky="ew")
    
    # Input label
    input_label = ttk.Label(input_frame, text="Enter a number (integer, decimal, fraction, or complex):", style="TLabel")
    input_label.grid(row=0, column=0, pady=(0, 5), sticky="w")
    
    # Input entry
    self.num_props_input_var = tk.StringVar()
    self.num_props_input_entry = ttk.Entry(input_frame, textvariable=self.num_props_input_var, width=40)
    self.num_props_input_entry.grid(row=1, column=0, padx=(0, 10), sticky="ew")
    
    # Analyze button
    analyze_button = ttk.Button(input_frame, text="Analyze", command=self.analyze_number)
    analyze_button.grid(row=1, column=1, sticky="w")
    
    # Configure grid to expand with window
    input_frame.columnconfigure(0, weight=1)
    
    # Results frame
    self.prop_results_frame = ttk.Frame(props_frame, style="TFrame")
    self.prop_results_frame.grid(row=2, column=0, columnspan=2, pady=(0, 20), sticky="ew")
    
    # History and export buttons frame
    buttons_frame = ttk.Frame(props_frame, style="TFrame")
    buttons_frame.grid(row=3, column=0, columnspan=2, pady=(0, 20), sticky="ew")
    
    # Add buttons for history operations
    clear_history_btn = ttk.Button(buttons_frame, text="Clear History", command=self.clear_properties_history)
    clear_history_btn.grid(row=0, column=0, padx=(0, 10))
    
    export_btn = ttk.Button(buttons_frame, text="Export Results", command=self.export_properties_result)
    export_btn.grid(row=0, column=1)
    
    # Help text frame
    help_frame = ttk.Frame(props_frame, style="TFrame")
    help_frame.grid(row=4, column=0, columnspan=2, sticky="ew")
    
    help_label = ttk.Label(help_frame, text="Input Examples:", style="TLabel", font=("Arial", 10, "bold"))
    help_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
    
    examples = [
        "• Integers: 42, -7, 0",
        "• Decimals: 3.14, -0.5",
        "• Fractions: 2/3, -4/7",
        "• Complex Numbers: 2+3j, 4-2j",
        "• Mixed Fractions: 1 1/2 (enter as 1.5 or 3/2)"
    ]
    
    for i, example in enumerate(examples):
        example_label = ttk.Label(help_frame, text=example, style="TLabel")
        example_label.grid(row=i+1, column=0, sticky="w")
    
    # Bind Enter key to analyze_number function
    self.num_props_input_entry.bind("<Return>", lambda event: self.analyze_number())
    
    # Make sure the frame has a proper width (to prevent scrolling issues)
    props_frame.update_idletasks()
    canvas.config(width=props_frame.winfo_width())
    
    
def clear_properties_history(self):
    """Clear the history of analyzed numbers."""
    if hasattr(self, 'history'):
        self.history.clear()
        messagebox.showinfo("History", "Analysis history has been cleared.")
    else:
        # Initialize history if it doesn't exist
        self.history = []

def export_properties_result(self):
    """Export the analysis results to a text file."""
    try:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Export Number Properties"
        )
        if not file_path:
            return
        
        # Check if we have a history to export
        if not hasattr(self, 'history') or not self.history:
            messagebox.showinfo("Export", "No analysis history available to export.")
            return
        
        with open(file_path, "w") as f:
            f.write("Number Properties Analysis\n")
            f.write("=========================\n\n")
            for entry in self.history:
                f.write(f"{entry}\n")
        
        messagebox.showinfo("Export", f"Analysis history exported successfully to {file_path}")
        
    except Exception as e:
        messagebox.showerror("Export Error", str(e))

def create_result_row(self, row, property_name, is_true):
    """Create a row in the results frame with property name and Yes/No indicator."""
    style = "Yes.TLabel" if is_true else "No.TLabel"
    value = "Yes" if is_true else "No"
    
    # Property name
    property_label = ttk.Label(self.prop_results_frame, text=f"{property_name}:", style="Result.TLabel")
    property_label.grid(row=row, column=0, sticky="w", padx=(0, 10), pady=3)
    
    # Value label with colored background
    value_frame = ttk.Frame(self.prop_results_frame, style=style)
    value_frame.grid(row=row, column=1, sticky="w", pady=3)
    value_label = ttk.Label(value_frame, text=value, style=style, padding=(10, 3))
    value_label.pack()
    
    return row + 1

def is_prime(self, n):
    """Check if a number is prime."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def parse_input(self, input_str):
    """
    Parse a string into a number (integer, float, fraction, or complex).
    Returns a tuple containing the parsed number and its type.
    """
    # Remove spaces
    input_str = input_str.replace(" ", "")
    
    # Check if it's a complex number
    if 'j' in input_str or 'i' in input_str:
        # Replace 'i' with 'j' for Python's complex number notation
        input_str = input_str.replace('i', 'j')
        try:
            # Try to evaluate it as a complex number
            num = complex(eval(input_str))
            return num, "complex"
        except:
            raise ValueError("Invalid complex number format.")
    
    # Check if it's a fraction
    if '/' in input_str:
        try:
            # Try to parse as a fraction
            parts = input_str.split('/')
            if len(parts) == 2:
                numerator = float(eval(parts[0]))
                denominator = float(eval(parts[1]))
                if denominator == 0:
                    raise ValueError("Division by zero.")
                return numerator / denominator, "fraction"
            else:
                raise ValueError("Invalid fraction format.")
        except Exception as e:
            if str(e) == "Division by zero.":
                raise ValueError("Division by zero.")
            raise ValueError("Invalid fraction format.")
    
    # Try to evaluate as a regular number
    try:
        num = float(eval(input_str))
        return num, "number"
    except:
        raise ValueError("Invalid number format.")

def analyze_number(self):
    """
    Analyze the properties of the input number and display the results.
    This function handles integers, floats, fractions, and complex numbers.
    """
    # Clear previous results
    for widget in self.prop_results_frame.winfo_children():
        widget.destroy()
    
    try:
        # Get the input string
        input_str = self.num_props_input_var.get().strip() if hasattr(self, 'num_props_input_var') else self.input_var.get().strip()
        
        if not input_str:
            messagebox.showerror("Error", "Please enter a number.")
            return
        
        # Parse the input
        num, num_type = self.parse_input(input_str)
        
        # Display the value being analyzed
        value_label = ttk.Label(self.prop_results_frame, text=f"Results for: {num}", style="Header.TLabel")
        value_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")
        
        row = 1
        
        # Basic classifications
        is_complex = isinstance(num, complex) and num.imag != 0
        is_real = isinstance(num, (int, float)) or (isinstance(num, complex) and num.imag == 0)
        
        # If it's a complex number with imaginary part, we only analyze the complex property
        if is_complex:
            row = self.create_result_row(row, "Complex Number", True)
            row = self.create_result_row(row, "Real Number", False)
            
            # Add to history
            if hasattr(self, 'history'):
                self.history.append(f"Number: {num} - Complex Number: Yes, Real Number: No")
            
            return
        
        # For real numbers, extract the real part if it's a complex with imag=0
        if isinstance(num, complex):
            num = num.real
        
        # Check if it's an integer
        is_integer = num.is_integer() if isinstance(num, float) else True
        
        # Check if it's rational or irrational
        try:
            fraction = fractions.Fraction(num).limit_denominator(1000)
            is_rational = abs(num - fraction.numerator / fraction.denominator) < 1e-10
        except:
            is_rational = is_integer
        
        is_irrational = is_real and not is_rational
        
        # For integers only
        if is_integer:
            num_int = int(num)
            is_whole = num_int >= 0
            is_natural = num_int > 0
            is_positive = num_int > 0
            is_negative = num_int < 0
            is_zero = num_int == 0
            is_even = num_int % 2 == 0
            is_odd = num_int % 2 != 0
            is_prime_number = is_natural and self.is_prime(num_int)
            is_composite = is_natural and not is_prime_number and num_int > 1
        else:
            is_whole = False
            is_natural = False
            is_positive = num > 0
            is_negative = num < 0
            is_zero = num == 0
            is_even = False
            is_odd = False
            is_prime_number = False
            is_composite = False
        
        # Create result rows for all properties
        row = self.create_result_row(row, "Complex Number", is_complex)
        row = self.create_result_row(row, "Real Number", is_real)
        row = self.create_result_row(row, "Rational Number", is_rational)
        row = self.create_result_row(row, "Irrational Number", is_irrational)
        row = self.create_result_row(row, "Integer", is_integer)
        row = self.create_result_row(row, "Whole Number", is_whole)
        row = self.create_result_row(row, "Natural Number", is_natural)
        row = self.create_result_row(row, "Positive", is_positive)
        row = self.create_result_row(row, "Negative", is_negative)
        row = self.create_result_row(row, "Zero", is_zero)
        row = self.create_result_row(row, "Even", is_even)
        row = self.create_result_row(row, "Odd", is_odd)
        row = self.create_result_row(row, "Prime", is_prime_number)
        row = self.create_result_row(row, "Composite", is_composite)
        
        # Add to history
        if hasattr(self, 'history'):
            result_summary = f"Number: {num} - "
            result_summary += f"Real: {'Yes' if is_real else 'No'}, "
            result_summary += f"Rational: {'Yes' if is_rational else 'No'}, "
            result_summary += f"Integer: {'Yes' if is_integer else 'No'}, "
            result_summary += f"Positive: {'Yes' if is_positive else 'No'}, "
            if is_integer and is_natural:
                result_summary += f"Prime: {'Yes' if is_prime_number else 'No'}"
            self.history.append(result_summary)
        
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        logging.exception("Error during number analysis")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")