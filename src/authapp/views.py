from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View

from authapp.models import User

context ={}

class LoginPageView(TemplateView):
    global context
    template_name = "authapp/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # return redirect("mainapp:index")
            return render(request, "mainapp/index.html", context)
        # return super().get(request, *args, **kwargs)
        return render(request, "authapp/login.html", context)

    def post(self, request, *args, **kwargs):
        context = {}
        if request.user.is_authenticated:
            return redirect("mainapp:index")
        user = authenticate(
            username=request.POST.get("username"), password=request.POST.get("password")
        )
        if user is not None:
            login(request, user)
            return redirect("mainapp:index")
        else:
            # messages.error(self.request, "Invalid username or password")
            context["error"] = "Invalid username or password"
            return render(request, "authapp/login.html", context)


class RegisterPageView(TemplateView):
    template_name = "authapp:register.html"
    global context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("mainapp:index")
        # return super().get(request, *args, **kwargs)
        return render(request, "authapp/register.html", context)

    def post(self, request, *args, **kwargs):
        context = {}
        username = request.POST.get("username")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")
        if not all([username, password, password_confirm]):
            # return redirect("register")
            context["error"] = "Введите все поля"
            return render(request,"authapp/register.html", context)
        if password != password_confirm:
            context["error"] = "Введите пароль правильно"
            return render(request, "authapp/register.html", context)
        user = User(username=username)
        user.set_password(password)
        try:
            user.save()
            context = {}
            # return redirect("login")
            return render(request, "authapp/login.html")
        except Exception:
            context["error"] = "Username Already in use"
            return render(request,"authapp/register.html", context)



class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        # return redirect("mainapp:index")
        return render(request, "mainapp/index.html")
