#!/usr/bin/env python3
"""
סקריפט הפעלה מהיר עם GUI לבחירת תיקייה
"""
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess


def select_folder_and_run():
    root = tk.Tk()
    root.withdraw()  # הסתר חלון ראשי

    folder_path = filedialog.askdirectory(
        title="בחר תיקייה עם קבצי MD",
        initialdir=os.getcwd()
    )

    if folder_path:
        print(f"תיקייה נבחרה: {folder_path}")

        # הפעלת השרת עם הנתיב הנבחר
        try:
            subprocess.run([sys.executable, "app.py", folder_path])
        except KeyboardInterrupt:
            print("\n👋 השרת נעצר")
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בהפעלת השרת: {e}")
    else:
        print("לא נבחרה תיקייה")


if __name__ == "__main__":
    # אם יש ארגומנט, הפעל ישירות
    if len(sys.argv) > 1:
        subprocess.run([sys.executable, "app.py"] + sys.argv[1:])
    else:
        # אחרת, הצג GUI לבחירת תיקייה
        select_folder_and_run()