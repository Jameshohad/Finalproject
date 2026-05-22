from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from application import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("course/", views.course_page, name="course"),
    path("quiz/", views.quiz_page, name="quiz"),
    path("about/", views.about_page, name="about"),
    path("login/", views.login_page, name="login"),
    path("signup/", views.signup_page, name="signup"),
    path("logout/", views.logout_page, name="logout"),
    path("api/", include("application.api_urls")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
