from rest_framework.routers import DefaultRouter

from .views import (
    LearningGoalViewSet,
    UserViewSet,
    CourseViewSet,
    LessonViewSet,
    CourseEnrollmentViewSet,
    UserLessonProgressViewSet,
    QuizViewSet,
    QuizQuestionViewSet,
    QuizOptionViewSet,
    QuizAttemptViewSet,
    QuizAttemptAnswerViewSet,
    LearningActivityViewSet,
)

router = DefaultRouter()
router.register(r"learning-goals", LearningGoalViewSet, basename="learning-goal")
router.register(r"users", UserViewSet, basename="user")
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"lessons", LessonViewSet, basename="lesson")
router.register(r"course-enrollments", CourseEnrollmentViewSet, basename="course-enrollment")
router.register(r"user-lesson-progress", UserLessonProgressViewSet, basename="user-lesson-progress")
router.register(r"quizzes", QuizViewSet, basename="quiz")
router.register(r"quiz-questions", QuizQuestionViewSet, basename="quiz-question")
router.register(r"quiz-options", QuizOptionViewSet, basename="quiz-option")
router.register(r"quiz-attempts", QuizAttemptViewSet, basename="quiz-attempt")
router.register(r"quiz-attempt-answers", QuizAttemptAnswerViewSet, basename="quiz-attempt-answer")
router.register(r"learning-activities", LearningActivityViewSet, basename="learning-activity")

urlpatterns = router.urls
