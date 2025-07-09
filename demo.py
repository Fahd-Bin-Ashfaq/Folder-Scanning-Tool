
try:
    with open("G:/Backup/BanoQabil/Excel.pdf", "rb") as file:
        header = file.read(8)
        if header.startswith():
except FileNotFoundError:
    print("❌ File not found. Please check the path.")
