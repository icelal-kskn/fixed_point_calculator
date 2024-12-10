import tkinter as tk
from tkinter import ttk, scrolledtext
import requests
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class FixedPointIterationGUI:
    def __init__(self, master):
        self.master = master
        master.title("Fixed-Point Iteration Root Finder")
        master.geometry("800x800")

        # Main Frame with Vertical Scrollbar
        main_frame = tk.Frame(master)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Vertical Scrollbar
        scrollbar = tk.Scrollbar(main_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Canvas for Scrolling
        canvas = tk.Canvas(main_frame, yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=canvas.yview)

        # Frame inside Canvas
        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor='nw')

        # Input Frame
        input_frame = ttk.Frame(frame, padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Function Input
        ttk.Label(input_frame, text="f(x):").grid(row=0, column=0, sticky=tk.W)
        self.function_entry = ttk.Entry(input_frame, width=40)
        self.function_entry.grid(row=0, column=1, columnspan=3, sticky=(tk.W, tk.E))
        self.function_entry.insert(0, "np.sin(x) + x + 1 ")  # Placeholder


        # Initial Guess
        ttk.Label(input_frame, text="Initial Guess (x0):").grid(row=1, column=0, sticky=tk.W)
        self.x0_entry = ttk.Entry(input_frame, width=20)
        self.x0_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))
        self.x0_entry.insert(0, "2")  # Placeholder

        # Tolerance
        ttk.Label(input_frame, text="Tolerance:").grid(row=2, column=0, sticky=tk.W)
        self.tol_entry = ttk.Entry(input_frame, width=20)
        self.tol_entry.grid(row=2, column=1, sticky=(tk.W, tk.E))
        self.tol_entry.insert(0, "1e-6")  # Placeholder

        # Max Iterations
        ttk.Label(input_frame, text="Max Iterations:").grid(row=3, column=0, sticky=tk.W)
        self.max_iter_entry = ttk.Entry(input_frame, width=20)
        self.max_iter_entry.grid(row=3  , column=1, sticky=(tk.W, tk.E))
        self.max_iter_entry.insert(0, "1000")  # Placeholder

        # Solve Button
        solve_button = ttk.Button(input_frame, text="Find Root", command=self.solve)
        solve_button.grid(row=5, column=0, columnspan=4, pady=10)

        # Result Frame with Scrollbar
        self.result_text = scrolledtext.ScrolledText(frame, height=20, width=50)  
        self.result_text.grid(row=1, column=1, sticky=(tk.W, tk.N, tk.S), padx=10)

        # Matplotlib Figure Frame
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas_plot = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas_plot_widget = self.canvas_plot.get_tk_widget()
        self.canvas_plot_widget.grid(row=1, column=0, padx=10, pady=10)

        # Update scroll region
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def solve(self):
        input_data = {
            "function": self.function_entry.get(),
            "x0": float(self.x0_entry.get()),
            "tolerance": float(self.tol_entry.get()),
            "max_iterations": int(self.max_iter_entry.get())
        }

        try:
            response = requests.post('http://localhost:5000/fixed-point-iteration', json=input_data)
            result = response.json()

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, json.dumps(result, indent=2))

            self.plot_iterations(result)

        except Exception as e:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Error: {str(e)}")

    def plot_iterations(self, result):
        self.ax.clear()

        if result.get('success', False): ## Can be show everything but NaN and inf how can be it shown
            iterations = result.get('iterations', [])
            x_values = [iter['x'] for iter in iterations]
            y_values = [iter['f_x'] for iter in iterations]

            self.ax.plot(x_values, y_values, marker='o', linestyle='-', linewidth=2, markersize=8)
            self.ax.set_title('Fixed-Point Iteration Convergence')
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('f(x)')
            self.ax.grid(True)

            for i, (x, y) in enumerate(zip(x_values, y_values)):
                self.ax.annotate(f'Iter {i}', (x, y), textcoords="offset points", xytext=(0,10), ha='center')

            self.canvas_plot.draw()

def main():
    root = tk.Tk()
    gui = FixedPointIterationGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()