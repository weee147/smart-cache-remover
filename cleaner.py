import os
import time
import shutil
import ctypes
from tkinter import messagebox, Tk

# Hide the root empty tkinter window
root = Tk()
root.withdraw()

# Path configurations
CACHE_DIR = os.environ.get('TEMP')
QUARANTINE_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "Cleaner_Quarantine")

# Report metrics
direct_deleted_files = 0
quarantined_files = []
total_space_freed = 0

print("⚡ Running high-speed scan and cleanup...")
start_time = time.time()

# Create quarantine folder if it doesn't exist
if not os.path.exists(QUARANTINE_DIR):
    os.makedirs(QUARANTINE_DIR)

# 1. FAST PHASE: Scan & Sort
for root_path, dirs, files in os.walk(CACHE_DIR):
    for f in files:
        file_path = os.path.join(root_path, f)
        try:
            file_size = os.path.getsize(file_path)
            days_unused = (time.time() - os.path.getatime(file_path)) / (60 * 60 * 24)
            _, extension = os.path.splitext(f)

            # Category A: Obvious Junk (Immediate deletion)
            if extension.lower() in ['.tmp', '.log', '.bak'] or file_size == 0:
                # os.remove(file_path)
              print(f"[TEST] Would delete: {file_path}")
                direct_deleted_files += 1
                total_space_freed += file_size
            
            # Category B: Suspicious/Old Files (Sent to quarantine for safety)
            elif days_unused >50:
                target_quarantine = os.path.join(QUARANTINE_DIR, f)
                # Handle filename duplicates in quarantine
                if os.path.exists(target_quarantine):
                    target_quarantine = target_quarantine + "_duplicate"
                # shutil.move(file_path, target_quarantine)
              print(f"[TEST] Would quarantine: {file_path}")
                quarantined_files.append((target_quarantine, file_path))
                total_space_freed += file_size

        except Exception:
            # Silently skip system-locked files to keep maximum speed
            pass

execution_time = round(time.time() - start_time, 2)
space_mb = round(total_space_freed / (1024 * 1024), 2)

# 2. GRAPHICAL REPORT (Pop-up)
report_message = (
    f"✨ Cleanup completed in {execution_time} seconds!\n\n"
    f"📊 REPORT:\n"
    f"• Junk files permanently deleted: {direct_deleted_files}\n"
    f"• Uncertain files moved to quarantine: {len(quarantined_files)}\n"
    f"• Total space recovered: {space_mb} MB\n\n"
    f"Uncertain files have been moved to your Desktop in the folder:\n'{os.path.basename(QUARANTINE_DIR)}'\n\n"
    f"Would you like to open the folder and check if you want to save anything?"
)

wants_to_review = messagebox.askyesno("Cleanup Report", report_message)

# 3. SAFETY REVIEW MANAGEMENT
if wants_to_review:
    messagebox.showinfo("Instructions", "Please check the quarantine folder on your Desktop. Move out any files you wish to keep. Click OK when you are done to wipe the rest.")
else:
    # If the user clicks 'No', automatically wipe the quarantine folder
    if os.path.exists(QUARANTINE_DIR):
        shutil.rmtree(QUARANTINE_DIR)

# 4. FINAL STEP: RECYCLE BIN
empty_trash = messagebox.askyesno("Final Step", "Would you like to empty the system Recycle Bin as well?")
if empty_trash:
    try:
        ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 7)
        messagebox.showinfo("Success!", "Recycle Bin emptied. Cleanup process successfully finished!")
    except Exception:
        messagebox.showerror("Notice", "Could not empty the Recycle Bin (it might already be empty).")
else:
    messagebox.showinfo("Finished!", "Cleanup complete. Recycle Bin preserved!")
