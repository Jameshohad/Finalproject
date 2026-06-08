from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class LearningGoal(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "learning_goals"

    def __str__(self):
        return self.name


class User(AbstractUser):
    email = models.EmailField(unique=True)
    goal = models.ForeignKey(
        LearningGoal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users"
    )
    preferred_language = models.CharField(max_length=10, default="zh-CN")
    is_premium = models.BooleanField(default=False)
    premium_until = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username

    @property
    def has_active_premium(self):
        if self.is_staff or self.is_superuser:
            return True
        if not self.is_premium:
            return False
        return self.premium_until is None or self.premium_until >= timezone.now()


class Course(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    category = models.CharField(max_length=50)
    level_name = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    external_link = models.URLField(blank=True, null=True)
    display_order = models.IntegerField(default=0)
    is_premium = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "courses"
        ordering = ["display_order", "title"]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    lesson_order = models.IntegerField()
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True, null=True)
    duration_minutes = models.IntegerField(default=0)
    video_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "lessons"
        ordering = ["lesson_order"]

    def __str__(self):
        return self.title


class CourseEnrollment(models.Model):
    STATUS_CHOICES = [
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("dropped", "Dropped"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="course_enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="in_progress")
    progress_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "course_enrollments"
        unique_together = ("user", "course")

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"


class UserLessonProgress(models.Model):
    STATUS_CHOICES = [
        ("not_started", "Not Started"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lesson_progress")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="user_progress")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="not_started")
    study_time_minutes = models.IntegerField(default=0)
    completed_at = models.DateTimeField(blank=True, null=True)
    last_accessed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "user_lesson_progress"
        unique_together = ("user", "lesson")

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"


class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name="quizzes")
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    pass_score = models.IntegerField(default=60)
    total_questions = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "quizzes"

    def __str__(self):
        return self.title


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question_order = models.IntegerField()
    question_text = models.TextField()
    explanation = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "quiz_questions"
        ordering = ["question_order"]

    def __str__(self):
        return f"{self.quiz.title} - Q{self.question_order}"


class QuizOption(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name="options")
    option_label = models.CharField(max_length=10, blank=True, null=True)
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    class Meta:
        db_table = "quiz_options"

    def __str__(self):
        return self.option_text


class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quiz_attempts")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "quiz_attempts"

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"


class QuizAttemptAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name="attempt_answers")
    selected_option = models.ForeignKey(
        QuizOption,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="selected_in_answers"
    )
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "quiz_attempt_answers"

    def __str__(self):
        return f"Answer {self.id}"


class LearningActivity(models.Model):
    ACTIVITY_CHOICES = [
        ("course_start", "Course Start"),
        ("lesson_view", "Lesson View"),
        ("quiz_attempt", "Quiz Attempt"),
        ("quiz_pass", "Quiz Pass"),
        ("quiz_fail", "Quiz Fail"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="learning_activities")
    activity_type = models.CharField(max_length=30, choices=ACTIVITY_CHOICES)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=255, blank=True, null=True)
    related_course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name="activities")
    related_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, related_name="activities")
    related_quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True, blank=True, related_name="activities")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "learning_activities"

    def __str__(self):
        return f"{self.user.username} - {self.activity_type}"
