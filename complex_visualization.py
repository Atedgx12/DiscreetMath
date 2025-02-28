import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math
import cmath
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# -----------------------------------------------------------------------------
# Fallback Helper: Parse a complex number from a string if self.parse_complex_input isn't available.
# This function supports inputs like "3+4j", "3 + 4j", or even "3,4"
# -----------------------------------------------------------------------------
def default_parse_complex_input(input_str):
    """
    Parse a string into a complex number.
    Accepts formats like '3+4j', '3 + 4j', or '3,4' (interpreting comma as separator).
    Raises ValueError on invalid input.
    """
    try:
        # Remove spaces
        input_str = input_str.strip().replace(' ', '')
        # If comma separated, replace with '+' and append 'j'
        if ',' in input_str:
            parts = input_str.split(',')
            if len(parts) != 2:
                raise ValueError("Invalid format. Expected two parts separated by a comma.")
            real, imag = parts
            # Interpret as a complex number: real + imag*j
            return complex(float(real), float(imag))
        else:
            # Directly try conversion using Python's complex() conversion.
            return complex(input_str)
    except Exception as e:
        logging.error(f"Failed to parse complex input '{input_str}': {e}")
        raise ValueError("Invalid complex number format. Please enter like '3+4j' or '3,4'.")

# -----------------------------------------------------------------------------
# Helper for Legend Entry Creation
# -----------------------------------------------------------------------------
def create_legend_entry(parent, label, number, color):
    """
    Create and return a legend entry in the parent widget.
    """
    # Create a small canvas as a color indicator
    color_indicator = tk.Canvas(parent, width=15, height=15, bg=color, highlightthickness=0)
    color_indicator.grid(row=parent.grid_size()[1], column=0, padx=(10, 5), pady=2)
    
    text = f"{label}: {number.real:.3g} + {number.imag:.3g}j"
    text_label = ttk.Label(parent, text=text, style="TLabel")
    text_label.grid(row=parent.grid_size()[1]-1, column=1, sticky="w", padx=(0, 10), pady=2)

