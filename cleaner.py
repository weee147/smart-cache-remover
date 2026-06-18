import os
import time
import shutil
import ctypes
import sys
from tkinter import Tk, Label, Button, messagebox
from tkinter.ttk import Progressbar

# ==============================================================================
# 🛡️ PROTEZIONE ANTINERO: NASCONDE IL TERMINALE NEI PRIMI MILLISECONDI
# ==============================================================================
if sys.platform == "win32":
    # Recupera l'identificativo della finestra nera del prompt dei comandi
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        # La nasconde all'istante per lasciare visibile solo la GUI
        ctypes.windll.user32.ShowWindow(whnd, 0)
# ==============================================================================

# FUNZIONE DI PULIZIA DIZIONARIO UNIFICATA (MODALITÀ SIMULAZIONE PROTETTA CON CANCELLETTI)
def run_cleanup_process(progress_bar, status_label, window, is_simulation=True):
    CACHE_DIR = os.environ.get('TEMP')
    QUARANTINE_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "Cleaner_Quarantine")
    
    # MODIFICA DI SICUREZZA: Commentato per non creare cartelle reali sul Desktop
    # if not is_simulation and not os.path.exists(QUARANTINE_DIR):
    #     os.makedirs(QUARANTINE_DIR)

    # Raccoglie tutti i file per calcolare la percentuale esatta della barra
    all_files = []
    for root_path, dirs, files in os.walk(CACHE_DIR):
        if QUARANTINE_DIR in root_path:
            continue
        for f in files:
            all_files.append((root_path, f))
            
    total_files = len(all_files)
    
    if total_files == 0:
        status_label.config(text="Status: No files found.")
        progress_bar['value'] = 100
        messagebox.showinfo("Done", "Your system is already clean!", parent=window)
        window.destroy()
        return

    direct_deleted_files = 0
    quarantined_files_count = 0
    total_space_freed = 0
    start_time = time.time()

    for index, (root_path, f) in enumerate(all_files):
        file_path = os.path.join(root_path, f)
        try:
            if os.path.islink(file_path):
                continue

            file_size = os.path.getsize(file_path)
            days_unused = (time.time() - os.path.getatime(file_path)) / (60 * 60 * 24)
            name, extension = os.path.splitext(f)

            # Categoria A: Spazzatura ovvia
            if extension.lower() in ['.tmp', '.log', '.bak'] or file_size == 0:
                if not is_simulation:
                    # BLOCCO DI SICUREZZA: Commentato per non cancellare nulla dal PC
                    # os.remove(file_path)  
                    pass
                direct_deleted_files += 1
                total_space_freed += file_size
            
            # Categoria B: File vecchi o inutilizzati
            elif days_unused > 14:
                target_quarantine = os.path.join(QUARANTINE_DIR, f)
                counter = 1
                while os.path.exists(target_quarantine):
                    target_quarantine = os.path.join(QUARANTINE_DIR, f"{name}_{counter}{extension}")
                    counter += 1
                
                if not is_simulation:
                    # BLOCCO DI SICUREZZA: Commentato per non spostare i tuoi file sul Desktop
                    # shutil.move(file_path, target_quarantine)  
                    pass
                quarantined_files_count += 1
                total_space_freed += file_size

        except Exception:
            # Salta i file bloccati da Windows senza rallentare o bloccarsi
            pass

        # Aggiorna la barra grafica e il testo in tempo reale
        progress_percent = int(((index + 1) / total_files) * 100)
        progress_bar['value'] = progress_percent
        prefix = "Simulating" if is_simulation else "Cleaning (Simulated)"
        status_label.config(text=f"{prefix}: {progress_percent}% ({index + 1}/{total_files} files)")
        window.update()

    execution_time = round(time.time() - start_time, 2)
    space_mb = round(total_space_freed / (1024 * 1024), 2)

    status_label.config(text="Status: Completed!")
    window.update()

    # IMPOSTAZIONE DEL REPORT (FORZATO IN MODALITÀ FINTA/SIMULATA)
    mode_title = "Cleanup Report (SIMULATION)" if is_simulation else "Cleanup Report (SIMULATED)"
    would_txt = "WOULD BE "
    
    report_message = (
        f"✨ Process completed in {execution_time} seconds!\n\n"
        f"📊 REPORT:\n"
        f"• Junk files {would_txt}permanently deleted: {direct_deleted_files}\n"
        f"• Uncertain files {would_txt}moved to quarantine: {quarantined_files_count}\n"
        f"• Total space {would_txt}recovered: {space_mb} MB\n\n"
    )
    
    if not is_simulation:
        report_message += f"Uncertain files {would_txt}moved to your Desktop in the folder:\n'{os.path.basename(QUARANTINE_DIR)}'\n\nWould you like to open the folder and check if you want to save anything?"
        wants_to_review = messagebox.askyesno(mode_title, report_message, parent=window)
        
        if wants_to_review:
            messagebox.showinfo("Instructions", "Please check the quarantine folder on your Desktop. Move OUT any files you wish to keep.\n\nWhen you are done, click OK on this window to permanently delete the rest.", parent=window)
            # BLOCCO DI SICUREZZA: Commentato per non eliminare cartelle reali
            # if os.path.exists(QUARANTINE_DIR):
            #     shutil.rmtree(QUARANTINE_DIR)
        else:
            # BLOCCO DI SICUREZZA: Commentato per non eliminare cartelle reali
            # if os.path.exists(QUARANTINE_DIR):
            #     shutil.rmtree(QUARANTINE_DIR)
            pass
    else:
        report_message += "This was a safe simulation. No files were modified or deleted."
        messagebox.showinfo(mode_title, report_message, parent=window)

    # SVUOTAMENTO CESTINO DI WINDOWS (FINTO / SIMULATO)
    empty_trash = messagebox.askyesno("Final Step", "Would you like to empty the Windows Recycle Bin as well?", parent=window)
    if empty_trash:
        if not is_simulation:
            # BLOCCO DI SICUREZZA: Commentato per non svuotare il cestino reale
            # try:
            #     ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 7)
            #     messagebox.showinfo("Success!", "Recycle Bin emptied. Cleanup finished!", parent=window)
            # except Exception:
            #     messagebox.showinfo("Notice", "Could not empty the Recycle Bin.", parent=window)
            messagebox.showinfo("Simulation", "[SIMULATION] Recycle Bin would be emptied successfully!", parent=window)
        else:
            messagebox.showinfo("Simulation", "[SIMULATION] Recycle Bin would be emptied successfully!", parent=window)
    else:
        messagebox.showinfo("Finished!", "Process complete. Recycle Bin preserved!")

    window.destroy()

