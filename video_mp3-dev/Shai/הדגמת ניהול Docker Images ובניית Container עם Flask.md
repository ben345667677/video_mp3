## סיכום התוכן הלימודי

**נושא הלימוד:** הדגמה מעשית של עבודה עם Docker - ניהול images וcontainers, ובניית image חדש.

**מה דובר בחלק זה:** המרצה הסביר על פקודות Dockerfile, בעיקר PIP INSTALL REQUIREMENTS שמתקין תלויות ו-CMD שמשמש כנקודת כניסה להרצת האפליקציה (APP.PY). לאחר מכן עבר להדגמה מעשית של ניהול Docker images - מחיקת images ישנים, ניקוי containers לא פעילים, והתחלת תהליך בניית image חדש.

**כלים וטכנולוגיות שהוזכרו:**

- Docker (פקודות שונות)
- Flask (אפליקציה לדוגמה)
- Python
- MySQL
- Dockerfile
- requirements.txt
- app.py

## סיכום כרונולוגי של הפעילות:

1. **הסבר תיאורטי** - פירוט פקודות Dockerfile (PIP INSTALL REQUIREMENTS, CMD)
2. **רישום images קיימים** - הרצת `docker image ls` לראיה כלל הimages
3. **מחיקת images ישנים** - ניסיון למחוק images של Flask (`docker image rm`)
4. **פתרון בעיות** - התמודדות עם שגיאת מחיקה עקב container קיים
5. **ניקוי containers** - הרצת `docker container prune` למחיקת containers לא פעילים
6. **ניקוי images נוסף** - שימוש ב-`docker image prune` למחיקת images שלא בשימוש
7. **בעיות טכניות** - התמודדות עם בעיות במחיקת images
8. **התחלת בניית image** - תחילת הדגמה של `docker build` עם tag

---

**כותרת התוכן:** הדגמת ניהול Docker Images ובניית Container עם Flask