# -----------------------------------------------------------------------------
# Visualization Tab Creation and Plot Management
# -----------------------------------------------------------------------------
def create_visualization_tab(self):
    """Create the Visualization tab for complex number plotting."""
    vis_frame = ttk.Frame(self.notebook, style="TFrame", padding="20")
    self.notebook.add(vis_frame, text="Visualization")
    
    # Header
    vis_header = ttk.Label(vis_frame, text="Complex Number Visualization", style="Header.TLabel")
    vis_header.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky="w")
    
    # Left-side Controls Frame
    controls_frame = ttk.Frame(vis_frame, style="TFrame")
    controls_frame.grid(row=1, column=0, sticky="nw", padx=(0, 20))
    
    # Legend Frame
    self.legend_frame = ttk.Frame(controls_frame, style="TFrame", relief="solid", borderwidth=1)
    self.legend_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
    legend_label = ttk.Label(self.legend_frame, text="Legend:", style="TLabel", font=("Arial", 10, "bold"))
    legend_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
    # (Legend entries will be added later.)
    
    # Display Options
    show_grid_label = ttk.Label(controls_frame, text="Display Options:", style="TLabel", font=("Arial", 10, "bold"))
    show_grid_label.grid(row=1, column=0, sticky="w", pady=(0, 5))
    
    self.show_grid_var = tk.BooleanVar(value=True)
    show_grid_check = ttk.Checkbutton(controls_frame, text="Show grid", variable=self.show_grid_var,
                                      command=self.update_plot)
    show_grid_check.grid(row=2, column=0, sticky="w", padx=10)
    
    self.show_unit_circle_var = tk.BooleanVar(value=True)
    show_unit_circle_check = ttk.Checkbutton(controls_frame, text="Show unit circle", 
                                            variable=self.show_unit_circle_var,
                                            command=self.update_plot)
    show_unit_circle_check.grid(row=3, column=0, sticky="w", padx=10)
    
    self.show_arrow_var = tk.BooleanVar(value=True)
    show_arrow_check = ttk.Checkbutton(controls_frame, text="Show arrows from origin", 
                                      variable=self.show_arrow_var,
                                      command=self.update_plot)
    show_arrow_check.grid(row=4, column=0, sticky="w", padx=10)
    
    # Manual Complex Number Addition
    manual_add_label = ttk.Label(controls_frame, text="Add Complex Number:", style="TLabel", font=("Arial", 10, "bold"))
    manual_add_label.grid(row=5, column=0, sticky="w", pady=(20, 5))
    
    manual_frame = ttk.Frame(controls_frame, style="TFrame")
    manual_frame.grid(row=6, column=0, sticky="ew")
    self.manual_complex_var = tk.StringVar()
    manual_complex_entry = ttk.Entry(manual_frame, textvariable=self.manual_complex_var, width=15)
    manual_complex_entry.grid(row=0, column=0, padx=(0, 5))
    add_manual_button = ttk.Button(manual_frame, text="Add", command=self.add_manual_complex)
    add_manual_button.grid(row=0, column=1)
    
    # Clear and Save Buttons
    clear_button = ttk.Button(controls_frame, text="Clear All Points", command=self.clear_visualization)
    clear_button.grid(row=7, column=0, sticky="ew", pady=(20, 0))
    
    save_plot_button = ttk.Button(controls_frame, text="Save Plot as Image", command=self.save_plot)
    save_plot_button.grid(row=8, column=0, sticky="ew", pady=(10, 0))
    
    # Plot Area Frame
    self.plot_frame = ttk.Frame(vis_frame, style="TFrame")
    self.plot_frame.grid(row=1, column=1, rowspan=2, sticky="nsew")
    vis_frame.columnconfigure(1, weight=1)
    vis_frame.rowconfigure(1, weight=1)
    
    # Retrieve theme colors via get_theme_colors method if available.
    colors = self.get_theme_colors() if hasattr(self, 'get_theme_colors') else {
        "bg": "#f0f0f0", "fg": "#000000", "highlight": "#4a86e8"
    }
    
    # Create matplotlib figure and canvas with theme-aware colors
    self.figure = Figure(figsize=(6, 6), dpi=100, facecolor=colors["bg"])
    self.plot = self.figure.add_subplot(111)
    self.plot.set_facecolor(colors["bg"])
    self.plot.tick_params(colors=colors["fg"], labelcolor=colors["fg"])
    for spine in self.plot.spines.values():
        spine.set_color(colors["fg"])
    self.plot.xaxis.label.set_color(colors["fg"])
    self.plot.yaxis.label.set_color(colors["fg"])
    self.plot.title.set_color(colors["fg"])
    
    self.canvas = FigureCanvasTkAgg(self.figure, self.plot_frame)
    self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame)
    self.toolbar.update()
    
    # Initialize storage for complex numbers and configure a color palette.
    self.complex_numbers = {}  # Dictionary mapping label -> (complex number, color)
    self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
                   '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    self.color_index = 0
    
    # Initial plot setup.
    self.setup_plot()

def setup_plot(self):
    """Set up or reinitialize the plot with the current theme and settings."""
    # Retrieve current theme colors.
    colors = self.get_theme_colors() if hasattr(self, 'get_theme_colors') else {
        "bg": "#f0f0f0", "fg": "#000000", "highlight": "#4a86e8"
    }
    
    self.plot.clear()
    self.plot.set_facecolor(colors["bg"])
    self.figure.set_facecolor(colors["bg"])
    self.plot.tick_params(colors=colors["fg"], labelcolor=colors["fg"])
    for spine in self.plot.spines.values():
        spine.set_color(colors["fg"])
    self.plot.xaxis.label.set_color(colors["fg"])
    self.plot.yaxis.label.set_color(colors["fg"])
    self.plot.title.set_color(colors["fg"])
    
    # Draw central axes.
    self.plot.axhline(y=0, color=colors["fg"], linestyle='-', alpha=0.3)
    self.plot.axvline(x=0, color=colors["fg"], linestyle='-', alpha=0.3)
    
    if self.show_grid_var.get():
        self.plot.grid(True, alpha=0.3, color=colors["fg"])
    
    if self.show_unit_circle_var.get():
        circle = plt.Circle((0, 0), 1, fill=False, color=colors["highlight"], linestyle='--', alpha=0.5)
        self.plot.add_artist(circle)
    
    self.plot.set_aspect('equal')
    self.plot.set_xlabel('Real')
    self.plot.set_ylabel('Imaginary')
    self.plot.set_title('Complex Plane')
    
    # Update canvas with the new plot.
    self.canvas.draw()

