from django.contrib import admin
from .models import (
    LearningGoal, User, Course, Lesson, CourseEnrollment,
    UserLessonProgress, Quiz, QuizQuestion, QuizOption,
    QuizAttempt, QuizAttemptAnswer, LearningActivity
)

admin.site.register(LearningGoal)
admin.site.register(User)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(CourseEnrollment)
admin.site.register(UserLessonProgress)
admin.site.register(Quiz)
admin.site.register(QuizQuestion)
admin.site.register(QuizOption)
admin.site.register(QuizAttempt)
admin.site.register(QuizAttemptAnswer)
admin.site.register(LearningActivity)
