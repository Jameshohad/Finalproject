from rest_framework import viewsets
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
    LearningActivity
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
    LearningActivitySerializer
)

from django.shortcuts import render

 #前端页面添加

def about_page(request):
    return render(request, "application/about.html")

def course_page(request):
    return render(request, "application/course.html")

def index(request):
    return render(request, "application/index.html")

def login(request):
    return render(request, "application/login.html")

def quiz_page(request):
    return render(request, "application/quiz.html")

def signup(request):
    return render(request, "application/signup.html")

class LearningGoalViewSet(viewsets.ModelViewSet):
    queryset = LearningGoal.objects.all()
    serializer_class = LearningGoalSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class CourseEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = CourseEnrollment.objects.all()
    serializer_class = CourseEnrollmentSerializer


class UserLessonProgressViewSet(viewsets.ModelViewSet):
    queryset = UserLessonProgress.objects.all()
    serializer_class = UserLessonProgressSerializer


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuizQuestionViewSet(viewsets.ModelViewSet):
    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionSerializer


class QuizOptionViewSet(viewsets.ModelViewSet):
    queryset = QuizOption.objects.all()
    serializer_class = QuizOptionSerializer


class QuizAttemptViewSet(viewsets.ModelViewSet):
    queryset = QuizAttempt.objects.all()
    serializer_class = QuizAttemptSerializer


class QuizAttemptAnswerViewSet(viewsets.ModelViewSet):
    queryset = QuizAttemptAnswer.objects.all()
    serializer_class = QuizAttemptAnswerSerializer


class LearningActivityViewSet(viewsets.ModelViewSet):
    queryset = LearningActivity.objects.all()
    serializer_class = LearningActivitySerializer