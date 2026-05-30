from rest_framework import serializers

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


class LearningGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningGoal
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    goal_name = serializers.CharField(source="goal.name", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "goal",
            "goal_name",
            "preferred_language",
            "is_premium",
            "premium_until",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("is_active", "created_at", "updated_at")


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField()
    is_locked = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_is_locked(self, obj) -> bool:
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not obj.is_premium:
            return False
        return not bool(user and user.is_authenticated and user.has_active_premium)

    def get_lessons(self, obj) -> list:
        if self.get_is_locked(obj):
            return []
        return LessonSerializer(obj.lessons.all(), many=True).data


class CourseEnrollmentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    course_title = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = CourseEnrollment
        fields = "__all__"


class UserLessonProgressSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    lesson_title = serializers.CharField(source="lesson.title", read_only=True)

    class Meta:
        model = UserLessonProgress
        fields = "__all__"


class QuizOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizOption
        fields = "__all__"


class QuizQuestionSerializer(serializers.ModelSerializer):
    options = QuizOptionSerializer(many=True, read_only=True)

    class Meta:
        model = QuizQuestion
        fields = "__all__"


class QuizSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)
    questions = QuizQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = "__all__"


class QuizAttemptAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttemptAnswer
        fields = "__all__"


class QuizAttemptSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    answers = QuizAttemptAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = QuizAttempt
        fields = "__all__"


class LearningActivitySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = LearningActivity
        fields = "__all__"
