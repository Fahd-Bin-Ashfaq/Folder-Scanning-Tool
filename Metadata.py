from datetime import datetime, timedelta
import os
def meta(path, tree_widget, info_label, fileType=None, size_range=None, date_filter_option="All",dateOption="All"):
    total_file = 0
    total_size = 0

    for row in tree_widget.get_children():
        tree_widget.delete(row)

    now = datetime.now()

    # Date filter threshold
    def check_date(modified_time):
        if date_filter_option == "Today":
            return modified_time.date() == now.date()
        elif date_filter_option == "Yesterday":
            return modified_time.date() == (now - timedelta(days=1)).date()
        elif date_filter_option == "Last Week":
            return modified_time >= now - timedelta(days=7)
        elif date_filter_option == "Last Month":
            return modified_time >= now - timedelta(days=30)
        return True  # If "All"

    for root, _, files in os.walk(path):
        for file in files:
            try:
                ext = os.path.splitext(file)[1].lower()
                if fileType and ext not in fileType:
                    continue

                full_path = os.path.join(root, file)
                stat = os.stat(full_path)
                size_kb = stat.st_size // 1024

                # Size filter
                if size_range and not (size_range[0] <= size_kb <= size_range[1]):
                    continue

                modified_time = datetime.fromtimestamp(stat.st_mtime)
                if not check_date(modified_time):
                    continue

                tree_widget.insert("", "end", values=(
                    file, ext, f"{size_kb} KB",
                    datetime.fromtimestamp(stat.st_atime).strftime("%y-%m-%d"),
                    modified_time.strftime("%y-%m-%d"),
                    datetime.fromtimestamp(stat.st_ctime).strftime("%y-%m-%d"),
                ))

                total_file += 1
                total_size += size_kb

            except Exception as e:
                print("Skip File", e)

    info_label.config(text=f"Total Files: {total_file}, Total Size: {total_size} KB")
