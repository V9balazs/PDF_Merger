import tkinter as tk
import PyPDF2
import pickle
import os
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import messagebox, Label, filedialog

def drop(event):
    filepath = event.data
    print(filepath)

def select_pdf():
    filepath = filedialog.askopenfilename(title="Select a PDF", filetypes=[("PDF files", "*.pdf")])
    if filepath:
        print(filepath)

# Globális változók definiálása
save_location_entry = None
file_name_entry = None

def display_merger():
    global entries, feedback_label
    global save_location_entry, file_name_entry
    # Törli a merger_frame aktuális tartalmát
    for widget in merger_frame.winfo_children():
        widget.destroy()

    full_filepaths = []

    def drop_on_entry(event, entry):
        filepath = event.data
        filename = os.path.basename(filepath)
        index = entries.index(entry)  # az aktuális Entry indexe a listában
        if index < len(full_filepaths):  # ha már létezik elérési út ezen az indexen
            full_filepaths[index] = filepath  # frissítsük a listában
        else:
            full_filepaths.append(filepath)  # egyébként adjuk hozzá az új elérési utat a listához
        entry.delete(0, tk.END)
        entry.insert(0, filename)

    def merge_files():
        merger = PyPDF2.PdfMerger()

        for index, filepath in enumerate(full_filepaths):  # használjuk a teljes elérési utat a listából
            if filepath.endswith('.pdf'):
                try:
                    merger.append(filepath)
                except:
                    feedback_label.config(text=f"Error merging file: {filepath}", fg="red")
                    app.after(3000, lambda: feedback_label.config(text=""))
                    return

        # Itt definiáljuk az output_path változót
        output_path = os.path.join(save_location_entry.get(), file_name_entry.get())
        if not output_path.endswith('.pdf'):
            output_path += '.pdf'

        try:
            with open(output_path, 'wb') as output_file:
                merger.write(output_file)
            feedback_label.config(text="Files merged successfully!")
            app.after(3000, lambda: feedback_label.config(text=""))
        except:
            feedback_label.config(text="Error saving merged file.", fg="red")
            app.after(3000, lambda: feedback_label.config(text=""))

    entries = []
    for i in range(3):
        for j in range(3):
            entry = tk.Entry(merger_frame, width=30)
            entry.grid(row=i, column=j, padx=20, pady=20, sticky='nsew')

            entry.drop_target_register(DND_FILES)
            entry.dnd_bind('<<Drop>>', lambda event, e=entry: drop_on_entry(event, e))

            entries.append(entry)

    merge_btn = tk.Button(merger_frame, text="Merge PDFs", command=merge_files, width=20, height=2)
    merge_btn.grid(row=3, column=1, pady=20)

    feedback_label = tk.Label(merger_frame, text="", fg="green")
    feedback_label.grid(row=4, column=0, columnspan=3, pady=5)

    def reset_entries():
        for entry in entries:
            entry.delete(0, tk.END)
        full_filepaths.clear()

    reset_btn = tk.Button(merger_frame, text="Reset", command=reset_entries, width=20, height=2)
    reset_btn.grid(row=3, column=2, pady=20)

DATA_FILE = "settings_data.pkl"

def save_data(file_name, save_location):
    with open(DATA_FILE, 'wb') as file:
        pickle.dump((file_name, save_location), file)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'rb') as file:
            return pickle.load(file)
    return None, None

def display_settings():
    global save_location_entry, file_name_entry

    # Törli a settings_frame aktuális tartalmát
    for widget in settings_frame.winfo_children():
        widget.destroy()

    # Változók definiálása a display_settings függvényen belül
    save_dir_entry_var = tk.StringVar()
    save_filename_entry_var = tk.StringVar()

    # Címke a fájlnévhez
    file_name_label = tk.Label(settings_frame, text="Merged File Name:")
    file_name_label.grid(row=0, column=0, sticky='w', padx=10, pady=10)

    # Entry a fájlnévhez
    file_name_entry = tk.Entry(settings_frame, textvariable=save_filename_entry_var, width=50)
    file_name_entry.grid(row=0, column=1, padx=10, pady=10)
    
    # Címke a mentési helyhez
    save_location_label = tk.Label(settings_frame, text="Save Location:")
    save_location_label.grid(row=1, column=0, sticky='w', padx=10, pady=10)

    # Entry a mentési helyhez
    save_location_entry = tk.Entry(settings_frame, textvariable=save_dir_entry_var, width=50)
    save_location_entry.grid(row=1, column=1, padx=10, pady=10)

    # Gomb a mappa választáshoz
    def choose_folder():
        folder = filedialog.askdirectory()
        if folder:
            save_dir_entry_var.set(folder)

    choose_folder_btn = tk.Button(settings_frame, text="Choose Folder", command=choose_folder)
    choose_folder_btn.grid(row=1, column=2, padx=10, pady=10)

    # Adatok betöltése
    saved_file_name, saved_location = load_data()
    if saved_file_name:
        save_filename_entry_var.set(saved_file_name)
    if saved_location:
        save_dir_entry_var.set(saved_location)

    # Adatok automatikus mentése
    def auto_save(*args):
        save_data(save_filename_entry_var.get(), save_dir_entry_var.get())

    save_filename_entry_var.trace_add("write", auto_save)
    save_dir_entry_var.trace_add("write", auto_save)

    # Itt ágyazzuk be a merge_files függvényt
    def merge_files():
        merger = PyPDF2.PdfMerger()

        for entry in entries:
            filepath = entry.get()
            if filepath.endswith('.pdf'):
                try:
                    merger.append(filepath)
                except:
                    messagebox.showerror("Error", f"Error merging file: {filepath}")

        # Itt definiáljuk az output_path változót
        output_path = os.path.join(save_location_entry.get(), file_name_entry.get())

        try:
            with open(output_path, 'wb') as output_file:
                merger.write(output_file)
            messagebox.showinfo("Success", f"Files merged successfully to {output_path}")
        except:
            messagebox.showerror("Error", "Error saving merged file.")

entries = []


# Alkalmazás létrehozása
app = TkinterDnD.Tk()
app.title("PDF Merger")

# Ablak méretének beállítása
width = 695
height = 450
app.geometry(f"{width}x{height}")
app.resizable(False, False)

# Ablak középre helyezése
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
app.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

# Settings Frame létrehozása
settings_frame = tk.Frame(app, bg="#53e2e5", bd=2, relief="groove")
settings_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

# Merger Frame létrehozása
merger_frame = tk.Frame(app, bg="#4d92e2", bd=2, relief="groove")
merger_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

# A grid súlyozásának beállítása, hogy a merger_frame és settings_frame kitöltse a rendelkezésre álló teret
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=3)

# App beállítás
app.configure(bg='#181c26')
current_directory = os.path.dirname(os.path.realpath(__file__))
icon_path = os.path.join(current_directory, 'Logo.ico')
app.iconbitmap(icon_path)

# Add drag-and-drop functionality to merger_frame
merger_frame.drop_target_register(DND_FILES)
merger_frame.dnd_bind('<<Drop>>', drop)

display_settings()
display_merger()
app.mainloop()