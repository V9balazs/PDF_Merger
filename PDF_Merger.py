import tkinter as tk
from tkinter import messagebox, Label, filedialog

def select_pdf():
    filepath = filedialog.askopenfilename(title="Select a PDF", filetypes=[("PDF files", "*.pdf")])
    if filepath:
        # Kezelje a kiválasztott PDF-et (pl. hozzáadja egy listához vagy megjeleníti az elérési útját)
        print(filepath)

def merger_clicked():
    # Törli a frame aktuális tartalmát
    for widget in content_frame.winfo_children():
        widget.destroy()
    # Itt implementálhatja a PDF merge funkciót
    Label(content_frame, text="Merger content goes here").pack(pady=20)

def settings_clicked():
    # Törli a frame aktuális tartalmát
    for widget in content_frame.winfo_children():
        widget.destroy()
    # Itt implementálhatja a beállítási opciókat
    Label(content_frame, text="Settings content goes here").pack(pady=20)

# Alkalmazás létrehozása
app = tk.Tk()
app.title("PDF Merger")

# Ablak méretének beállítása
width = 900
height = 500
app.geometry(f"{width}x{height}")
app.resizable(False, False)

# Ablak középre helyezése
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
app.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

# Gomb hozzáadása a PDF kiválasztásához
select_button = tk.Button(buttons_frame, text="Select PDF", command=select_pdf, width=10, height=3)
select_button.grid(row=2, column=0, sticky='nw', pady=5)  # <--- Új gomb hozzáadása a többi gomb alá

# Gombokat tartalmazó Frame létrehozása
buttons_frame = tk.Frame(app)
buttons_frame.grid(row=0, column=0, sticky='nw', padx=20, pady=20)

# Gombok létrehozása a buttons_frame-en belül
merger_button = tk.Button(buttons_frame, text="Merger", command=merger_clicked, width=10, height=3)
merger_button.grid(row=0, column=0, sticky='nw', pady=5)

settings_button = tk.Button(buttons_frame, text="Settings", command=settings_clicked, width=10, height=3)
settings_button.grid(row=1, column=0, sticky='nw', pady=5)

# Tartalom Frame létrehozása
content_frame = tk.Frame(app, bg="white", bd=2, relief="groove")
content_frame.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=20, pady=20)

# A grid súlyozásának beállítása, hogy a content_frame kitöltse a rendelkezésre álló teret
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)

merger_clicked()
app.mainloop()
