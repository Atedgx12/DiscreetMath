import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")  # Set the backend to TkAgg before other imports

import logging
logging.basicConfig(level=logging.WARNING)

# Import the modules
from complex_solver import ComplexSolverApp
import complex_solver_functions
import complex_visualization
import advanced_math_operations
import prime_calculator as number_properties  # Use prime_calculator as number_properties

def assign_advanced_math_functions():
    """Assign functions from advanced_math_operations to ComplexSolverApp."""
    # Main tab function
    ComplexSolverApp.create_advanced_math_tab = advanced_math_operations.create_advanced_math_tab
    
    # Set operations functions
    ComplexSolverApp.create_set_operations_tab = advanced_math_operations.create_set_operations_tab
    ComplexSolverApp.calculate_set_operation = advanced_math_operations.calculate_set_operation
    ComplexSolverApp.display_set_result = advanced_math_operations.display_set_result
    
    # Set visualization functions
    ComplexSolverApp.update_set_visualization_preview = advanced_math_operations.update_set_visualization_preview
    ComplexSolverApp.draw_set_visualization = advanced_math_operations.draw_set_visualization
    ComplexSolverApp.get_set_operation_title = advanced_math_operations.get_set_operation_title
    ComplexSolverApp.preview_venn_diagram = advanced_math_operations.preview_venn_diagram
    ComplexSolverApp.fill_venn_diagram = advanced_math_operations.fill_venn_diagram
    ComplexSolverApp.draw_set_elements = advanced_math_operations.draw_set_elements
    ComplexSolverApp.draw_cartesian_product = advanced_math_operations.draw_cartesian_product
    
    # Logic operations functions
    ComplexSolverApp.create_logic_operations_tab = advanced_math_operations.create_logic_operations_tab
    ComplexSolverApp.update_logic_interface = advanced_math_operations.update_logic_interface
    ComplexSolverApp.calculate_logic_operation = advanced_math_operations.calculate_logic_operation
    ComplexSolverApp.display_logic_result = advanced_math_operations.display_logic_result
    
    # Number conversion functions
    ComplexSolverApp.create_number_conversion_tab = advanced_math_operations.create_number_conversion_tab
    ComplexSolverApp.calculate_number_conversion = advanced_math_operations.calculate_number_conversion
    ComplexSolverApp.display_conversion_results = advanced_math_operations.display_conversion_results
    
def assign_complex_solver_functions():
    """Assign functions from complex_solver_functions to ComplexSolverApp."""
    ComplexSolverApp.solve_complex = complex_solver_functions.solve_complex

def assign_visualization_functions():
    """Assign functions from complex_visualization to ComplexSolverApp."""
    ComplexSolverApp.create_visualization_tab = complex_visualization.create_visualization_tab
    ComplexSolverApp.setup_plot = complex_visualization.setup_plot
    ComplexSolverApp.update_plot = complex_visualization.update_plot
    ComplexSolverApp.add_to_visualization = complex_visualization.add_to_visualization
    ComplexSolverApp.update_legend = complex_visualization.update_legend
    ComplexSolverApp.add_manual_complex = complex_visualization.add_manual_complex
    ComplexSolverApp.clear_visualization = complex_visualization.clear_visualization
    ComplexSolverApp.save_plot = complex_visualization.save_plot

def assign_advanced_math_functions():
    """Assign functions from advanced_math_operations to ComplexSolverApp."""
    ComplexSolverApp.create_advanced_math_tab = advanced_math_operations.create_advanced_math_tab
    ComplexSolverApp.create_set_operations_tab = advanced_math_operations.create_set_operations_tab
    ComplexSolverApp.create_logic_operations_tab = advanced_math_operations.create_logic_operations_tab
    ComplexSolverApp.create_number_conversion_tab = advanced_math_operations.create_number_conversion_tab
    ComplexSolverApp.update_logic_interface = advanced_math_operations.update_logic_interface
    ComplexSolverApp.calculate_set_operation = advanced_math_operations.calculate_set_operation
    ComplexSolverApp.display_set_result = advanced_math_operations.display_set_result
    ComplexSolverApp.calculate_logic_operation = advanced_math_operations.calculate_logic_operation
    ComplexSolverApp.display_logic_result = advanced_math_operations.display_logic_result
    ComplexSolverApp.calculate_number_conversion = advanced_math_operations.calculate_number_conversion
    ComplexSolverApp.display_conversion_results = advanced_math_operations.display_conversion_results

def assign_number_properties_functions():
    """Assign functions from number_properties (prime_calculator) to ComplexSolverApp,
    logging a warning if any expected function is missing."""
    expected_functions = [
        "create_number_properties_tab", "analyze_number", "create_result_row",
        "is_prime", "parse_input", "clear_properties_history", "export_properties_result"
    ]
    for func_name in expected_functions:
        if hasattr(number_properties, func_name):
            setattr(ComplexSolverApp, func_name, getattr(number_properties, func_name))
        else:
            logging.warning(f"{func_name} not found in number_properties")

def create_tabs(app):
    """Create the tabs for the application if the functions exist."""
    # Create visualization tab
    if hasattr(app, "create_visualization_tab"):
        app.create_visualization_tab()
    else:
        logging.warning("Visualization tab function is missing.")

    # Create advanced math tab
    if hasattr(app, "create_advanced_math_tab"):
        app.create_advanced_math_tab()
    else:
        logging.warning("Advanced math tab function is missing.")

    # Create number properties tab if available
    if hasattr(app, "create_number_properties_tab"):
        app.create_number_properties_tab()
    else:
        logging.warning("Number Properties tab not created because create_number_properties_tab is missing.")

# Fixed toggle_dark_mode function to properly handle text colors
def patched_toggle_dark_mode(self):
    """Toggle between light and dark mode with proper text handling."""
    # Toggle the dark mode variable
    self.dark_mode.set(not self.dark_mode.get())
    
    # Update styles based on the new mode
    self.setup_styles()
    
    # Fix: Explicitly set tab text colors to remain black regardless of mode
    self.style.configure('TNotebook.Tab', foreground='black')
    self.style.map('TNotebook.Tab', foreground=[('selected', 'black')])
    
    # Update content frame and root background
    if hasattr(self, 'content_frame'):
        self.content_frame.configure(style="TFrame")
    
    self.root.configure(background=self.get_theme_colors()["bg"])

def main():
    """Run the main application"""
    root = tk.Tk()
    root.title("Mathematical Toolkit")
    root.geometry("900x750")
    
    # Create the application instance
    app = ComplexSolverApp(root)
    
    # Patch the toggle_dark_mode method to fix text color issues
    if hasattr(app, 'toggle_dark_mode'):
        original_toggle = app.toggle_dark_mode
        app.toggle_dark_mode = lambda: patched_toggle_dark_mode(app)
    
    # Create a Notebook widget and assign it to app so that visualization and advanced math functions can add tabs.
    app.notebook = ttk.Notebook(root)
    app.notebook.pack(fill=tk.BOTH, expand=True)
    
    # Assign functions from the different modules
    assign_complex_solver_functions()
    assign_visualization_functions()
    assign_advanced_math_functions()
    assign_number_properties_functions()
    
    # Create the tabs if the functions are available
    create_tabs(app)
    
    # Fix tab text color - ensure black text on tabs
    style = ttk.Style()
    style.configure('TNotebook.Tab', foreground='black')
    style.map('TNotebook.Tab', foreground=[('selected', 'black')])
    
    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()