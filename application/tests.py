from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from .models import Course, Lesson, Quiz, QuizQuestion, QuizOption, User


class FinalProjectFlowTests(TestCase):
    def setUp(self):
        cache.clear()
        self.free_course = Course.objects.create(
            title="Free HSK Basics",
            slug="free-hsk-basics",
            category="HSK",
            description="Open beginner course",
            is_published=True,
        )
        Lesson.objects.create(
            course=self.free_course,
            lesson_order=1,
            title="Hello and numbers",
            duration_minutes=12,
        )
        self.premium_course = Course.objects.create(
            title="Premium Business Chinese",
            slug="premium-business-chinese",
            category="Business",
            description="Advanced paid course",
            is_published=True,
            is_premium=True,
        )
        Lesson.objects.create(
            course=self.premium_course,
            lesson_order=1,
            title="Premium negotiation lesson",
            duration_minutes=25,
        )
        quiz = Quiz.objects.create(
            course=self.free_course,
            title="Starter quiz",
            pass_score=60,
            is_active=True,
        )
        question = QuizQuestion.objects.create(
            quiz=quiz,
            question_order=1,
            question_text="What does ni hao mean?",
        )
        QuizOption.objects.create(
            question=question,
            option_label="A",
            option_text="Hello",
            is_correct=True,
        )

    def test_public_pages_render(self):
        for route_name in ["index", "login", "signup", "course", "quiz", "about"]:
            response = self.client.get(reverse(route_name))
            self.assertEqual(response.status_code, 200, route_name)

    def test_user_can_register_login_and_logout(self):
        signup_response = self.client.post(
            reverse("signup"),
            {
                "username": "student",
                "email": "student@example.com",
                "preferred_language": "en",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )
        self.assertRedirects(signup_response, reverse("index"))
        self.assertTrue(User.objects.filter(username="student").exists())

        self.client.get(reverse("logout"))
        login_response = self.client.post(
            reverse("login"),
            {"username": "student@example.com", "password": "StrongPass123!"},
        )
        self.assertRedirects(login_response, reverse("index"))

        logout_response = self.client.get(reverse("logout"))
        self.assertRedirects(logout_response, reverse("index"))

    def test_free_user_sees_premium_course_locked(self):
        user = User.objects.create_user(
            username="free-user",
            email="free@example.com",
            password="StrongPass123!",
        )
        self.client.force_login(user)
        response = self.client.get(reverse("course"))
        self.assertContains(response, "Premium Business Chinese")
        self.assertContains(response, "Upgrade to Premium")
        self.assertNotContains(response, "Premium negotiation lesson")

    def test_premium_user_sees_premium_lessons(self):
        user = User.objects.create_user(
            username="premium-user",
            email="premium@example.com",
            password="StrongPass123!",
            is_premium=True,
        )
        self.client.force_login(user)
        response = self.client.get(reverse("course"))
        self.assertContains(response, "Premium negotiation lesson")

    def test_course_api_marks_locked_premium_content(self):
        response = self.client.get("/api/courses/")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        premium = next(item for item in payload if item["slug"] == "premium-business-chinese")
        self.assertTrue(premium["is_premium"])
        self.assertTrue(premium["is_locked"])
        self.assertEqual(premium["lessons"], [])

        premium_user = User.objects.create_user(
            username="api-premium",
            email="api-premium@example.com",
            password="StrongPass123!",
            is_premium=True,
        )
        self.client.force_login(premium_user)
        response = self.client.get("/api/courses/")
        payload = response.json()
        premium = next(item for item in payload if item["slug"] == "premium-business-chinese")
        self.assertFalse(premium["is_locked"])
        self.assertEqual(premium["lessons"][0]["title"], "Premium negotiation lesson")
