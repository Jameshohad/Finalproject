from rest_framework.routers import DefaultRouter
from .views import (
    LearningGoalViewSet, UserViewSet, CourseViewSet, LessonViewSet,
    CourseEnrollmentViewSet, UserLessonProgressViewSet, QuizViewSet,
    QuizQuestionViewSet, QuizOptionViewSet, QuizAttemptViewSet,
    QuizAttemptAnswerViewSet, LearningActivityViewSet
)

router = DefaultRouter()
router.register(r'learning-goals', LearningGoalViewSet)
router.register(r'users', UserViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'course-enrollments', CourseEnrollmentViewSet)
router.register(r'user-lesson-progress', UserLessonProgressViewSet)
router.register(r'quizzes', QuizViewSet)
router.register(r'quiz-questions', QuizQuestionViewSet)
router.register(r'quiz-options', QuizOptionViewSet)
router.register(r'quiz-attempts', QuizAttemptViewSet)
router.register(r'quiz-attempt-answers', QuizAttemptAnswerViewSet)
router.register(r'learning-activities', LearningActivityViewSet)

urlpatterns = router.urls