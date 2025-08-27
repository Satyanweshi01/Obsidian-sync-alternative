import os
import shutil
import subprocess
import tkinter as tk
from tkinter import messagebox

# Config
file_to_encrypt = r"your_obsidian_file_location"
archive_name = "your_new_archived_file_name.7z"  # Keep static name
google_drive_folder = r"your_google_driver_folder_location"
desktop = r"your_pull_folder_location"
seven_zip_path = r"your_7z.exe_location"  # Path to 7z.exe

# Use a prewritten password
PREWRITTEN_PASSWORD = "your_password"  # Replace with your desired password

def get_password():
    return PREWRITTEN_PASSWORD  # Always return the same password

def delete_existing_archive(path):
    if os.path.exists(path):
        try:
            os.remove(path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete existing archive:\n{e}")
            return False
    return True

def encrypt_with_7zip():
    try:
        password = get_password()
        archive_path = os.path.join(google_drive_folder, archive_name)

        if not delete_existing_archive(archive_path):
            return None  # Failed to delete existing archive

        cmd = [
            seven_zip_path,
            'a', archive_path,
            file_to_encrypt,
            f'-p{password}',
            '-mhe=on',       # encrypt header
            '-y',            # assume Yes on all queries
            '-mx=0'          # no compression (fast)
        ]
        subprocess.run(cmd, check=True)
        return archive_path
    except Exception as e:
        messagebox.showerror("Error", f"Encryption failed:\n{e}")
        return None

def push_file():
    archive_path = encrypt_with_7zip()
    if archive_path and os.path.exists(archive_path):
        messagebox.showinfo("Success", "Encrypted file stored in Google Drive folder.")
    else:
        messagebox.showerror("Error", "Archive not found after encryption.")

def pull_file():
    try:
        source = os.path.join(google_drive_folder, archive_name)
        destination = os.path.join(desktop, archive_name)
        shutil.copy(source, destination)
        messagebox.showinfo("Success", "Encrypted file pulled to Desktop.")
    except Exception as e:
        messagebox.showerror("Error", f"Pull failed:\n{e}")

# GUI
root = tk.Tk()
root.title("Encrypted Drive Sync")
root.geometry("300x150")

tk.Button(root, text="Push", command=push_file, width=30, height=2).pack(pady=10)
tk.Button(root, text="Pull", command=pull_file, width=30, height=2).pack()

root.mainloop()
