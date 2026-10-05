import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# 1) Page setup
st.set_page_config(page_title="Quadratic Explorer")
st.title("Quadratic Explorer")
st.write(
    "Adjust a, b and c in the sidebar to see the graph of "
    "y = ax² + bx + c, its vertex and its real roots."
)

# 2) INPUT
with st.sidebar:
    st.header("Parameters")
    a = st.slider("a", -5.0, 5.0, 1.0, 0.5)
    b = st.slider("b", -10.0, 10.0, -2.0, 0.5)
    c = st.slider("c", -10.0, 10.0, -3.0, 0.5)
    x_min, x_max = st.slider("x range", -20.0, 20.0, (-6.0, 6.0), 0.5)
    show_table = st.checkbox("Show data table", value=True)

# Input validation
if a == 0:
    st.warning("a must not be 0, otherwise this is a straight line. Please choose a ≠ 0.")
    st.stop()
if x_max <= x_min:
    st.error("x range is invalid: the minimum must be less than the maximum.")
    st.stop()

# 3) CALCULATION
x_vertex = -b / (2 * a)
y_vertex = a * x_vertex**2 + b * x_vertex + c
disc = b**2 - 4 * a * c

roots = []
if disc >= 0:
    root1 = (-b - np.sqrt(disc)) / (2 * a)
    root2 = (-b + np.sqrt(disc)) / (2 * a)
    roots = sorted({float(root1), float(root2)})

x = np.linspace(x_min, x_max, 401)
y = a * x**2 + b * x + c
data = pd.DataFrame({"x": x, "y": y})

# 4) OUTPUT
st.latex(f"y = {a:g}x^2 {b:+g}x {c:+g}")

col1, col2, col3 = st.columns(3)
col1.metric("Vertex", f"({x_vertex:.2f}, {y_vertex:.2f})")
col2.metric("Discriminant", f"{disc:.2f}")
col3.metric("Real roots", len(roots))

if len(roots) == 0:
    st.info("Discriminant < 0: the parabola does not cross the x-axis (no real roots).")
elif len(roots) == 1:
    st.info(f"Discriminant = 0: one repeated root at x = {roots[0]:.2f}")
else:
    st.info(f"Two real roots: x = {roots[0]:.2f} and x = {roots[1]:.2f}")

fig, ax = plt.subplots()
ax.plot(x, y, color="#123f6c", linewidth=2, label="y = ax² + bx + c")
ax.axhline(0, color="gray", linewidth=1)
if x_min <= x_vertex <= x_max:
    ax.scatter([x_vertex], [y_vertex], color="#dc8d29", zorder=3, label="Vertex")
root_in_range = [r for r in roots if x_min <= r <= x_max]
if root_in_range:
    ax.scatter(root_in_range, [0] * len(root_in_range), color="red", zorder=3, label="Roots")
ax.set(xlabel="x", ylabel="y", title="Quadratic function")
ax.grid(alpha=0.25)
ax.legend()
st.pyplot(fig)
plt.close(fig)

# 5) TABLE / DOWNLOAD
if show_table:
    st.dataframe(data.round(3), hide_index=True)

csv_bytes = data.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download CSV",
    csv_bytes,
    file_name="quadratic.csv",
    mime="text/csv",
)
