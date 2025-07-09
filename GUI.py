import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from Metadata import meta
from PiaChart import show_filetype_pie_in_frame

selected_folder = ""

def browse_folder():
    global selected_folder
    selected_folder = filedialog.askdirectory()
    if selected_folder:
        folder_label.config(text=f"Selected folder:\n{selected_folder}", fg="#0B5394")
        show_filetype_pie_in_frame(selected_folder, chart_frame)

def sort_by(tree, col, descending):
    data = [(tree.set(child, col), child) for child in tree.get_children('')]
    data.sort(reverse=descending)
    for index, (_, item) in enumerate(data):
        tree.move(item, '', index)
    tree.heading(col, command=lambda: sort_by(tree, col, not descending))

def show_result_advanced(file_types=None, size_range=None, date_filter_option="All", window_title="Metadata Result"):
    if not selected_folder:
        info_label.config(text="⚠️ Please select a folder first!", fg="red")
        return

    result_window = tk.Toplevel(root)
    result_window.title(window_title)
    result_window.geometry("1000x600")
    result_window.configure(bg="#F0F0F0")

    # --- Top Row ---
    top_row = tk.Frame(result_window, bg="#F0F0F0")
    top_row.pack(pady=5, fill="x")

    def export_to_csv():
        import csv
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["File", "Type", "Size", "Accessed", "Modified", "Created"])
            for row_id in tree.get_children():
                writer.writerow(tree.item(row_id)["values"])
        messagebox.showinfo("Export", "Data exported successfully!")

    # Export Button
    tk.Button(top_row, text="Export to CSV", command=export_to_csv,
              bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=10)

    # Spacer
    tk.Frame(top_row, width=30, bg="#F0F0F0").pack(side="left")

    # Centered Label Frame
    center_frame = tk.Frame(top_row, bg="#F0F0F0")
    center_frame.pack(side="left", expand=True)

    info_label_result = tk.Label(center_frame, text="Processing...", font=("Arial", 11),
                                 fg="#FF5722", bg="#F0F0F0")
    info_label_result.pack()

    # Back Button
    tk.Button(top_row, text="Back", command=result_window.destroy,
              bg="#D32F2F", fg="white", font=("Arial", 10, "bold")).pack(side="right", padx=10)

    # Treeview Table
    columns = ("File", "Type", "Size", "Accessed", "Modified", "Created")
    tree = ttk.Treeview(result_window, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col, command=lambda _col=col: sort_by(tree, _col, False))
        tree.column(col, width=150)

    tree.pack(expand=True, fill="both", padx=10, pady=10)

    meta(selected_folder, tree, info_label_result, file_types, size_range, date_filter_option)

def open_filter_window():
    filter_win = tk.Toplevel(root)
    filter_win.title("Advanced Filter")
    filter_win.geometry("300x350")
    filter_win.configure(bg="#F0F0F0")

    # File Type
    tk.Label(filter_win, text="File Type:", bg="#F0F0F0").pack(pady=5)
    type_filter = ttk.Combobox(filter_win, values=["All", "PDF", "Word", "Excel", "PowerPoint"])
    type_filter.current(0)
    type_filter.pack()

    # File Size
    tk.Label(filter_win, text="File Size:", bg="#F0F0F0").pack(pady=5)
    size_filter = ttk.Combobox(filter_win, values=["All", "<1MB", "1–10MB", ">10MB"])
    size_filter.current(0)
    size_filter.pack()

    # Date Modified
    tk.Label(filter_win, text="Date Modified:", bg="#F0F0F0").pack(pady=5)
    date_filter = ttk.Combobox(filter_win, values=["All", "Today", "Yesterday", "Last Week", "Last Month"])
    date_filter.current(0)
    date_filter.pack()

    def apply_filter():
        type_choice = type_filter.get()
        file_types = None
        if type_choice == "PDF":
            file_types = ['.pdf']
        elif type_choice == "Word":
            file_types = ['.doc', '.docx']
        elif type_choice == "Excel":
            file_types = ['.xls', '.xlsx']
        elif type_choice == "PowerPoint":
            file_types = ['.ppt', '.pptx']

        size_choice = size_filter.get()
        size_range = None
        if size_choice == "<1MB":
            size_range = (0, 1024)
        elif size_choice == "1–10MB":
            size_range = (1024, 10240)
        elif size_choice == ">10MB":
            size_range = (10240, float('inf'))

        date_option = date_filter.get()

        show_result_advanced(file_types, size_range, date_option, "Filtered Files")
        filter_win.destroy()

    tk.Button(filter_win, text="Apply", command=apply_filter, bg="#4CAF50", fg="white").pack(pady=10)
    tk.Button(filter_win, text="Back", command=filter_win.destroy, bg="#D32F2F", fg="white").pack(pady=5)

# --- MAIN WINDOW ---
root = tk.Tk()
root.title("📁 Folder Metadata Viewer")
root.geometry("750x700")
root.configure(bg="#F0F0F0")

folder_label = tk.Label(root, text="No folder selected", fg="#0B5394", font=("Arial", 10, "bold"), bg="#F0F0F0")
folder_label.pack(pady=5)

tk.Button(root, text="📁 Browse Folder", command=browse_folder,
          bg="#0B5394", fg="white", font=("Arial", 10)).pack(pady=5)

filter_frame = tk.Frame(root, bg="#F0F0F0")
filter_frame.pack(pady=10)

tk.Button(filter_frame, text="📝 Word", width=15,
          command=lambda: show_result_advanced(['.doc', '.docx'], window_title="Word Files"),
          bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5)

tk.Button(filter_frame, text="📽 PowerPoint", width=15,
          command=lambda: show_result_advanced(['.ppt', '.pptx'], window_title="PowerPoint Files"),
          bg="#4CAF50", fg="white").grid(row=0, column=1, padx=5)

tk.Button(filter_frame, text="📊 Excel", width=15,
          command=lambda: show_result_advanced(['.xls', '.xlsx'], window_title="Excel Files"),
          bg="#4CAF50", fg="white").grid(row=0, column=2, padx=5)

tk.Button(filter_frame, text="📄 PDF", width=15,
          command=lambda: show_result_advanced(['.pdf'], window_title="PDF Files"),
          bg="#4CAF50", fg="white").grid(row=0, column=3, padx=5)

tk.Button(root, text="⚙️ Advanced Filter", width=30,
          command=open_filter_window, bg="#2196F3", fg="white").pack(pady=5)

tk.Button(root, text="📂 Show All Files", width=30,
          command=lambda: show_result_advanced(None, window_title="All Files"),
          bg="#FF9800", fg="white").pack(pady=10)

chart_frame = tk.Frame(root, bg="#F0F0F0")
chart_frame.pack(pady=10)

info_label = tk.Label(root, text="", font=("Arial", 11), fg="green", bg="#F0F0F0")
info_label.pack(pady=5)

root.mainloop()
