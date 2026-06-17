import os
import time
import shutil
import ctypes
from tkinter import messagebox, Tk

# Initialize the hidden GUI root for pop-up windows
root = Tk()
root.withdraw()

# Path configurations
CACHE_DIR = os.environ.get('TEMP')
# The quarantine directory is placed on the Desktop for easy user access
QUARANTINE_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "Cleaner_Quarantine")

# Performance and report metrics
direct_deleted_files = 0
quarantined_files_count = 0
total_space_freed = 0

start_time = time.time()

# Create the quarantine folder if it does not exist yet
if not os.path.exists(QUARANTINE_DIR):
    os.makedirs(QUARANTINE_DIR)

# 1. SCAN & CLEAN PHASE
# Standard directory tree traversal using os.walk
for root_path, dirs, files in os.walk(CACHE_DIR):
    # Prevention: Prevent scanning the quarantine folder if it is located inside TEMP
    if QUARANTINE_DIR in root_path:
        continue

    for f in files:
        file_path = os.path.join(root_path, f)
        try:
            # Safety check: Skip symbolic links to avoid accidentally escaping the TEMP directory
            if os.path.islink(file_path):
                continue

            file_size = os.path.getsize(file_path)
            days_unused = (time.time() - os.path.getatime(file_path)) / (60 * 60 * 24)
            name, extension = os.path.splitext(f)

            # Category A: Obvious Junk (Immediate permanent deletion)
            if extension.lower() in ['.tmp', '.log', '.bak'] or file_size == 0:
                os.remove(file_path)
                direct_deleted_files += 1
                total_space_freed += file_size
            
            # Category B: Obsolete/Old Files (Safely moved to quarantine)
            elif days_unused > 50:
                target_quarantine = os.path.join(QUARANTINE_DIR, f)
                
                # Correct duplicate handling: Appends numbers while keeping the file extension intact (e.g., file_1.txt)
                counter = 1
                while os.path.exists(target_quarantine):
                    target_quarantine = os.path.join(QUARANTINE_DIR, f"{name}_{counter}{extension}")
                    counter += 1
                
                shutil.move(file_path, target_quarantine)
                quarantined_files_count += 1
                total_space_freed += file_size

        except Exception:
            # Silently ignore locked files or files currently in use by the OS
            pass

execution_time = round(time.time() - start_time, 2)
space_mb = round(total_space_freed / (1024 * 1024), 2)

# 2. GRAPHICAL REPORT (Pop-up window)
report_message = (
    f"✨ Cleanup completed in {execution_time} seconds!\n\n"
    f"📊 REPORT:\n"
    f"• Junk files permanently deleted: {direct_deleted_files}\n"
    f"• Uncertain files moved to quarantine: {quarantined_files_count}\n"
    f"• Total space recovered: {space_mb} MB\n\n"
    f"Uncertain files have been moved to your Desktop in the folder:\n'{os.path.basename(QUARANTINE_DIR)}'\n\n"
    f"Would you like to open the folder and check if you want to save anything?"
)

wants_to_review = messagebox.askyesno("Cleanup Report", report_message)

# 3. SAFETY REVIEW MANAGEMENT
if wants_to_review:
    # User choice: Review folder content before wiping the remaining files
    messagebox.showinfo("Instructions", "Please check the quarantine folder on your Desktop. Move OUT any files you wish to keep.\n\nWhen you are done, click OK on this window to permanently delete the rest.")
    if os.path.exists(QUARANTINE_DIR):
        shutil.rmtree(QUARANTINE_DIR)
else:
    # User choice: Wipe the entire quarantine directory immediately
    if os.path.exists(QUARANTINE_DIR):
        shutil.rmtree(QUARANTINE_DIR)

# 4. FINAL STEP: WINDOWS RECYCLE BIN
empty_trash = messagebox.askyesno("Final Step", "Would you like to empty the Windows Recycle Bin as well?")
if empty_trash:
    try:
        # Native Windows API call to empty the Recycle Bin without bringing up the system confirmation dialog
        ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 7)
        messagebox.showinfo("Success!", "Recycle Bin emptied. Cleanup process successfully finished!")
    except Exception:
        messagebox.showinfo("Notice", "Could not empty the Recycle Bin (it might already be empty).")
else:
    messagebox.showinfo("Finished!", "Cleanup complete. Recycle Bin preserved!")



