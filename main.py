import os
import subprocess
from pydub import AudioSegment, silence

VIDEO_DIR = "video"
AUDIO_DIR = "audio"
CHUNK_LENGTH_MS = 14 * 60 * 1000  # 14 דקות במילישניות
LOOKBACK_MS = 60 * 1000           # דקה אחרונה לבדוק בה שקט
SILENCE_THRESH_DB = -40           # סף שקט (dBFS)
SILENCE_MIN_MS = 200              # מינימום שקט 0.2 שניות
MIN_SEGMENT_MS = 5000             # מינימום קטע שמור (5 שניות)

def video_to_audio(video_path, audio_path):
    """ממיר וידאו ל-MP3"""
    subprocess.run([
        "ffmpeg", "-i", video_path,
        "-vn", "-acodec", "mp3", audio_path, "-y"
    ])

def split_audio(audio_path, output_dir):
    """פיצול אודיו לקטעים כרונולוגיים, עם שמות לפי זמן"""
    os.makedirs(output_dir, exist_ok=True)
    audio = AudioSegment.from_file(audio_path)

    start = 0
    part = 0

    while start < len(audio):
        end = min(start + CHUNK_LENGTH_MS, len(audio))
        segment = audio[start:end]

        # נחפש שקט בדקה האחרונה של המקטע
        search_start = max(0, len(segment) - LOOKBACK_MS)
        last_minute = segment[search_start:]
        silence_ranges = silence.detect_silence(
            last_minute,
            min_silence_len=SILENCE_MIN_MS,
            silence_thresh=segment.dBFS + SILENCE_THRESH_DB
        )

        if silence_ranges:
            cut_point = search_start + silence_ranges[0][0]
            segment = segment[:cut_point]

        if len(segment) < MIN_SEGMENT_MS:
            print("⚠️ קטע קצר מדי – דילוג")
            start = end
            continue

        # חישוב טווח הזמן לשם
        start_min = start // 60000
        end_min = (start + len(segment)) // 60000
        out_name = f"{start_min:04d}-{end_min:04d}min.mp3"
        out_path = os.path.join(output_dir, out_name)

        segment.export(out_path, format="mp3")
        print(f"✅ נשמר: {out_path} ({len(segment)/1000:.1f} שניות)")

        # ממשיכים מהסוף של הקטע ששמרנו
        start += len(segment)
        part += 1

if __name__ == "__main__":
    os.makedirs(AUDIO_DIR, exist_ok=True)

    files = [f for f in os.listdir(VIDEO_DIR) if f.endswith((".mp4", ".mkv", ".mov"))]
    if not files:
        print("❌ לא נמצא קובץ וידאו בתיקיית video/")
        exit(1)

    video_file = os.path.join(VIDEO_DIR, files[0])
    audio_file = os.path.join(AUDIO_DIR, "full_audio.mp3")

    print(f"🎬 ממיר וידאו לאודיו: {video_file}")
    video_to_audio(video_file, audio_file)

    print("✂️ מפצל לקטעי 14 דקות כרונולוגיים עם חיתוך על שקט...")
    split_audio(audio_file, AUDIO_DIR)

    print("🏁 סיימתי! הקבצים נמצאים בתיקיית audio/")
