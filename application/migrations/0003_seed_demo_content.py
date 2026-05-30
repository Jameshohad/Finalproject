from django.db import migrations


def seed_demo_content(apps, schema_editor):
    LearningGoal = apps.get_model("application", "LearningGoal")
    Course = apps.get_model("application", "Course")
    Lesson = apps.get_model("application", "Lesson")
    Quiz = apps.get_model("application", "Quiz")
    QuizQuestion = apps.get_model("application", "QuizQuestion")
    QuizOption = apps.get_model("application", "QuizOption")

    goals = [
        ("beginner", "Beginner Chinese", "Build basic vocabulary and daily phrases."),
        ("daily", "Daily conversation", "Practice everyday conversations and situations."),
        ("business", "Business Chinese", "Learn professional expressions for work."),
        ("travel", "Travel Chinese", "Prepare for restaurants, hotels, transport, and directions."),
    ]
    for code, name, description in goals:
        LearningGoal.objects.get_or_create(
            code=code,
            defaults={"name": name, "description": description},
        )

    course_data = [
        {
            "title": "HSK 1 Starter Course",
            "slug": "hsk-1-starter-course",
            "category": "HSK",
            "level_name": "Beginner",
            "description": "Learn greetings, numbers, pronouns, and simple sentence patterns.",
            "external_link": "https://www.youtube.com/results?search_query=hsk+1+chinese+lesson",
            "is_premium": False,
            "lessons": [
                (1, "Greetings and self-introduction", 15),
                (2, "Numbers, dates, and time", 18),
                (3, "Basic sentence order", 20),
            ],
        },
        {
            "title": "Travel Chinese Essentials",
            "slug": "travel-chinese-essentials",
            "category": "Travel",
            "level_name": "Practical",
            "description": "Useful phrases for airports, hotels, restaurants, and asking directions.",
            "external_link": "https://www.youtube.com/results?search_query=travel+chinese+phrases",
            "is_premium": False,
            "lessons": [
                (1, "Airport and hotel phrases", 14),
                (2, "Ordering food politely", 16),
                (3, "Asking for directions", 13),
            ],
        },
        {
            "title": "Premium Business Chinese",
            "slug": "premium-business-chinese-course",
            "category": "Business",
            "level_name": "Premium",
            "description": "Advanced workplace Chinese for meetings, negotiation, and client emails.",
            "external_link": "https://www.youtube.com/results?search_query=business+chinese+lesson",
            "is_premium": True,
            "lessons": [
                (1, "Meeting introductions and agenda language", 22),
                (2, "Negotiation phrases and polite disagreement", 28),
                (3, "Writing short business messages", 24),
            ],
        },
    ]

    created_courses = {}
    for item in course_data:
        lessons = item.pop("lessons")
        course, _ = Course.objects.get_or_create(slug=item["slug"], defaults=item)
        created_courses[item["slug"]] = course
        for order, title, duration in lessons:
            Lesson.objects.get_or_create(
                course=course,
                lesson_order=order,
                defaults={
                    "title": title,
                    "duration_minutes": duration,
                    "content": f"Demo lesson content for {title}.",
                },
            )

    quiz, _ = Quiz.objects.get_or_create(
        title="Starter Chinese Quiz",
        defaults={
            "course": created_courses["hsk-1-starter-course"],
            "description": "A short quiz for basic Chinese words.",
            "pass_score": 60,
            "total_questions": 3,
            "is_active": True,
        },
    )

    questions = [
        (1, "What does ni hao mean?", [("A", "Hello", True), ("B", "Goodbye", False), ("C", "Thanks", False)]),
        (2, "How do you say thank you in Chinese?", [("A", "Zaijian", False), ("B", "Xiexie", True), ("C", "Wo", False)]),
        (3, "Which phrase means goodbye?", [("A", "Ni hao", False), ("B", "Xiexie", False), ("C", "Zaijian", True)]),
    ]
    for order, text, options in questions:
        question, _ = QuizQuestion.objects.get_or_create(
            quiz=quiz,
            question_order=order,
            defaults={"question_text": text, "explanation": "Review the HSK 1 starter vocabulary."},
        )
        for label, option_text, is_correct in options:
            QuizOption.objects.get_or_create(
                question=question,
                option_label=label,
                defaults={"option_text": option_text, "is_correct": is_correct},
            )


def unseed_demo_content(apps, schema_editor):
    Course = apps.get_model("application", "Course")
    LearningGoal = apps.get_model("application", "LearningGoal")
    Quiz = apps.get_model("application", "Quiz")

    Quiz.objects.filter(title="Starter Chinese Quiz").delete()
    Course.objects.filter(
        slug__in=[
            "hsk-1-starter-course",
            "travel-chinese-essentials",
            "premium-business-chinese-course",
        ]
    ).delete()
    LearningGoal.objects.filter(code__in=["beginner", "daily", "business", "travel"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("application", "0002_premium_fields"),
    ]

    operations = [
        migrations.RunPython(seed_demo_content, unseed_demo_content),
    ]
