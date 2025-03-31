from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError

from main.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form.

    This form extends the default UserCreationForm to include email and add custom validation for username and password.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "example@mail.com"}),
    )

    class Meta:
        """Meta class for CustomUserCreationForm.

        Specifies the model and fields used in the form.
        """
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def clean_username(self):
        """Validates the username field.

        Checks if the username is at least 3 characters long and contains only alphanumeric characters.
        """
        username = self.cleaned_data.get("username")
        if len(username) < 3:
            raise ValidationError("Ім'я користувача має містити принаймні 3 символи.")
        if not username.isalnum():
            raise ValidationError(
                "Ім'я користувача повинно містити лише літери та цифри."
            )
        return username

    def clean_email(self):
        """Validates the email field.

        Checks if the email is already in use.
        """
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Цей email вже використовується.")
        return email

    def clean_password1(self):
        """Validates the password1 field.

        Checks if the password meets certain criteria: minimum length, at least one digit, and at least one uppercase letter.
        """
        password = self.cleaned_data.get("password1")
        if len(password) < 8:
            raise ValidationError("Пароль має містити принаймні 8 символів.")
        if not any(char.isdigit() for char in password):
            raise ValidationError("Пароль має містити принаймні одну цифру.")
        if not any(char.isupper() for char in password):
            raise ValidationError("Пароль має містити принаймні одну велику літеру.")
        return password


class CustomAuthenticationForm(AuthenticationForm):
    """Custom authentication form.

    This form extends the default AuthenticationForm to customize username and password fields.
    """
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