def update_plot(self):
    """Update the plot to reflect current settings and drawn complex numbers."""
    self.setup_plot()
    colors = self.get_theme_colors() if hasattr(self, 'get_theme_colors') else {
        "bg": "#f0f0f0", "fg": "#000000", "highlight": "#4a86e8"
    }
    
    # Plot each stored complex number.
    for label, (number, color) in self.complex_numbers.items():
        self.plot.scatter(number.real, number.imag, color=color, s=50, zorder=5)
        self.plot.annotate(label, (number.real, number.imag), 
                           xytext=(5, 5), textcoords='offset points',
                           color=colors["fg"])
        if self.show_arrow_var.get():
            self.plot.arrow(0, 0, number.real, number.imag, 
                            head_width=0.1, head_length=0.1, fc=color, ec=color, alpha=0.6)
    
    # Auto-adjust axis limits to ensure all points are visible.
    if self.complex_numbers:
        real_values = [z.real for _, (z, _) in self.complex_numbers.items()]
        imag_values = [z.imag for _, (z, _) in self.complex_numbers.items()]
        if len(real_values) > 0 and len(imag_values) > 0:
            real_range = max(real_values) - min(real_values)
            imag_range = max(imag_values) - min(imag_values)
            margin_real = max(0.5, real_range * 0.2)
            margin_imag = max(0.5, imag_range * 0.2)
            x_min = min(real_values + [-1]) - margin_real
            x_max = max(real_values + [1]) + margin_real
            y_min = min(imag_values + [-1]) - margin_imag
            y_max = max(imag_values + [1]) + margin_imag
            self.plot.set_xlim(x_min, x_max)
            self.plot.set_ylim(y_min, y_max)
    
    self.canvas.draw()

def add_to_visualization(self, label, complex_num):
    """
    Add a complex number with a given label to the visualization.
    Assigns a color from the palette, updates the legend, and refreshes the plot.
    """
    color = self.colors[self.color_index % len(self.colors)]
    self.color_index += 1
    self.complex_numbers[label] = (complex_num, color)
    self.update_legend()
    # Optionally switch to the visualization tab if desired.
    if hasattr(self, 'visualize_var') and self.visualize_var.get():
        self.notebook.select(1)
    self.update_plot()

def update_legend(self):
    """Update the legend to display all added complex numbers."""
    # Clear all legend entries except the header.
    for widget in self.legend_frame.winfo_children():
        grid_info = widget.grid_info()
        if int(grid_info.get("row", 0)) > 0:
            widget.destroy()
    
    # Add new legend entries.
    row = 1
    for label, (number, color) in self.complex_numbers.items():
        # Create each legend entry using the helper function.
        legend_entry_frame = ttk.Frame(self.legend_frame, style="TFrame")
        legend_entry_frame.grid(row=row, column=0, columnspan=2, sticky="w", padx=10, pady=2)
        # Color indicator
        color_indicator = tk.Canvas(legend_entry_frame, width=15, height=15, bg=color, highlightthickness=0)
        color_indicator.pack(side="left", padx=(0,5))
        # Label text
        text = f"{label}: {number.real:.3g} + {number.imag:.3g}j"
        text_label = ttk.Label(legend_entry_frame, text=text, style="TLabel")
        text_label.pack(side="left")
        row += 1

def add_manual_complex(self):
    """Add a manually entered complex number to the visualization."""
    try:
        input_str = self.manual_complex_var.get().strip()
        if not input_str:
            return
        # Use self.parse_complex_input if available, else use our default helper.
        if hasattr(self, "parse_complex_input"):
            complex_num = self.parse_complex_input(input_str)
        else:
            complex_num = default_parse_complex_input(input_str)
        label = f"Manual {len(self.complex_numbers) + 1}"
        self.add_to_visualization(label, complex_num)
        self.manual_complex_var.set("")  # Clear the input field.
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        logging.exception("Unexpected error in add_manual_complex")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def clear_visualization(self):
    """Clear all complex numbers from the visualization."""
    self.complex_numbers = {}
    self.color_index = 0
    self.update_legend()
    self.update_plot()

def save_plot(self):
    """Save the current plot as an image file."""
    try:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"), 
                ("JPEG files", "*.jpg"), 
                ("PDF files", "*.pdf"),
                ("All files", "*.*")
            ],
            title="Save Plot As"
        )
        if not file_path:
            return
        self.figure.savefig(file_path, dpi=300, bbox_inches='tight')
        messagebox.showinfo("Save Successful", f"Plot saved to {file_path}")
    except Exception as e:
        logging.exception("Failed to save plot")
        messagebox.showerror("Save Error", f"Could not save plot: {e}")
