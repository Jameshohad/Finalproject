from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "you@example.com"}),
    )
    preferred_language = forms.ChoiceField(
        label="Preferred language",
        choices=(("zh-CN", "Chinese"), ("en", "English")),
        initial="zh-CN",
    )

    class Meta:
        model = User
        fields = ("username", "email", "goal", "preferred_language", "password1", "password2")
        labels = {
            "username": "Username",
            "goal": "Learning goal",
        }
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Choose a username"}),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.goal = self.cleaned_data.get("goal")
        user.preferred_language = self.cleaned_data.get("preferred_language") or "zh-CN"
        if commit:
            user.save()
        return user


class EmailOrUsernameLoginForm(forms.Form):
    username = forms.CharField(
        label="Username or email",
        max_length=254,
        widget=forms.TextInput(attrs={"placeholder": "Username or email"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username_or_email and password:
            username = username_or_email
            if "@" in username_or_email:
                try:
                    username = User.objects.get(email=username_or_email.lower()).username
                except User.DoesNotExist:
                    username = username_or_email

            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("The username/email or password is incorrect.")
            if not user.is_active:
                raise forms.ValidationError("This account is disabled.")
            cleaned_data["user"] = user
        return cleaned_data
