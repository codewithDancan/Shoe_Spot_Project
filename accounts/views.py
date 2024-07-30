from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from .models import User
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .forms import UserUpdateProfileForm

@login_required(login_url="login")
def home_view(request):
    return render(request, "index.html")


def register_view(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["password2"]

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username Taken")
                # return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Taken")
                return redirect("register")
            else:
                new_user = User.objects.create_user(first_name=first_name, last_name=last_name,
                                                    username=username, email=email, password=password)
                new_user.save()
                messages.success(request, "Account successfully created")
                #return redirect("login")
        else:
            messages.info(request, "Password Not Matching")
            return redirect("register")
        
    return render(request, "accounts/register.html")



def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Credentials Invalid")  
    return render(request, "accounts/login.html")


@login_required(login_url="login")  
def password_reset_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            link = request.build_absolute_uri(f"/reset_password/{uid}/{token}/")
            mail_subject = "Reset your password"
            message = render_to_string("password_reset_email.html", {
                "user": user,
                "link": link,
            })
            send_mail(mail_subject, message, "shoe@gmail.com", [email])
            messages.success(request, "An email has been sent with instructions to reset your password.")
            return redirect("login")
        else:
            messages.error(request, "No account found with that email address.")
    return render(request, "accounts/forgotpassword.html")


@login_required(login_url="login")
def profile_update_view(request):
    if request.method == "POST":
        user_form = UserUpdateProfileForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Your profile has been updated successfully")
            return redirect("profile-update")
    else:
        user_form = UserUpdateProfileForm()

    return render(request, "accounts/profile-update.html", {"user_form": user_form})


@login_required(login_url="login")
def logout_view(request):
    auth.logout(request)
    return render(request, "login")


def single(request):

    return render(request, "agent-single.html")