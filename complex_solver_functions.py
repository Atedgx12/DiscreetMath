import math
import cmath
import tkinter as tk
from tkinter import ttk, messagebox
import logging

# Set up logging for debugging purposes
logging.basicConfig(level=logging.DEBUG)

def solve_complex(self):
    """
    Solve complex number operations and update the GUI with the results.
    
    This function parses input complex numbers (from GUI variables), determines
    the selected operation, performs the computation with optional step-by-step 
    logging, displays the result in both rectangular and polar forms, and adds 
    the operation to history and (optionally) to the visualization.
    """
    # Clear any previous results and steps from the UI
    self.clear_complex_results()
    self.clear_steps()
    
    try:
        # Retrieve inputs and operation
        z1_str = self.first_complex_var.get().strip()
        z2_str = self.second_complex_var.get().strip()
        operation = self.operation_var.get()
        
        if not z1_str:
            messagebox.showerror("Error", "Please enter the first complex number.")
            return
        
        # Parse first complex number
        self.add_step(f"Parsing first complex number: {z1_str}")
        z1 = self.parse_complex_input(z1_str)
        self.add_step(f"z1 = {z1}")
        
        # Initialize variables used in binary operations
        z2 = None
        equation = ""
        operation_text = ""
        result = None
        
        # For binary operations: +, -, *, /, and power (^)
        if operation in ['+', '-', '*', '/', '^']:
            if not z2_str:
                messagebox.showerror("Error", "Please enter the second complex number for binary operations.")
                return
            
            self.add_step(f"Parsing second complex number: {z2_str}")
            z2 = self.parse_complex_input(z2_str)
            self.add_step(f"z2 = {z2}")
            
            # Perform the selected binary operation
            if operation == '+':
                self.add_step(f"Performing addition: {z1} + {z2}")
                result = z1 + z2
                operation_text = "Addition"
                equation = f"({z1}) + ({z2}) = {result}"
                
            elif operation == '-':
                self.add_step(f"Performing subtraction: {z1} - {z2}")
                result = z1 - z2
                operation_text = "Subtraction"
                equation = f"({z1}) - ({z2}) = {result}"
                
            elif operation == '*':
                self.add_step(f"Performing multiplication: {z1} * {z2}")
                result = z1 * z2
                operation_text = "Multiplication"
                equation = f"({z1}) * ({z2}) = {result}"
                # Provide detailed multiplication steps if enabled
                if self.show_steps_var.get():
                    a, b = z1.real, z1.imag
                    c, d = z2.real, z2.imag
                    self.add_step("Using (a+bi) * (c+di) = (ac-bd) + (ad+bc)i")
                    self.add_step(f"a = {a}, b = {b}, c = {c}, d = {d}")
                    real_part = a*c - b*d
                    imag_part = a*d + b*c
                    self.add_step(f"Real part: {a}*{c} - {b}*{d} = {real_part}")
                    self.add_step(f"Imaginary part: {a}*{d} + {b}*{c} = {imag_part}")
                    self.add_step(f"Result = {real_part} + {imag_part}j = {result}")
                
            elif operation == '/':
                if z2 == 0:
                    messagebox.showerror("Error", "Division by zero.")
                    return
                
                self.add_step(f"Performing division: {z1} / {z2}")
                result = z1 / z2
                operation_text = "Division"
                equation = f"({z1}) / ({z2}) = {result}"
                # Detailed division steps if enabled
                if self.show_steps_var.get():
                    a, b = z1.real, z1.imag
                    c, d = z2.real, z2.imag
                    self.add_step("Multiplying numerator and denominator by the conjugate of the denominator")
                    self.add_step(f"(a+bi)/(c+di) = [(a+bi)*(c-di)] / [(c+di)*(c-di)]")
                    self.add_step(f"a = {a}, b = {b}, c = {c}, d = {d}")
                    numerator_real = a*c + b*d
                    numerator_imag = b*c - a*d
                    denominator = c*c + d*d
                    self.add_step(f"Numerator: real = {a}*{c} + {b}*{d} = {numerator_real}, imaginary = {b}*{c} - {a}*{d} = {numerator_imag}")
                    self.add_step(f"Denominator: {c}² + {d}² = {denominator}")
                    self.add_step(f"Result = ({numerator_real} + {numerator_imag}j) / {denominator} = {result}")
                
            elif operation == '^':
                self.add_step(f"Calculating power: {z1} ^ {z2}")
                result = z1 ** z2
                operation_text = "Power"
                equation = f"({z1}) ^ ({z2}) = {result}"
                # Detailed power calculation steps if enabled
                if self.show_steps_var.get():
                    # If exponent is an integer and small, show iterative multiplication
                    if z2.imag == 0 and z2.real.is_integer() and 0 < z2.real <= 5:
                        self.add_step("For integer powers, multiplying z1 by itself repeatedly:")
                        power = int(z2.real)
                        temp = complex(1, 0)
                        for i in range(power):
                            temp_prev = temp
                            temp = temp * z1
                            self.add_step(f"Step {i+1}: {temp_prev} * {z1} = {temp}")
                    else:
                        # General case using the exponential/log form
                        r, theta = cmath.polar(z1)
                        self.add_step("Using formula: z^w = e^(w*ln(z))")
                        self.add_step(f"Convert {z1} to polar form: r = {r}, θ = {theta} rad")
                        self.add_step(f"Then, {z1}^{z2} = e^({z2} * ln({z1}))")
                        self.add_step(f"Result = {result}")
        
        # For unary operations (operations that require only one input)
        else:
            if operation == 'sqrt':
                self.add_step(f"Calculating square root of {z1}")
                result = cmath.sqrt(z1)
                operation_text = "Square Root"
                equation = f"√({z1}) = {result}"
                if self.show_steps_var.get():
                    r, theta = cmath.polar(z1)
                    self.add_step(f"Convert to polar form: {z1} = {r}e^({theta}j)")
                    self.add_step("Square root: √r * e^(θ/2 * j)")
                    self.add_step(f"Result = √{r} * e^({theta/2}j) = {result}")
            
            elif operation == 'abs':
                self.add_step(f"Calculating absolute value (modulus) of {z1}")
                result = abs(z1)
                operation_text = "Absolute Value"
                equation = f"|{z1}| = {result}"
                if self.show_steps_var.get():
                    a, b = z1.real, z1.imag
                    self.add_step(f"Using formula: |a+bi| = √(a² + b²)")
                    self.add_step(f"|{a}+{b}j| = √({a}² + {b}²) = √({a*a} + {b*b}) = {result}")
            
            elif operation == 'conj':
                self.add_step(f"Calculating conjugate of {z1}")
                result = z1.conjugate()
                operation_text = "Conjugate"
                equation = f"conj({z1}) = {result}"
                if self.show_steps_var.get():
                    a, b = z1.real, z1.imag
                    self.add_step(f"Conjugate of {a}+{b}j is {a}-{b}j = {result}")
            
            elif operation == 'polar':
                self.add_step(f"Converting {z1} to polar form")
                r, theta = cmath.polar(z1)
                result = f"{r} < {theta}"
                operation_text = "Conversion to Polar Form"
                equation = f"polar({z1}) = {result} (r < θ, θ in radians)"
                if self.show_steps_var.get():
                    a, b = z1.real, z1.imag
                    self.add_step(f"For a complex number {a}+{b}j, r = √(a²+b²) and θ = atan2(b, a)")
                    self.add_step(f"r = √({a*a} + {b*b}) = {r}")
                    self.add_step(f"θ = atan2({b}, {a}) = {theta} rad ({math.degrees(theta)}°)")
            
            elif operation == 'rect':
                # Convert from polar to rectangular form.
                polar_form = self.parse_polar_form(z1_str)
                if polar_form:
                    self.add_step(f"Converting polar form {z1_str} to rectangular form")
                    result = polar_form
                    operation_text = "Conversion to Rectangular Form"
                    equation = f"rect({z1_str}) = {result}"
                    if self.show_steps_var.get():
                        parts = z1_str.split('<')
                        r = float(parts[0].strip())
                        theta = float(parts[1].strip())
                        self.add_step(f"r = {r}, θ = {theta}")
                        self.add_step(f"Rectangular form: r*cos(θ) + r*sin(θ)j")
                        self.add_step(f"Result = {r*math.cos(theta)} + {r*math.sin(theta)}j = {result}")
                else:
                    messagebox.showerror("Error", "For rect operation, please enter z1 in polar form (r<θ).")
                    return
            
            elif operation == 'sin':
                self.add_step(f"Calculating sine of {z1}")
                result = cmath.sin(z1)
                operation_text = "Sine"
                equation = f"sin({z1}) = {result}"
            
            elif operation == 'cos':
                self.add_step(f"Calculating cosine of {z1}")
                result = cmath.cos(z1)
                operation_text = "Cosine"
                equation = f"cos({z1}) = {result}"
            
            elif operation == 'tan':
                self.add_step(f"Calculating tangent of {z1}")
                result = cmath.tan(z1)
                operation_text = "Tangent"
                equation = f"tan({z1}) = {result}"
            
            elif operation == 'exp':
                self.add_step(f"Calculating exponential of {z1}")
                result = cmath.exp(z1)
                operation_text = "Exponential"
                equation = f"exp({z1}) = {result}"
                if self.show_steps_var.get():
                    a, b = z1.real, z1.imag
                    self.add_step(f"Using Euler's formula: e^(a+bj) = e^a * (cos(b) + j*sin(b))")
                    self.add_step(f"e^{a} * (cos({b}) + j*sin({b}))")
                    self.add_step(f"Result = {math.exp(a)*math.cos(b)} + j*{math.exp(a)*math.sin(b)} = {result}")
            
            elif operation == 'log':
                if z1 == 0:
                    messagebox.showerror("Error", "Cannot compute logarithm of zero.")
                    return
                self.add_step(f"Calculating natural logarithm of {z1}")
                result = cmath.log(z1)
                operation_text = "Natural Logarithm"
                equation = f"ln({z1}) = {result}"
                if self.show_steps_var.get():
                    r, theta = cmath.polar(z1)
                    self.add_step("For a complex number in polar form: ln(r*e^(θj)) = ln(r) + θj")
                    self.add_step(f"r = {r}, θ = {theta}")
                    self.add_step(f"Result = ln({r}) + {theta}j = {result}")
            else:
                messagebox.showerror("Error", "Unknown operation selected.")
                return
        
        # Display the results in the GUI
        display_complex_results(self, operation_text, equation, result)
        
        # Add operation to history
        self.add_to_history(operation_text, equation, result)
        
        # Optionally add operands and result to the visualization
        if hasattr(self, 'add_to_visualization') and self.visualize_var.get():
            if operation in ['+', '-', '*', '/', '^']:
                self.add_to_visualization(f"z1 ({operation_text})", z1)
                self.add_to_visualization(f"z2 ({operation_text})", z2)
            self.add_to_visualization(f"Result ({operation_text})", result)
    
    except Exception as e:
        logging.exception("Error during complex solving")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def display_complex_results(self, operation_text, equation, result):
    """
    Display the result of the complex operation in the designated results frame.
    
    For complex results, both rectangular and polar forms are shown.
    For non-complex (real) results, a single value is displayed.
    """
    # Clear previous results (if any)
    for widget in self.complex_results_frame.winfo_children():
        widget.destroy()
    
    # Display header and equation
    results_header = ttk.Label(self.complex_results_frame, text=f"Complex {operation_text} Result:", 
                               style="Header.TLabel")
    results_header.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")
    
    equation_label = ttk.Label(self.complex_results_frame, text=equation, style="TLabel", font=("Arial", 12))
    equation_label.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="w")
    
    # Display results based on type
    if isinstance(result, complex):
        # Rectangular form
        rect_label = ttk.Label(self.complex_results_frame, text="Rectangular form:", style="TLabel")
        rect_label.grid(row=2, column=0, sticky="w", pady=(5, 0))
        rect_result = ttk.Label(self.complex_results_frame, text=f"{result.real} + {result.imag}j", 
                                  style="Result.TLabel", font=("Arial", 12))
        rect_result.grid(row=2, column=1, sticky="w", pady=(5, 0), padx=(10, 0))
        
        # Polar form
        r, theta = cmath.polar(result)
        polar_label = ttk.Label(self.complex_results_frame, text="Polar form:", style="TLabel")
        polar_label.grid(row=3, column=0, sticky="w", pady=(5, 0))
        polar_result = ttk.Label(self.complex_results_frame, 
                                 text=f"{r} < {theta} rad (≈ {math.degrees(theta)}°)", 
                                 style="Result.TLabel", font=("Arial", 12))
        polar_result.grid(row=3, column=1, sticky="w", pady=(5, 0), padx=(10, 0))
        
        # Modulus
        mod_label = ttk.Label(self.complex_results_frame, text="Modulus:", style="TLabel")
        mod_label.grid(row=4, column=0, sticky="w", pady=(5, 0))
        mod_result = ttk.Label(self.complex_results_frame, text=f"{abs(result)}", 
                               style="Result.TLabel", font=("Arial", 12))
        mod_result.grid(row=4, column=1, sticky="w", pady=(5, 0), padx=(10, 0))
        
        # Argument
        arg_label = ttk.Label(self.complex_results_frame, text="Argument:", style="TLabel")
        arg_label.grid(row=5, column=0, sticky="w", pady=(5, 0))
        arg_result = ttk.Label(self.complex_results_frame, 
                               text=f"{theta} rad (≈ {math.degrees(theta)}°)", 
                               style="Result.TLabel", font=("Arial", 12))
        arg_result.grid(row=5, column=1, sticky="w", pady=(5, 0), padx=(10, 0))
    else:
        # For real results (e.g. absolute value)
        value_label = ttk.Label(self.complex_results_frame, text="Result:", style="TLabel")
        value_label.grid(row=2, column=0, sticky="w", pady=(5, 0))
        value_result = ttk.Label(self.complex_results_frame, text=f"{result}", 
                                 style="Result.TLabel", font=("Arial", 12))
        value_result.grid(row=2, column=1, sticky="w", pady=(5, 0), padx=(10, 0))
