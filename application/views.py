from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
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
        .order_by("display_order", "title")
    )


def free_lesson_queryset():
    return Lesson.objects.filter(course__is_published=True, course__is_premium=False)


def free_path_progress(user):
    total_lessons = free_lesson_queryset().count()
    if not user.is_authenticated:
        return {
            "completed_lesson_ids": [],
            "free_lessons_total": total_lessons,
            "free_lessons_completed": 0,
            "free_progress_percent": 0,
            "has_completed_free_path": False,
        }

    completed_lesson_ids = list(
        UserLessonProgress.objects.filter(
            user=user,
            status="completed",
            lesson__course__is_published=True,
            lesson__course__is_premium=False,
        ).values_list("lesson_id", flat=True)
    )
    completed_count = len(completed_lesson_ids)
    progress_percent = round((completed_count / total_lessons) * 100) if total_lessons else 0
    return {
        "completed_lesson_ids": completed_lesson_ids,
        "free_lessons_total": total_lessons,
        "free_lessons_completed": completed_count,
        "free_progress_percent": min(100, progress_percent),
        "has_completed_free_path": total_lessons > 0 and completed_count >= total_lessons,
    }


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
            **free_path_progress(request.user),
        },
    )


@login_required
@require_POST
def complete_lesson(request, lesson_id):
    lesson = get_object_or_404(
        Lesson.objects.select_related("course"),
        pk=lesson_id,
        course__is_published=True,
    )

    if lesson.course.is_premium and not user_has_premium(request.user):
        messages.error(request, "This lesson is part of Premium. Complete the free path first, then ask an admin to activate Premium.")
        return redirect("course")

    now = timezone.now()
    progress, created = UserLessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson,
        defaults={
            "status": "completed",
            "completed_at": now,
            "last_accessed_at": now,
            "study_time_minutes": lesson.duration_minutes,
        },
    )
    was_completed = progress.status == "completed"
    if not was_completed:
        progress.status = "completed"
        progress.completed_at = now
        progress.study_time_minutes = max(progress.study_time_minutes, lesson.duration_minutes)
    progress.last_accessed_at = now
    progress.save()

    course_lesson_ids = lesson.course.lessons.values_list("id", flat=True)
    course_lesson_count = lesson.course.lessons.count()
    completed_in_course = UserLessonProgress.objects.filter(
        user=request.user,
        lesson_id__in=course_lesson_ids,
        status="completed",
    ).count()
    course_progress = round((completed_in_course / course_lesson_count) * 100, 2) if course_lesson_count else 0
    enrollment, _ = CourseEnrollment.objects.get_or_create(
        user=request.user,
        course=lesson.course,
        defaults={"status": "in_progress"},
    )
    enrollment.progress_percent = course_progress
    if course_lesson_count and completed_in_course >= course_lesson_count:
        enrollment.status = "completed"
        enrollment.completed_at = enrollment.completed_at or now
    enrollment.save()

    if created or not was_completed:
        LearningActivity.objects.create(
            user=request.user,
            activity_type="lesson_view",
            title=f"Completed {lesson.title}",
            description=f"Finished a lesson in {lesson.course.title}.",
            related_course=lesson.course,
            related_lesson=lesson,
        )
        messages.success(request, f"Lesson completed: {lesson.title}")
    else:
        messages.info(request, f"You already completed: {lesson.title}")

    return redirect("course")


def quiz_page(request):
    quizzes = list(active_quizzes())
    if request.user.is_authenticated:
        latest_attempts = {}
        attempts = QuizAttempt.objects.filter(
            user=request.user,
            submitted_at__isnull=False,
            quiz__in=quizzes,
        ).order_by("-submitted_at")
        for attempt in attempts:
            latest_attempts.setdefault(attempt.quiz_id, attempt)
        for quiz in quizzes:
            quiz.latest_attempt = latest_attempts.get(quiz.id)

    return render(
        request,
        "application/quiz.html",
        {
            "quizzes": quizzes,
            "has_premium": user_has_premium(request.user),
        },
    )


@login_required
@require_POST
def submit_quiz(request, quiz_id):
    quiz = get_object_or_404(
        Quiz.objects.prefetch_related("questions__options"),
        pk=quiz_id,
        is_active=True,
    )
    questions = list(quiz.questions.all())
    if not questions:
        messages.error(request, "This quiz does not have questions yet.")
        return redirect("quiz")

    now = timezone.now()
    correct_count = 0
    attempt = QuizAttempt.objects.create(
        user=request.user,
        quiz=quiz,
        total_questions=len(questions),
        submitted_at=now,
    )

    for question in questions:
        selected_option_id = request.POST.get(f"question_{question.id}")
        selected_option = None
        is_correct = False
        if selected_option_id:
            selected_option = question.options.filter(id=selected_option_id).first()
            is_correct = bool(selected_option and selected_option.is_correct)
        if is_correct:
            correct_count += 1
        QuizAttemptAnswer.objects.create(
            attempt=attempt,
            question=question,
            selected_option=selected_option,
            is_correct=is_correct,
        )

    score_percent = round((correct_count / len(questions)) * 100)
    attempt.score = score_percent
    attempt.save(update_fields=["score"])

    passed = score_percent >= quiz.pass_score
    LearningActivity.objects.create(
        user=request.user,
        activity_type="quiz_pass" if passed else "quiz_fail",
        title=f"{'Passed' if passed else 'Practiced'} {quiz.title}",
        description=f"Score: {score_percent}% ({correct_count}/{len(questions)} correct).",
        related_course=quiz.course,
        related_quiz=quiz,
    )
    messages.success(
        request,
        f"{quiz.title} submitted. Score: {score_percent}% ({correct_count}/{len(questions)} correct).",
    )
    return redirect("quiz")


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
        queryset = Course.objects.prefetch_related("lessons").order_by("display_order", "title")
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
