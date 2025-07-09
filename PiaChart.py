import os
from collections import Counter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def show_filetype_pie_in_frame(path, container_frame):
    # Clear previous charts
    for widget in container_frame.winfo_children():
        widget.destroy()

    extensions = []

    for root, _, files in os.walk(path):
        for name in files:
            ext = os.path.splitext(name)[1].lower() or "NoExt"
            extensions.append(ext)

    if not extensions:
        return

    counter = Counter(extensions)

    labels = list(counter.keys())
    sizes = list(counter.values())

    fig = Figure(figsize=(5, 5), dpi=100)
    ax = fig.add_subplot(111)
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title("File Types Distribution")
    ax.axis('equal')

    chart_canvas = FigureCanvasTkAgg(fig, master=container_frame)
    chart_canvas.draw()
    chart_canvas.get_tk_widget().pack()
