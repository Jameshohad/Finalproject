from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from rest_framework import permissions, viewsets

from .forms import EmailOrUsernameLoginForm, SignUpForm
from .models import (
    LearningGoal,
    User,
    Course,
    Lesson,
    CourseEnrollment,
    UserLessonProgress,
    Quiz,
    QuizQuestion,
    QuizOption,
    QuizAttempt,
    QuizAttemptAnswer,
    LearningActivity,
)
from .serializers import (
    LearningGoalSerializer,
    UserSerializer,
    CourseSerializer,
    LessonSerializer,
    CourseEnrollmentSerializer,
    UserLessonProgressSerializer,
    QuizSerializer,
    QuizQuestionSerializer,
    QuizOptionSerializer,
    QuizAttemptSerializer,
    QuizAttemptAnswerSerializer,
    LearningActivitySerializer,
)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Public can read published learning content; only staff can create/update/delete."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


# ---------- Django template pages ----------

def index(request):
    context = {
        "completed_lessons": 0,
        "completed_quizzes": 0,
        "study_hours": 0,
        "overall_progress": 0,
        "activities": [],
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
    courses = (
        Course.objects.filter(is_published=True)
        .prefetch_related("lessons")
        .order_by("category", "title")
    )
    return render(request, "application/course.html", {"courses": courses})


def quiz_page(request):
    quizzes = (
        Quiz.objects.filter(is_active=True)
        .select_related("course")
        .prefetch_related("questions__options")
        .order_by("title")
    )
    return render(request, "application/quiz.html", {"quizzes": quizzes})


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
            messages.success(request, "注册成功，欢迎开始学习中文！")
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
            messages.success(request, "登录成功！")
            return redirect("index")
    else:
        form = EmailOrUsernameLoginForm()

    return render(request, "application/login.html", {"form": form})


@login_required
def logout_page(request):
    auth_logout(request)
    messages.success(request, "已登出。")
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
        if self.request.user.is_staff:
            return queryset.all()
        return queryset.filter(attempt__user=self.request.user)


class LearningActivityViewSet(viewsets.ModelViewSet):
    serializer_class = LearningActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = LearningActivity.objects.select_related("user", "related_course", "related_lesson", "related_quiz")
        if self.request.user.is_staff:
            return queryset.all()
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
