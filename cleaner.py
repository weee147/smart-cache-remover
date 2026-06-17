import os
import time
import shutil
import ctypes
from tkinter import Tk, Label, Button, messagebox
from tkinter.ttk import Progressbar

# 1. FUNZIONE DI PULIZIA IN MODALITÀ SIMULAZIONE (DRY-RUN)
def run_cleanup(progress_bar, status_label, window):
    CACHE_DIR = os.environ.get('TEMP')
    QUARANTINE_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "Cleaner_Quarantine")
    
    # Crea la cartella sul Desktop se non esiste (solo per calcolare i percorsi)
    if not os.path.exists(QUARANTINE_DIR):
        os.makedirs(QUARANTINE_DIR)

    # Raccoglie prima tutti i file per calcolare la percentuale esatta della barra
    all_files = []
    for root_path, dirs, files in os.walk(CACHE_DIR):
        # Sicurezza: Evita di scansionare la quarantena stessa se si trova dentro TEMP
        if QUARANTINE_DIR in root_path:
            continue
        for f in files:
            all_files.append((root_path, f))
            
    total_files = len(all_files)
    
    if total_files == 0:
        status_label.config(text="Status: No files found to clean.")
        progress_bar['value'] = 100
        messagebox.showinfo("Done", "Your system is already clean!")
        window.destroy()
        return

    direct_deleted_files = 0
    quarantined_files_count = 0
    total_space_freed = 0
    start_time = time.time()

    # Avvia la simulazione file per file aggiornando la GUI
    for index, (root_path, f) in enumerate(all_files):
        file_path = os.path.join(root_path, f)
        try:
            # Sicurezza: Salta i collegamenti simbolici
            if os.path.islink(file_path):
                continue

            file_size = os.path.getsize(file_path)
            days_unused = (time.time() - os.path.getatime(file_path)) / (60 * 60 * 24)
            name, extension = os.path.splitext(f)

            # Categoria A: Spazzatura ovvia (Simulazione eliminazione)
            if extension.lower() in ['.tmp', '.log', '.bak'] or file_size == 0:
                # BLOCCO DI SICUREZZA: Commentato per non cancellare nulla dal PC
                # os.remove(file_path)  
                direct_deleted_files += 1
                total_space_freed += file_size
            
            # Categoria B: File vecchi o inutilizzati (Simulazione spostamento)
            elif days_unused > 14:
                target_quarantine = os.path.join(QUARANTINE_DIR, f)
                
                # Gestione corretta dei duplicati
                counter = 1
                while os.path.exists(target_quarantine):
                    target_quarantine = os.path.join(QUARANTINE_DIR, f"{name}_{counter}{extension}")
                    counter += 1
                
                # BLOCCO DI SICUREZZA: Commentato per non spostare i tuoi file sul Desktop
                # shutil.move(file_path, target_quarantine)  
                quarantined_files_count += 1
                total_space_freed += file_size

        except Exception:
            # Salta i file in uso senza bloccare la simulazione
            pass

        # Aggiorna la barra grafica e il testo in tempo reale
        progress_percent = int(((index + 1) / total_files) * 100)
        progress_bar['value'] = progress_percent
        status_label.config(text=f"Simulating: {progress_percent}% ({index + 1}/{total_files} files)")
        window.update() # Forza l'aggiornamento visivo della barra

    execution_time = round(time.time() - start_time, 2)
    space_mb = round(total_space_freed / (1024 * 1024), 2)

    # Nasconde temporaneamente la finestra principale per mostrare i pop-up di report
    window.withdraw()

    # Report finale (Pop-up di simulazione)
    report_message = (
        f"✨ [SIMULATION] Cleanup completed in {execution_time} seconds!\n\n"
        f"📊 REPORT:\n"
        f"• Junk files that WOULD BE permanently deleted: {direct_deleted_files}\n"
        f"• Uncertain files that WOULD BE moved to quarantine: {quarantined_files_count}\n"
        f"• Total space that WOULD BE recovered: {space_mb} MB\n\n"
        f"Would you like to open the folder and check if you want to save anything?"
    )
    wants_to_review = messagebox.askyesno("Cleanup Report (SIMULATION)", report_message)

    # Gestione simulata della Quarantena
    if wants_to_review:
        messagebox.showinfo("Instructions", "Please check the quarantine folder on your Desktop. Move OUT any files you wish to keep.\n\nWhen you are done, click OK on this window to permanently delete the rest.")
        # BLOCCO DI SICUREZZA: Commentato per non eliminare la cartella
        # if os.path.exists(QUARANTINE_DIR):
        #     shutil.rmtree(QUARANTINE_DIR)
    else:
        # BLOCCO DI SICUREZZA: Commentato per non eliminare la cartella
        # if os.path.exists(QUARANTINE_DIR):
        #     shutil.rmtree(QUARANTINE_DIR)
        pass

    # Svuotamento Cestino di Windows (Simulato)
    empty_trash = messagebox.askyesno("Final Step", "Would you like to empty the Windows Recycle Bin as well?")
    if empty_trash:
        try:
            # BLOCCO DI SICUREZZA: Commentato per non svuotare il cestino reale
            # ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 7)
            messagebox.showinfo("Success!", "Recycle Bin emptied. Cleanup finished!")
        except Exception:
            messagebox.showinfo("Notice", "Could not empty the Recycle Bin.")
    else:
        messagebox.showinfo("Finished!", "Cleanup complete. Recycle Bin preserved!")

    window.destroy() # Chiude definitivamente l'app

# 2. INTERFACCIA GRAFICA CON BARRA DI AVANZAMENTO
def create_gui():
    window = Tk()
    window.title("Smart Cache Cleaner ⚡ [SIMULATION MODE]")
    window.geometry("400x180")
    window.resizable(False, False)
    
    # Centra la finestra sullo schermo
    window.eval('tk::PlaceWindow . center')

    # Titolo dell'applicazione
    title_label = Label(window, text="Smart Cache Cleaner v1.2.0 (Demo)", font=("Arial", 12, "bold"))
    title_label.pack(pady=10)

    # Etichetta di stato dinamica
    status_label = Label(window, text="Status: Ready to simulate scan", font=("Arial", 10))
    status_label.pack(pady=5)

    # Barra di avanzamento grafica
    progress_bar = Progressbar(window, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=10)

    # Bottone di avvio (Verde stile WhatsApp)
    start_button = Button(
        window, 
        text="START SIMULATION", 
        font=("Arial", 10, "bold"), 
        bg="#25D366", 
        fg="white", 
        command=lambda: [start_button.config(state="disabled"), run_cleanup(progress_bar, status_label, window)]
    )
    start_button.pack(pady=5)

    window.mainloop()

if __name__ == "__main__":
    create_gui()





