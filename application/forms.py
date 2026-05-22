from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "goal", "preferred_language", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.goal = self.cleaned_data.get("goal")
        user.preferred_language = self.cleaned_data.get("preferred_language") or "zh-CN"
        if commit:
            user.save()
        return user


class EmailOrUsernameLoginForm(forms.Form):
    username = forms.CharField(label="用户名或邮箱", max_length=254)
    password = forms.CharField(label="密码", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username_or_email and password:
            username = username_or_email
            if "@" in username_or_email:
                try:
                    username = User.objects.get(email=username_or_email).username
                except User.DoesNotExist:
                    username = username_or_email

            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("用户名/邮箱或密码不正确。")
            if not user.is_active:
                raise forms.ValidationError("该账户已被禁用。")
            cleaned_data["user"] = user
        return cleaned_data
