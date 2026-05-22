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
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"


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
