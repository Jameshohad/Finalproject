from django.db import migrations, models


DEMO_COURSES = [
    {
        "title": "HSK 1 Starter Course",
        "slug": "hsk-1-starter-course",
        "category": "Free",
        "level_name": "Starter",
        "description": "Start with pinyin, tones, greetings, numbers, and the first sentence patterns every Chinese learner needs.",
        "external_link": "https://www.youtube.com/results?search_query=hsk+1+chinese+lesson",
        "display_order": 10,
        "is_premium": False,
        "lessons": [
            (1, "Pinyin, tones, and greetings", 15, "Learn how Chinese sounds work, then say hello and introduce yourself."),
            (2, "Numbers, dates, and time", 18, "Use numbers for ages, prices, days, and simple schedules."),
            (3, "Basic word order", 20, "Build your first subject-verb-object Chinese sentences."),
        ],
    },
    {
        "title": "Daily Conversation",
        "slug": "daily-conversation",
        "category": "Free",
        "level_name": "Beginner",
        "description": "Practice everyday Chinese for greetings, shopping, restaurants, and simple personal questions.",
        "external_link": "https://www.youtube.com/results?search_query=daily+chinese+conversation+lesson",
        "display_order": 20,
        "is_premium": False,
        "lessons": [
            (1, "Meeting people and asking simple questions", 16, "Ask names, nationalities, and how someone is doing."),
            (2, "Shopping and restaurant language", 18, "Use polite phrases for prices, ordering food, and asking for help."),
            (3, "Short daily conversations", 20, "Connect phrases into two-way conversations you can actually use."),
        ],
    },
    {
        "title": "Travel Chinese Essentials",
        "slug": "travel-chinese-essentials",
        "category": "Free",
        "level_name": "Practical",
        "description": "Useful phrases for airports, hotels, restaurants, directions, and common travel problems.",
        "external_link": "https://www.youtube.com/results?search_query=travel+chinese+phrases",
        "display_order": 30,
        "is_premium": False,
        "lessons": [
            (1, "Airport and hotel phrases", 14, "Check in, ask for a room, and handle simple travel requests."),
            (2, "Ordering food politely", 16, "Read common menu words and order meals with confidence."),
            (3, "Directions and emergencies", 15, "Ask where to go, understand basic answers, and request urgent help."),
        ],
    },
    {
        "title": "Sentence Building and Grammar",
        "slug": "sentence-building-and-grammar",
        "category": "Premium",
        "level_name": "Intermediate",
        "description": "Move from memorized phrases to flexible sentences with grammar patterns, connectors, and longer answers.",
        "external_link": "https://www.youtube.com/results?search_query=chinese+grammar+sentence+patterns",
        "display_order": 40,
        "is_premium": True,
        "lessons": [
            (1, "From words to full sentences", 22, "Turn vocabulary into clear sentences with time, place, and action."),
            (2, "Because, so, but, and then", 24, "Use connectors to explain reasons and tell short stories."),
            (3, "Speaking in longer answers", 26, "Practice moving from one sentence to a complete spoken response."),
        ],
    },
    {
        "title": "Business Chinese",
        "slug": "business-chinese",
        "category": "Premium",
        "level_name": "Professional",
        "description": "Chinese for meetings, polite disagreement, email, presentations, and workplace communication.",
        "external_link": "https://www.youtube.com/results?search_query=business+chinese+lesson",
        "display_order": 50,
        "is_premium": True,
        "lessons": [
            (1, "Meetings and introductions", 22, "Introduce your role, explain an agenda, and ask professional questions."),
            (2, "Negotiation and polite disagreement", 28, "State opinions clearly while keeping the conversation respectful."),
            (3, "Short business messages", 24, "Write and speak concise professional updates in Chinese."),
        ],
    },
    {
        "title": "Chinese Culture and Poetry",
        "slug": "chinese-culture-and-poetry",
        "category": "Premium",
        "level_name": "Advanced",
        "description": "Learn cultural context, idioms, short poems, and expressive Chinese for richer communication.",
        "external_link": "https://www.youtube.com/results?search_query=chinese+culture+poetry+lesson",
        "display_order": 60,
        "is_premium": True,
        "lessons": [
            (1, "Culture in everyday expressions", 20, "Understand common cultural references behind natural Chinese phrases."),
            (2, "Idioms and short stories", 24, "Use simple chengyu and story-based expressions in context."),
            (3, "Reading a short poem aloud", 26, "Practice rhythm, tone, and meaning through a short classical poem."),
        ],
    },
]


def seed_subscription_demo(apps, schema_editor):
    Course = apps.get_model("application", "Course")
    Lesson = apps.get_model("application", "Lesson")

    demo_slugs = [item["slug"] for item in DEMO_COURSES]
    Course.objects.exclude(slug__in=demo_slugs).update(is_published=False)

    for item in DEMO_COURSES:
        lessons = item["lessons"]
        defaults = {
            "title": item["title"],
            "category": item["category"],
            "level_name": item["level_name"],
            "description": item["description"],
            "external_link": item["external_link"],
            "display_order": item["display_order"],
            "is_premium": item["is_premium"],
            "is_published": True,
        }
        course, _ = Course.objects.update_or_create(slug=item["slug"], defaults=defaults)
        for order, title, duration, content in lessons:
            Lesson.objects.update_or_create(
                course=course,
                lesson_order=order,
                defaults={
                    "title": title,
                    "duration_minutes": duration,
                    "content": content,
                },
            )


def unseed_subscription_demo(apps, schema_editor):
    Course = apps.get_model("application", "Course")
    Course.objects.filter(
        slug__in=[
            "sentence-building-and-grammar",
            "business-chinese",
            "chinese-culture-and-poetry",
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("application", "0003_seed_demo_content"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="display_order",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterModelOptions(
            name="course",
            options={"ordering": ["display_order", "title"]},
        ),
        migrations.RunPython(seed_subscription_demo, unseed_subscription_demo),
    ]
