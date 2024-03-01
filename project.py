import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import sympy
import math


def show_plot():
    # Get the user-inputted function from the entry widget
    user_function = entry_function.get()

    # Create a lambda function from the user input
    custom_function = lambda x, y: eval(user_function)

    # Calculate partial derivatives
    x, y = sympy.symbols("x y")
    fx = sympy.diff(user_function, x)
    fy = sympy.diff(user_function, y)

    # Calculate the Hessian matrix
    fxx = sympy.diff(fx, x)
    fyy = sympy.diff(fy, y)
    fxy = sympy.diff(fx, y)

    # Evaluate partial derivatives at x=0, y=0
    fx_at_zero = fx.subs({x: 0, y: 0})
    fy_at_zero = fy.subs({x: 0, y: 0})
    fxx_at_zero = fxx.subs({x: 0, y: 0})
    fyy_at_zero = fyy.subs({x: 0, y: 0})
    fxy_at_zero = fxy.subs({x: 0, y: 0})

    # Calculate the determinant of the Hessian matrix
    hessian_det_at_zero = fxx_at_zero * fyy_at_zero - fxy_at_zero**2

    # Determine the type of critical point based on the determinant
    if hessian_det_at_zero > 0 and fxx > 0:
        critical_point_type = "Minimo"
        marker_color = "g"  # Green for minimum
    elif hessian_det_at_zero > 0 and fxx < 0:
        critical_point_type = "Maximo"
        marker_color = "r"  # Red for maximum
    else:
        critical_point_type = "Punto silla"
        marker_color = "b"  # Blue for saddle point

    # Display partial derivatives, Hessian matrix, and critical point type as text
    partial_eqs.config(
        text=f"Derivadas parciales :\nfx = {fx}\nfy = {fy}\n\nDeivadas parciales en 0 :\nfx(0, 0) = {fx_at_zero}\nfy(0, 0) = {fy_at_zero}\n\nMatriz Hessiana con fxx, fyy y fxx:\n{[[fxx_at_zero, fxy_at_zero], [fxy_at_zero, fyy_at_zero]]}\n\nPunto critico: {critical_point_type}"
    )

    # Create points for vectors
    x2 = np.linspace(-4, 4, 100)
    y2 = np.linspace(-4, 4, 100)
    x2, y2 = np.meshgrid(x2, y2)

    # Calculate the function values
    z_surface = custom_function(x2, y2)

    # Clear existing plot if it exists
    ax.clear()

    # Surface plot on the same axes
    surface = ax.plot_surface(x2, y2, z_surface, cmap="plasma", alpha=0.8)

    # Plot critical points as markers
    ax.scatter(
        [0],
        [0],
        [custom_function(0, 0)],
        color=marker_color,
        s=100,
        label=critical_point_type,
    )

    # Set labels
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Grafica de: " + user_function)
    ax.legend()

    # Update canvas
    canvas.draw()


# Create Tkinter window
root = Tk()
root.title("Representadora grafica de puntos criticos acordes a la matriz Hessiana")

# Create a subplot for the 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# Entry widget for the user to input the function
entry_label = Label(root, text="Su funcion: ")
entry_label.pack()
entry_function = Entry(root)
entry_function.pack()

# Button to show the plot, partial derivatives, and Hessian matrix
show_button = Button(root, text="Mostrar", command=show_plot)
show_button.pack()

# Display equations of partial derivatives, Hessian matrix, and critical point type as text
partial_eqs = Label(root, text="")
partial_eqs.pack()

# Embed the plot and equations in the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=BOTTOM, fill=BOTH, expand=True)

# Run the Tkinter event loop
root.mainloop()
