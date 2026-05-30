from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import redirect, render
from rest_framework import permissions, viewsets

from .forms import EmailOrUsernameLoginForm, SignUpForm
from .models import (
    Course,
    CourseEnrollment,
    LearningActivity,
    LearningGoal,
    Lesson,
    Quiz,
    QuizAttempt,
    QuizAttemptAnswer,
    QuizOption,
    QuizQuestion,
    User,
    UserLessonProgress,
)
from .serializers import (
    CourseEnrollmentSerializer,
    CourseSerializer,
    LearningActivitySerializer,
    LearningGoalSerializer,
    LessonSerializer,
    QuizAttemptAnswerSerializer,
    QuizAttemptSerializer,
    QuizOptionSerializer,
    QuizQuestionSerializer,
    QuizSerializer,
    UserLessonProgressSerializer,
    UserSerializer,
)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Public users can read learning content; only staff can change it."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


def user_has_premium(user):
    return bool(user.is_authenticated and user.has_active_premium)


def published_courses():
    return (
        Course.objects.filter(is_published=True)
        .prefetch_related("lessons")
        .order_by("category", "title")
    )


def active_quizzes():
    return (
        Quiz.objects.filter(is_active=True)
        .select_related("course")
        .prefetch_related("questions__options")
        .order_by("title")
    )


# ---------- Django template pages ----------

def index(request):
    context = {
        "completed_lessons": 0,
        "completed_quizzes": 0,
        "study_hours": 0,
        "overall_progress": 0,
        "activities": [],
        "premium_courses_count": Course.objects.filter(is_premium=True, is_published=True).count(),
        "has_premium": user_has_premium(request.user),
    }

    if request.user.is_authenticated:
        completed_lessons = UserLessonProgress.objects.filter(
            user=request.user, status="completed"
        ).count()
        completed_quizzes = QuizAttempt.objects.filter(
            user=request.user, submitted_at__isnull=False
        ).count()
        study_minutes = sum(
            UserLessonProgress.objects.filter(user=request.user).values_list(
                "study_time_minutes", flat=True
            )
        )
        activities = LearningActivity.objects.filter(user=request.user).order_by("-created_at")[:5]
        context.update(
            {
                "completed_lessons": completed_lessons,
                "completed_quizzes": completed_quizzes,
                "study_hours": round(study_minutes / 60, 1),
                "overall_progress": min(100, (completed_lessons + completed_quizzes) * 10),
                "activities": activities,
            }
        )

    return render(request, "application/index.html", context)


def course_page(request):
    cache_key = "published_courses"
    courses = cache.get(cache_key)
    if courses is None:
        courses = list(published_courses())
        cache.set(cache_key, courses, 60 * 5)

    return render(
        request,
        "application/course.html",
        {
            "courses": courses,
            "has_premium": user_has_premium(request.user),
        },
    )


def quiz_page(request):
    cache_key = "active_quizzes"
    quizzes = cache.get(cache_key)
    if quizzes is None:
        quizzes = list(active_quizzes())
        cache.set(cache_key, quizzes, 60 * 5)

    return render(
        request,
        "application/quiz.html",
        {
            "quizzes": quizzes,
            "has_premium": user_has_premium(request.user),
        },
    )


def about_page(request):
    return render(request, "application/about.html")


def signup_page(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Registration successful. Welcome to Learn Chinese!")
            return redirect("index")
    else:
        form = SignUpForm()

    return render(request, "application/signup.html", {"form": form})


def login_page(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = EmailOrUsernameLoginForm(request.POST)
        if form.is_valid():
            auth_login(request, form.cleaned_data["user"])
            messages.success(request, "Login successful.")
            return redirect("index")
    else:
        form = EmailOrUsernameLoginForm()

    return render(request, "application/login.html", {"form": form})


@login_required
def logout_page(request):
    auth_logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("index")


# ---------- DRF API ----------

class LearningGoalViewSet(viewsets.ModelViewSet):
    queryset = LearningGoal.objects.all()
    serializer_class = LearningGoalSerializer
    permission_classes = [IsAdminOrReadOnly]


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return User.objects.select_related("goal").all()


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = Course.objects.prefetch_related("lessons")
        if self.request.user.is_staff:
            return queryset.all()
        return queryset.filter(is_published=True)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.select_related("course").all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminOrReadOnly]


class CourseEnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = CourseEnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = CourseEnrollment.objects.select_related("user", "course")
        if not self.request.user.is_authenticated:
            return queryset.none()
        if self.request.user.is_staff:
            return queryset.all()
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserLessonProgressViewSet(viewsets.ModelViewSet):
    serializer_class = UserLessonProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = UserLessonProgress.objects.select_related("user", "lesson", "lesson__course")
        if not self.request.user.is_authenticated:
            return queryset.none()
        if self.request.user.is_staff:
            return queryset.all()
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class QuizViewSet(viewsets.ModelViewSet):
    serializer_class = QuizSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = Quiz.objects.select_related("course").prefetch_related("questions__options")
        if self.request.user.is_staff:
            return queryset.all()
        return queryset.filter(is_active=True)


class QuizQuestionViewSet(viewsets.ModelViewSet):
    queryset = QuizQuestion.objects.select_related("quiz").prefetch_related("options").all()
    serializer_class = QuizQuestionSerializer
    permission_classes = [IsAdminOrReadOnly]


class QuizOptionViewSet(viewsets.ModelViewSet):
    queryset = QuizOption.objects.select_related("question", "question__quiz").all()
    serializer_class = QuizOptionSerializer
    permission_classes = [IsAdminOrReadOnly]


class QuizAttemptViewSet(viewsets.ModelViewSet):
    serializer_class = QuizAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = QuizAttempt.objects.select_related("user", "quiz").prefetch_related("answers")
        if not self.request.user.is_authenticated:
            return queryset.none()
        if self.request.user.is_staff:
            return queryset.all()
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class QuizAttemptAnswerViewSet(viewsets.ModelViewSet):
    serializer_class = QuizAttemptAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = QuizAttemptAnswer.objects.select_related(
            "attempt", "attempt__user", "question", "selected_option"
        )
        if not self.request.user.is_authenticated:
            return queryset.none()
        if self.request.user.is_staff:
            return queryset.all()
        return queryset.filter(attempt__user=self.request.user)


class LearningActivityViewSet(viewsets.ModelViewSet):
    serializer_class = LearningActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = LearningActivity.objects.select_related(
            "user", "related_course", "related_lesson", "related_quiz"
        )
        if not self.request.user.is_authenticated:
            return queryset.none()
        if self.request.user.is_staff:
            return queryset.all()
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
