from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.core.cache import cache

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


@admin.register(LearningGoal)
class LearningGoalAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "description")
    search_fields = ("code", "name")


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Learning profile", {"fields": ("goal", "preferred_language", "is_premium", "premium_until")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
    readonly_fields = ("created_at", "updated_at")
    list_display = ("username", "email", "goal", "is_premium", "premium_until", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "is_premium", "goal")
    search_fields = ("username", "email")


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ("lesson_order", "title", "duration_minutes", "video_url", "content")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "level_name", "is_premium", "is_published", "created_at")
    list_filter = ("category", "level_name", "is_premium", "is_published")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [LessonInline]

    def save_model(self, request, obj, form, change):
        cache.delete("published_courses")
        super().save_model(request, obj, form, change)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "lesson_order", "duration_minutes", "created_at")
    list_filter = ("course",)
    search_fields = ("title", "content")
    ordering = ("course", "lesson_order")


class QuizOptionInline(admin.TabularInline):
    model = QuizOption
    extra = 4
    fields = ("option_label", "option_text", "is_correct")


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ("quiz", "question_order", "question_text")
    list_filter = ("quiz",)
    search_fields = ("question_text",)
    inlines = [QuizOptionInline]
    ordering = ("quiz", "question_order")


class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 1
    fields = ("question_order", "question_text", "explanation")


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "pass_score", "total_questions", "is_active", "created_at")
    list_filter = ("is_active", "course")
    search_fields = ("title", "description")
    inlines = [QuizQuestionInline]

    def save_model(self, request, obj, form, change):
        cache.delete("active_quizzes")
        super().save_model(request, obj, form, change)


@admin.register(QuizOption)
class QuizOptionAdmin(admin.ModelAdmin):
    list_display = ("question", "option_label", "option_text", "is_correct")
    list_filter = ("is_correct",)
    search_fields = ("option_text",)


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "status", "progress_percent", "started_at", "completed_at")
    list_filter = ("status", "course")
    search_fields = ("user__username", "course__title")


@admin.register(UserLessonProgress)
class UserLessonProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "status", "study_time_minutes", "completed_at", "last_accessed_at")
    list_filter = ("status", "lesson__course")
    search_fields = ("user__username", "lesson__title")


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ("user", "quiz", "score", "total_questions", "started_at", "submitted_at")
    list_filter = ("quiz",)
    search_fields = ("user__username", "quiz__title")


@admin.register(QuizAttemptAnswer)
class QuizAttemptAnswerAdmin(admin.ModelAdmin):
    list_display = ("attempt", "question", "selected_option", "is_correct", "answered_at")
    list_filter = ("is_correct",)


@admin.register(LearningActivity)
class LearningActivityAdmin(admin.ModelAdmin):
    list_display = ("user", "activity_type", "title", "related_course", "created_at")
    list_filter = ("activity_type", "related_course")
    search_fields = ("user__username", "title", "description")
