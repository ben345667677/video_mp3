import os
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv
import concurrent.futures
from threading import Lock


# number of processing in one time each
multi_processing = 5

# טוען את משתני הסביבה מקובץ .env
load_dotenv()

# הגדרת OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# נתיבים
AUDIO_DIR = Path('output/audio')
TEXT_DIR = Path('output/text')
LOG_DIR = Path('output/log')

# יצירת תקיות אם לא קיימות
TEXT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# קבצי לוג
ERROR_LOG = LOG_DIR / 'errors.log'
EXISTS_LOG = LOG_DIR / 'existing_files.log'

# נעילה לכתיבה בטוחה ללוגים
log_lock = Lock()


def write_to_log(log_file, message):
    """כותב הודעה ללוג בצורה thread-safe"""
    with log_lock:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"{message}\n")


def transcribe_audio(audio_file_path):
    """מתמלל קובץ אודיו בודד"""
    audio_file = Path(audio_file_path)
    text_file = TEXT_DIR / f"{audio_file.stem}.txt"

    # בדיקה אם הקובץ כבר קיים
    if text_file.exists():
        write_to_log(EXISTS_LOG, f"קובץ קיים: {text_file.name}")
        return f"דולג על {audio_file.name} - קובץ טקסט כבר קיים"

    try:
        # פתיחת קובץ האודיו ושליחה ל-Whisper API
        with open(audio_file, 'rb') as audio:
            transcript = client.audio.transcriptions.create(
                model="gpt-4o-transcribe",  # המודל הטוב ביותר הזמין
                file=audio,
                language=None  # זיהוי אוטומטי של השפה
            )

        # שמירת התמליל
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(transcript.text)

        return f"הושלם: {audio_file.name}"

    except Exception as e:
        error_msg = f"שגיאה בקובץ {audio_file.name}: {str(e)}"
        write_to_log(ERROR_LOG, error_msg)
        return error_msg


def main():
    # בדיקה שתקיית האודיו קיימת
    if not AUDIO_DIR.exists():
        print(f"שגיאה: תקיית {AUDIO_DIR} לא קיימת")
        return

    # איסוף כל קבצי האודיו
    audio_files = []
    for ext in ['*.mp3', '*.wav', '*.m4a', '*.flac']:
        audio_files.extend(AUDIO_DIR.glob(ext))

    if not audio_files:
        print("לא נמצאו קבצי אודיו בתקייה")
        return

    print(f"נמצאו {len(audio_files)} קבצי אודיו")
    print("מתחיל תמליל...")

    # אתחול קבצי לוג (מנקה את הקבצים הקיימים)
    ERROR_LOG.write_text('', encoding='utf-8')
    EXISTS_LOG.write_text('', encoding='utf-8')

    # עיבוד מקבילי של קבצי האודיו (מקסימום 10 בו-זמנית)
    with concurrent.futures.ThreadPoolExecutor(max_workers=multi_processing) as executor:
        future_to_file = {executor.submit(transcribe_audio, audio_file): audio_file
                          for audio_file in audio_files}

        completed = 0
        for future in concurrent.futures.as_completed(future_to_file):
            result = future.result()
            completed += 1
            print(f"[{completed}/{len(audio_files)}] {result}")

    # בדיקה אם היו שגיאות
    has_errors = ERROR_LOG.stat().st_size > 0
    has_existing = EXISTS_LOG.stat().st_size > 0

    print("\n" + "=" * 50)
    print("התמליל הושלם!")

    if has_errors or has_existing:
        print("\n⚠️  נמצאו בעיות - בדוק את קבצי הלוג:")
        if has_errors:
            print(f"   • שגיאות: {ERROR_LOG}")
        if has_existing:
            print(f"   • קבצים קיימים: {EXISTS_LOG}")
    else:
        print("✅ כל הקבצים עובדו בהצלחה!")


if __name__ == "__main__":
    main()