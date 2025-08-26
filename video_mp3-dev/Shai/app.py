#!/usr/bin/env python3
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote
import mimetypes


class LessonHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, base_path=None, **kwargs):
        self.base_path = base_path or os.getcwd()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == '/':
            self.serve_file('index.html')
        elif self.path == '/api/lessons':
            self.serve_lessons_list()
        elif self.path.startswith('/api/file/'):
            filename = unquote(self.path[10:])  # Remove '/api/file/'
            self.serve_markdown_file(filename)
        else:
            self.serve_file(self.path[1:])  # Remove leading '/'

    def serve_file(self, filepath):
        try:
            full_path = os.path.join(self.base_path, filepath)
            if os.path.exists(full_path) and os.path.isfile(full_path):
                with open(full_path, 'rb') as f:
                    content = f.read()

                content_type, _ = mimetypes.guess_type(filepath)
                if content_type is None:
                    content_type = 'text/plain'

                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error(404, "File not found")
        except Exception as e:
            print(f"Error serving file {filepath}: {e}")
            self.send_error(500, str(e))

    def serve_lessons_list(self):
        try:
            # קריאת קובץ מערך השיעור
            syllabus_file = os.path.join(self.base_path, "מערך השיעור.md")
            lessons = []

            if os.path.exists(syllabus_file):
                lessons = self.parse_syllabus_file(syllabus_file)
            else:
                # אם אין קובץ מערך שיעור, סרוק את כל קבצי ה-MD
                lessons = self.scan_md_files()

            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()

            response = json.dumps(lessons, ensure_ascii=False)
            self.wfile.write(response.encode('utf-8'))

        except Exception as e:
            print(f"Error serving lessons list: {e}")
            self.send_error(500, str(e))

    def parse_syllabus_file(self, filepath):
        """פענוח קובץ מערך השיעור"""
        lessons = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line and (line.startswith('1.') or line.startswith('2.') or
                             any(line.startswith(f'{i}.') for i in range(1, 20))):

                    # חילוץ מספר השיעור
                    parts = line.split('.', 1)
                    if len(parts) >= 2:
                        try:
                            num = int(parts[0])
                            title_part = parts[1].strip()

                            # חילוץ הכותרת מתוך [[ ]]
                            if '[[' in title_part and ']]' in title_part:
                                start = title_part.find('[[') + 2
                                end = title_part.find(']]')
                                title = title_part[start:end]

                                # בדיקה אם יש בעיה
                                is_problem = '(בעיה)' in title_part

                                filename = title + '.md'

                                lessons.append({
                                    'num': num,
                                    'title': title,
                                    'file': filename,
                                    'problem': is_problem
                                })
                        except ValueError:
                            continue

        except Exception as e:
            print(f"Error parsing syllabus: {e}")

        return lessons

    def scan_md_files(self):
        """סריקת כל קבצי MD בתיקייה"""
        lessons = []
        md_files = [f for f in os.listdir(self.base_path) if f.endswith('.md')]

        for i, filename in enumerate(sorted(md_files), 1):
            title = filename.replace('.md', '')
            lessons.append({
                'num': i,
                'title': title,
                'file': filename,
                'problem': False
            })

        return lessons

    def serve_markdown_file(self, filename):
        try:
            filepath = os.path.join(self.base_path, filename)

            if not os.path.exists(filepath):
                self.send_error(404, f"File not found: {filename}")
                return

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Content-Length', str(len(content.encode('utf-8'))))
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))

        except Exception as e:
            print(f"Error serving markdown file {filename}: {e}")
            self.send_error(500, str(e))

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()


def create_handler(base_path):
    def handler(*args, **kwargs):
        return LessonHandler(*args, base_path=base_path, **kwargs)

    return handler


def main():
    import sys

    # קבלת נתיב התיקייה מהמשתמש
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = input("הכנס את הנתיב לתיקייה עם קבצי ה-MD (או Enter לתיקייה הנוכחית): ").strip()
        if not base_path:
            base_path = os.getcwd()

    # וידוא שהנתיב קיים
    if not os.path.exists(base_path):
        print(f"❌ התיקייה {base_path} לא קיימת!")
        return

    # מעבר לתיקייה
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    PORT = 8000
    handler = create_handler(base_path)

    try:
        with HTTPServer(("", PORT), handler) as httpd:
            print(f"🚀 השרת רץ על http://localhost:{PORT}")
            print(f"📁 מגיש קבצים מהתיקייה: {base_path}")

            # בדיקה אם קיים קובץ מערך השיעור
            syllabus_path = os.path.join(base_path, "מערך השיעור.md")
            if os.path.exists(syllabus_path):
                print("✅ נמצא קובץ 'מערך השיעור.md'")
            else:
                print("⚠️  לא נמצא קובץ 'מערך השיעור.md', יוצג כל קבצי ה-MD")

            print("לעצירת השרת: Ctrl+C")
            httpd.serve_forever()

    except KeyboardInterrupt:
        print("\n👋 השרת נעצר")
    except Exception as e:
        print(f"❌ שגיאה בהפעלת השרת: {e}")


if __name__ == "__main__":
    main()