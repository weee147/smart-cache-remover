import os
import time
import shutil
import ctypes
import sys
import json
import logging
from datetime import datetime
from tkinter import Tk, Label, Button, messagebox, Frame, Canvas, Scrollbar, VERTICAL, RIGHT, BOTH, LEFT
from tkinter.ttk import Progressbar
from threading import Thread

# ==============================================================================
# ⚙️ CONFIGURAZIONE SISTEMA LOGGING
# ==============================================================================
LOG_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "Cleaner_Logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

log_file = os.path.join(LOG_DIR, f"cleaner_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ==============================================================================
# 📋 CONFIGURAZIONE DI DEFAULT (con possibilità di personalizzazione)
# ==============================================================================
CONFIG_FILE = os.path.join(os.path.expanduser("~"), "Desktop", "cleaner_config.json")

DEFAULT_CONFIG = {
    "junk_extensions": [".tmp", ".log", ".bak", ".cache", ".temp"],
    "days_threshold": 14,
    "enable_logging": True,
    "scan_subdirectories": True,
    "file_size_threshold_kb": 0,  # File vuoti (0 KB)
    "timeout_per_file_seconds": 5
}

def load_config():
    """Carica la configurazione dal file, altrimenti usa i default."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
            logging.info("Configurazione caricata da file personalizzato")
            return config
        except Exception as e:
            logging.warning(f"Errore nel caricamento config: {e}. Uso default.")
            return DEFAULT_CONFIG
    else:
        # Crea file config di default
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(DEFAULT_CONFIG, f, indent=4)
            logging.info("File configurazione creato con default")
        except Exception:
            pass
        return DEFAULT_CONFIG

CONFIG = load_config()

# ==============================================================================
# 🛡️ PROTEZIONE ANTINERO: CHIUDE IL TERMINALE ALL'ISTANTE ALL'AVVIO
# ==============================================================================
if sys.platform == "win32":
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)
    
    if sys.executable.endswith("python.exe"):
        script_path = os.path.abspath(__file__)
        pythonw_path = sys.executable.replace("python.exe", "pythonw.exe")
        if os.path.exists(pythonw_path):
            os.execv(pythonw_path, [pythonw_path, script_path])
            sys.exit()

# ==============================================================================
# 🔍 VALIDAZIONE PERCORSI
# ==============================================================================
def validate_paths(cache_dir, quarantine_dir):
    """Valida che i percorsi siano accessibili."""
    try:
        if not os.path.exists(cache_dir):
            logging.error(f"CACHE_DIR non esiste: {cache_dir}")
            return False
        if not os.access(cache_dir, os.R_OK):
            logging.error(f"CACHE_DIR non leggibile: {cache_dir}")
            return False
        
        # Tenta di creare quarantine_dir
        if not os.path.exists(quarantine_dir):
            os.makedirs(quarantine_dir)
        if not os.access(quarantine_dir, os.W_OK):
            logging.error(f"QUARANTINE_DIR non scrivibile: {quarantine_dir}")
            return False
        
        logging.info(f"✓ Percorsi validati - CACHE: {cache_dir}, QUARANTINE: {quarantine_dir}")
        return True
    except Exception as e:
        logging.error(f"Errore nella validazione percorsi: {e}")
        return False

# ==============================================================================
# 📊 FUNZIONE DI SIMULAZIONE (DRY-RUN)
# ==============================================================================
def simulate_cleanup(cache_dir, config):
    """Esegue una simulazione della pulizia senza eliminare nulla."""
    junk_files = []
    old_files = []
    
    try:
        for root_path, dirs, files in os.walk(cache_dir):
            for f in files:
                file_path = os.path.join(root_path, f)
                try:
                    if os.path.islink(file_path):
                        continue
                    
                    name, extension = os.path.splitext(f)
                    file_size = os.path.getsize(file_path)
                    
                    if extension.lower() in config["junk_extensions"] or file_size == 0:
                        junk_files.append(file_path)
                    else:
                        try:
                            days_unused = (time.time() - os.path.getatime(file_path)) / (60 * 60 * 24)
                            if days_unused > config["days_threshold"]:
                                old_files.append(file_path)
                        except:
                            pass
                except:
                    pass
    except Exception as e:
        logging.error(f"Errore durante la simulazione: {e}")
    
    return junk_files, old_files

# ==============================================================================
# 1. FUNZIONE PRINCIPALE DI PULIZIA REALE (MIGLIORATA)
# ==============================================================================
def run_cleanup(progress_bar, status_label, window, cancel_flag, dry_run=False):
    """Esegue la pulizia con tutte le feature migliorate."""
    try:
        CACHE_DIR = os.environ.get('TEMP')
        QUARANTINE_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "Cleaner_Quarantine")
        
        # Validazione percorsi
        if not validate_paths(CACHE_DIR, QUARANTINE_DIR):
            messagebox.showerror("Errore", "Impossibile validare i percorsi di sistema!")
            window.destroy()
            return
        
        # Raccoglie i file
        all_files = []
        for root_path, dirs, files in os.walk(CACHE_DIR):
            if cancel_flag['stop']:
                logging.info("Pulizia annullata dall'utente durante la scansione")
                return
            if QUARANTINE_DIR in root_path:
                continue
            for f in files:
                all_files.append((root_path, f))
        
        total_files = len(all_files)
        logging.info(f"Scansione completata: {total_files} file trovati")
        
        if total_files == 0:
            status_label.config(text="Status: Sistema già pulito!")
            progress_bar['value'] = 100
            messagebox.showinfo("Fatto", "Il tuo sistema è già pulito! ✨")
            window.destroy()
            return
        
        # Se è una simulazione, mostra i risultati
        if dry_run:
            junk, old = simulate_cleanup(CACHE_DIR, CONFIG)
            msg = f"SIMULAZIONE:\n\n"
            msg += f"🗑️  File spazzatura: {len(junk)}\n"
            msg += f"📦 File vecchi: {len(old)}\n"
            msg += f"📊 Totale: {len(junk) + len(old)} file\n\n"
            msg += "Nessun file è stato eliminato (modalità simulazione)."
            messagebox.showinfo("Risultati Simulazione", msg)
            window.destroy()
            return
        
        direct_deleted_files = 0
        quarantined_files_count = 0
        total_space_freed = 0
        failed_files_count = 0
        skipped_files_count = 0
        start_time = time.time()
        
        logging.info("=== AVVIO PULIZIA REALE ===")
        
        # Esecuzione pulizia
        for index, (root_path, f) in enumerate(all_files):
            if cancel_flag['stop']:
                logging.info("Pulizia annullata dall'utente durante l'esecuzione")
                messagebox.showwarning("Annullato", "Pulizia interrotta dall'utente")
                window.destroy()
                return
            
            file_path = os.path.join(root_path, f)
            try:
                # Aggiornamento GUI con protezione
                try:
                    progress_percent = int(((index + 1) / total_files) * 100)
                    progress_bar['value'] = progress_percent
                    status_label.config(
                        text=f"Pulizia: {progress_percent}% ({index + 1}/{total_files})\nFile: {f[:40]}..."
                    )
                    window.update()
                except:
                    logging.warning("Errore nell'aggiornamento GUI")
                
                # Salta collegamenti simbolici
                if os.path.islink(file_path):
                    skipped_files_count += 1
                    continue
                
                file_size = os.path.getsize(file_path)
                
                # Calcolo giorni inutilizzati con protezione
                try:
                    days_unused = (time.time() - os.path.getatime(file_path)) / (60 * 60 * 24)
                except:
                    days_unused = 0
                
                name, extension = os.path.splitext(f)
                
                # Categoria A: Spazzatura ovvia (ELIMINAZIONE REALE)
                if extension.lower() in CONFIG["junk_extensions"] or file_size == 0:
                    os.remove(file_path)
                    direct_deleted_files += 1
                    total_space_freed += file_size
                    logging.info(f"ELIMINATO: {file_path} ({file_size} bytes)")
                
                # Categoria B: File vecchi o inutilizzati (SPOSTAMENTO REALE)
                elif days_unused > CONFIG["days_threshold"]:
                    target_quarantine = os.path.join(QUARANTINE_DIR, f)
                    
                    # Gestione duplicati
                    counter = 1
                    while os.path.exists(target_quarantine):
                        target_quarantine = os.path.join(QUARANTINE_DIR, f"{name}_{counter}{extension}")
                        counter += 1
                    
                    shutil.move(file_path, target_quarantine)
                    quarantined_files_count += 1
                    total_space_freed += file_size
                    logging.info(f"SPOSTATO IN QUARANTENA: {file_path} ({file_size} bytes)")
                else:
                    skipped_files_count += 1

            except PermissionError:
                failed_files_count += 1
                logging.warning(f"ACCESSO NEGATO: {file_path}")
            except Exception as e:
                failed_files_count += 1
                logging.warning(f"ERRORE SU FILE: {file_path} - {str(e)}")
        
        execution_time = round(time.time() - start_time, 2)
        space_mb = round(total_space_freed / (1024 * 1024), 2)
        
        logging.info(f"=== PULIZIA COMPLETATA ===")
        logging.info(f"Tempo: {execution_time}s | Spazio liberato: {space_mb} MB")
        logging.info(f"Eliminati: {direct_deleted_files} | Spostati: {quarantined_files_count}")
        logging.info(f"Falliti: {failed_files_count} | Saltati: {skipped_files_count}")
        
        # Nasconde la finestra
        window.withdraw()
        
        # Report finale completo
        report_message = (
            f"✨ Pulizia completata in {execution_time} secondi!\n\n"
            f"📊 REPORT DETTAGLIATO:\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🗑️  File eliminati: {direct_deleted_files}\n"
            f"📦 File in quarantena: {quarantined_files_count}\n"
            f"⏭️  File saltati: {skipped_files_count}\n"
            f"⚠️  File protetti/errore: {failed_files_count}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💾 Spazio liberato: {space_mb} MB\n\n"
            f"📂 I file in quarantena sono su:\n'{os.path.basename(QUARANTINE_DIR)}'\n\n"
            f"Vuoi verificare la cartella?"
        )
        wants_to_review = messagebox.askyesno("Report Pulizia", report_message)
        
        # Gestione quarantena
        if wants_to_review:
            instructions = (
                "📋 ISTRUZIONI:\n\n"
                "1. Controlla la cartella 'Cleaner_Quarantine' sul Desktop\n"
                "2. Sposta i file che vuoi SALVARE fuori da questa cartella\n"
                "3. Clicca OK quando hai finito\n\n"
                "⚠️  I file rimasti verranno eliminati in modo permanente!"
            )
            messagebox.showinfo("Istruzioni Quarantena", instructions)
            if os.path.exists(QUARANTINE_DIR):
                try:
                    shutil.rmtree(QUARANTINE_DIR)
                    logging.info("Quarantena svuotata dopo revisione")
                except Exception as e:
                    logging.error(f"Errore nello svuotamento quarantena: {e}")
        else:
            if os.path.exists(QUARANTINE_DIR):
                try:
                    shutil.rmtree(QUARANTINE_DIR)
                    logging.info("Quarantena svuotata (utente non ha revisionato)")
                except Exception as e:
                    logging.error(f"Errore nello svuotamento quarantena: {e}")
        
        # Svuotamento Cestino
        empty_trash = messagebox.askyesno(
            "Passo Finale",
            "Vuoi svuotare anche il Cestino di Windows?"
        )
        if empty_trash:
            try:
                ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 7)
                messagebox.showinfo("Successo!", "Cestino svuotato! 🎉\nPulizia terminata!")
                logging.info("Cestino Windows svuotato")
            except Exception as e:
                messagebox.showinfo("Avviso", "Cestino non svuotabile (potrebbe essere già vuoto)")
                logging.warning(f"Impossibile svuotare Cestino: {e}")
        else:
            messagebox.showinfo("Finito!", "Pulizia completata! Cestino preservato.")
            logging.info("Pulizia terminata - Cestino preservato")
        
        # Mostra il log
        show_log = messagebox.askyesno("Log", "Vuoi visualizzare il file di log dettagliato?")
        if show_log:
            try:
                os.startfile(log_file)
            except:
                messagebox.showinfo("Log", f"File log salvato in:\n{log_file}")
        
        window.destroy()
        
    except Exception as e:
        logging.critical(f"Errore critico: {e}")
        messagebox.showerror("Errore Critico", f"Si è verificato un errore:\n{str(e)}")
        window.destroy()

# ==============================================================================
# 2. INTERFACCIA GRAFICA MIGLIORATA
# ==============================================================================
def create_gui():
    """Crea l'interfaccia grafica con pulsante di cancellazione."""
    window = Tk()
    window.title("Smart Cache Cleaner ⚡")
    window.geometry("500x280")
    window.resizable(False, False)
    window.eval('tk::PlaceWindow . center')
    
    # Flag per annullare l'operazione
    cancel_flag = {'stop': False}
    
    # Titolo
    title_label = Label(window, text="Smart Cache Cleaner v2.0.0", font=("Arial", 14, "bold"), fg="#25D366")
    title_label.pack(pady=10)
    
    # Sottotitolo
    subtitle_label = Label(
        window,
        text="Sistema avanzato di pulizia cache con configurazione personalizzabile",
        font=("Arial", 9),
        fg="gray"
    )
    subtitle_label.pack(pady=2)
    
    # Status label
    status_label = Label(window, text="Status: Pronto per la pulizia", font=("Arial", 10), fg="#333")
    status_label.pack(pady=10)
    
    # Barra di avanzamento
    progress_bar = Progressbar(window, orient="horizontal", length=400, mode="determinate")
    progress_bar.pack(pady=15, padx=20)
    
    # Frame per i pulsanti
    button_frame = Frame(window)
    button_frame.pack(pady=10)
    
    # Pulsante START (Verde)
    start_button = Button(
        button_frame,
        text="▶ PULIZIA REALE",
        font=("Arial", 11, "bold"),
        bg="#25D366",
        fg="white",
        width=18,
        command=lambda: [
            start_button.config(state="disabled"),
            simulate_btn.config(state="disabled"),
            cancel_button.config(state="normal"),
            Thread(target=run_cleanup, args=(progress_bar, status_label, window, cancel_flag, False), daemon=True).start()
        ]
    )
    start_button.pack(side=LEFT, padx=5)
    
    # Pulsante SIMULAZIONE (Blu)
    simulate_btn = Button(
        button_frame,
        text="🔍 SIMULAZIONE",
        font=("Arial", 11, "bold"),
        bg="#007AFF",
        fg="white",
        width=18,
        command=lambda: [
            start_button.config(state="disabled"),
            simulate_btn.config(state="disabled"),
            cancel_button.config(state="normal"),
            Thread(target=run_cleanup, args=(progress_bar, status_label, window, cancel_flag, True), daemon=True).start()
        ]
    )
    simulate_btn.pack(side=LEFT, padx=5)
    
    # Pulsante ANNULLA (Rosso)
    cancel_button = Button(
        button_frame,
        text="⏹ ANNULLA",
        font=("Arial", 11, "bold"),
        bg="#FF3B30",
        fg="white",
        width=18,
        state="disabled",
        command=lambda: [
            cancel_flag.update({'stop': True}),
            cancel_button.config(state="disabled"),
            start_button.config(state="normal"),
            simulate_btn.config(state="normal"),
            messagebox.showwarning("Annullato", "Pulizia annullata!")
        ]
    )
    cancel_button.pack(side=LEFT, padx=5)
    
    # Info footer
    footer = Label(
        window,
        text="💡 Suggerimento: Simulazione prima di pulire per anteprima | 📁 Log salvati in: Desktop/Cleaner_Logs",
        font=("Arial", 8),
        fg="gray",
        wraplength=480
    )
    footer.pack(pady=10)
    
    window.mainloop()

if __name__ == "__main__":
    create_gui()
