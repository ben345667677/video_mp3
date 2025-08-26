import os
import tiktoken

# ==== הגדרות ====
FOLDER_PATH = "text"   # שים כאן את נתיב התיקייה שלך
MODEL = "gpt-5"                  # המודל שבו תרצה לחשב טוקנים
# =================

enc = tiktoken.encoding_for_model(MODEL)

def count_tokens_in_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        tokens = enc.encode(text)
        return len(tokens)
    except Exception as e:
        print(f"שגיאה בקריאת הקובץ {file_path}: {e}")
        return 0

def count_tokens_in_folder(folder_path):
    total_tokens = 0
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_tokens = count_tokens_in_file(file_path)
            print(f"{file_path} → {file_tokens} טוקנים")
            total_tokens += file_tokens
    return total_tokens

if __name__ == "__main__":
    total = count_tokens_in_folder(FOLDER_PATH)
    print(f"\nסה״כ טוקנים בכל התיקייה: {total}")