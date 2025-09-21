"""
gui.py Simple GUI for GelbeSeiten AI Scraper
"""

import tkinter as tk
from tkinter import messagebox
from scraper import run_discovery


def start_scraping():
    """Run the scraper with user input and show status."""
    query = entry_query.get().strip()
    pages = entry_pages.get().strip()

    if not query:
        messagebox.showerror("Error", "Please enter a profession/industry.")
        return

    try:
        pages = int(pages) if pages else 1
    except ValueError:
        messagebox.showerror("Error", "Pages must be a number.")
        return

    # Collect selected formats
    formats = []
    if var_csv.get():
        formats.append("csv")
    if var_json.get():
        formats.append("json")

    if not formats:
        messagebox.showerror("Error", "Please select at least one file format (CSV or JSON).")
        return

    try:
        paths = run_discovery(query, pages=pages, formats=formats)
        msg = "Scraping completed!\n\nSaved files:\n"
        for fmt, path in paths.items():
            msg += f"- {fmt.upper()}: {path}\n"
        messagebox.showinfo("Success", msg)
    except Exception as e:
        messagebox.showerror("Error", f"Scraping failed:\n{e}")


# ---------------------------
# Build GUI
# ---------------------------
root = tk.Tk()
root.title("GelbeSeiten AI Scraper")

# Profession input
tk.Label(root, text="Enter profession/industry:").pack(pady=5)
entry_query = tk.Entry(root, width=40)
entry_query.pack(pady=5)

# Pages input
tk.Label(root, text="Number of pages to scrape (default=1):").pack(pady=5)
entry_pages = tk.Entry(root, width=10)
entry_pages.pack(pady=5)

# Format selection
tk.Label(root, text="Select output formats:").pack(pady=5)
var_csv = tk.BooleanVar(value=True)
var_json = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="CSV", variable=var_csv).pack()
tk.Checkbutton(root, text="JSON", variable=var_json).pack()

# Scrape button
tk.Button(root, text="Scrape", command=start_scraping, bg="lightblue").pack(pady=15)

root.mainloop()
