# Finalproject first fix patch

This patch focuses on the first coding problem: content added in Django Admin should appear on the website.

## How to apply

1. Back up your project or commit your current work:
   ```bash
   git add . && git commit -m "backup before first fix"
   ```
2. Copy these files into your project root and overwrite the existing files.
3. Install missing packages only if you use the settings snippet:
   ```bash
   pip install python-dotenv django-redis
   ```
4. Run:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```
5. In `/admin/`, add:
   - Course: title, slug, category, description, external_link, and set `is_published=True`
   - Lesson under Course
   - Quiz with `is_active=True`
   - QuizQuestion and QuizOption
6. Check:
   - `/course/` now displays courses from the database.
   - `/quiz/` now displays quizzes from the database.
   - `/api/courses/` and `/api/quizzes/` return JSON.

## Notes

- This patch does not fully finish Docker, report, presentation, or front-end React migration.
- It keeps Django templates because the project PDF allows Django Templates as one frontend option.
- If your teacher specifically requires React + DRF, keep these APIs and later create a separate `frontend/` React app that fetches from `/api/courses/` and `/api/quizzes/`.
