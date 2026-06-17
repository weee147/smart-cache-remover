import os
import time
import shutil
import ctypes
from tkinter import Tk, Label, Button, messagebox
from tkinter.ttk import Progressbar

# 1. FUNZIONE PRINCIPALE DI PULIZIA (REALE, SENZA BLOCCHI)
def run_cleanup(progress_bar, status_label, window):
    CACHE_DIR = os.environ.get('TEMP')
    
    # Raccoglie prima tutti i file per calcolare la percentuale esatta
    all_files = []
    for root_path, dirs, files in os.walk(CACHE_DIR):
        for f in files:
            all_files.append(os.path.join(root_path, f))
            
    total_files = len(all_files)
    
    if total_files == 0:
        status_label.config(text="Status: No files found to clean.")
        progress_bar['value'] = 100
        messagebox.showinfo("Done", "Your system is already clean!")
        window.destroy()
        return

    direct_deleted_files = 0
    total_space_freed = 0
    start_time = time.time()

    # Avvia la pulizia reale file per file aggiornando la GUI
    for index, file_path in enumerate(all_files):
        try:
            if os.path.islink(file_path):
                continue

            file_size = os.path.getsize(file_path)
            _, extension = os.path.splitext(file_path)

            # ELIMINAZIONE DIRETTA E IMMEDIATA DI TUTTI I FILE DENTRO TEMP
            os.remove(file_path)
            direct_deleted_files += 1
            total_space_freed += file_size

        except Exception:
            # Salta i file bloccati da Windows senza fermare il programma
            pass

        # Aggiorna la barra grafica e il testo in tempo reale
        progress_percent = int(((index + 1) / total_files) * 100)
        progress_bar['value'] = progress_percent
        status_label.config(text=f"Cleaning: {progress_percent}% ({index + 1}/{total_files} files)")
        window.update() # Forza la finestra grafica ad aggiornarsi visivamente

    execution_time = round(time.time() - start_time, 2)
    space_mb = round(total_space_freed / (1024 * 1024), 2)

    # Report finale
    report_message = (
        f"✨ Cleanup completed in {execution_time} seconds!\n\n"
        f"📊 REPORT:\n"
        f"• Files permanently deleted: {direct_deleted_files}\n"
        f"• Total space recovered: {space_mb} MB"
    )
    messagebox.showinfo("Cleanup Report", report_message)

    # Chiede l'ultimo passaggio per il Cestino
    empty_trash = messagebox.askyesno("Final Step", "Would you like to empty the Windows Recycle Bin as well?")
    if empty_trash:
        try:
            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 7)
            messagebox.showinfo("Success!", "Recycle Bin emptied!")
        except Exception:
            pass

    window.destroy() # Chiude la finestra del programma al termine

# 2. CREAZIONE DELLA GUI CON PROGRESS BAR
def create_gui():
    window = Tk()
    window.title("Smart Cache Cleaner ⚡")
    window.geometry("400x180")
    window.resizable(False, False)
    
    # Centra la finestra sullo schermo dello smartphone o PC
    window.eval('tk::PlaceWindow . center')

    # Testo di benvenuto / istruzioni
    title_label = Label(window, text="Smart Cache Cleaner v1.1.0", font=("Arial", 12, "bold"))
    title_label.pack(pady=10)

    # Etichetta di stato dinamica
    status_label = Label(window, text="Status: Ready to clean", font=("Arial", 10))
    status_label.pack(pady=5)

    # Barra di avanzamento grafica (Progress Bar)
    progress_bar = Progressbar(window, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=10)

    # Bottone di avvio
    start_button = Button(
        window, 
        text="START CLEANING", 
        font=("Arial", 10, "bold"), 
        bg="#25D366", # Colore verde WhatsApp
        fg="white", 
        command=lambda: [start_button.config(state="disabled"), run_cleanup(progress_bar, status_label, window)]
    )
    start_button.pack(pady=5)

    window.mainloop()

if __name__ == "__main__":
    create_gui()