# CREAZIONE DELLA FINESTRA PRINCIPALE (GUI)
def create_gui():
    window = Tk()
    window.title("Smart Cache Cleaner ⚡ [PROTECTED DEMO]")
    window.geometry("460x220")
    window.resizable(False, False)
    window.eval('tk::PlaceWindow . center')

    title_label = Label(window, text="Smart Cache Cleaner v1.3.0 (Protected Demo)", font=("Arial", 12, "bold"))
    title_label.pack(pady=10)

    status_label = Label(window, text="Status: Choose an action below", font=("Arial", 10))
    status_label.pack(pady=5)

    progress_bar = Progressbar(window, orient="horizontal", length=360, mode="determinate")
    progress_bar.pack(pady=10)

    import tkinter as tk
    btn_frame = tk.Frame(window)
    btn_frame.pack(pady=10)

    def disable_all_buttons():
        sim_button.config(state="disabled")
        clean_button.config(state="disabled")
        cancel_button.config(state="disabled")

    # BOTTONE ROSSO: SIMULAZIONE
    sim_button = Button(
        btn_frame, 
        text="RUN SIMULATION", 
        font=("Arial", 9, "bold"), 
        bg="#FF3B30", 
        fg="white", 
        width=15,
        command=lambda: [disable_all_buttons(), run_cleanup_process(progress_bar, status_label, window, is_simulation=True)]
    )
    sim_button.pack(side="left", padx=5)

    # BOTTONE VERDE: PULIZIA (CANCELLATA DAI CANCELLETTI, ORA AGISCE COME ULTERIORE SIMULAZIONE)
    clean_button = Button(
        btn_frame, 
        text="REAL CLEAN", 
        font=("Arial", 9, "bold"), 
        bg="#25D366", 
        fg="white", 
        width=12,
        command=lambda: [disable_all_buttons(), run_cleanup_process(progress_bar, status_label, window, is_simulation=False)]
    )
    clean_button.pack(side="left", padx=5)

    # BOTTONE GRIGIO: ESCI / ANNULLA
    cancel_button = Button(
        btn_frame, 
        text="CANCEL", 
        font=("Arial", 9, "bold"), 
        bg="#8E8E93", 
        fg="white", 
        width=10,
        command=window.destroy
    )
    cancel_button.pack(side="left", padx=5)

    window.mainloop()

if __name__ == "__main__":
    create_gui()
