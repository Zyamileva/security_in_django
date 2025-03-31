from django.contrib.auth import logout
from django.http import HttpRequest

from .forms import CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect


def register(request:HttpRequest):
    """Registers a new user.

     Handles user registration using a custom form, authenticates the user, and redirects to the home page upon successful registration.
     """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("home")
            else:
                return redirect("login")
    else:
        form = CustomUserCreationForm()

    return render(request, "main/register.html", {"form": form})


def user_login(request):
    """Logs in an existing user.

    Handles user login using a custom form and redirects to the home page upon successful authentication.
    """
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Ви успішно увійшли!")
            return redirect("home")
        else:
            messages.error(request, "Неправильне ім'я користувача або пароль.")
    else:
        form = CustomAuthenticationForm()
    return render(request, "main/login.html", {"form": form})


@login_required
def user_logout(request:HttpRequest):
    """Logs out the current user.

    Logs out the user, displays a message, and redirects to the login page.
    """
    logout(request)
    messages.info(request, "Ви вийшли з системи.")
    return redirect("login")


@login_required
def home(request):
    """Displays the home page.

    Renders the home page for logged-in users.
    """
    return render(request, "main/home.html")
