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
from .forms import UserUpdateProfileForm,PasswordChangeForm
from django.contrib.auth import get_user_model,update_session_auth_hash
from products.models import Shoe, ShoeAttribute


@login_required(login_url="login-view")
def home_view(request):
    shoes = Shoe.objects.all()
    
    context = {
        'shoes': shoes,
    }
    return render(request, "index.html", context)

from django.contrib.auth.models import User, Group
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
                return redirect("register-view")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Taken")
                return redirect("register-view")
            else:
                new_user = User.objects.create_user(first_name=first_name, last_name=last_name,
                                                    username=username, email=email, password=password)
                customer_group, created = Group.objects.get_or_create(name='customer')
                new_user.save()
                new_user.groups.add(customer_group)
                messages.success(request, "Account successfully created")
                return redirect("login-view")
        else:
            messages.info(request, "Password Not Matching")
            return redirect("register-view")
        
    return render(request, "accounts/register.html")



def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Credentials Invalid")  
    return render(request, "accounts/login.html")



def password_reset_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            link = request.build_absolute_uri(f"/reset_password/{uid}/{token}/")
            mail_subject = "Reset your password"
            message = render_to_string("email_template/password_reset_email.html", {
                    "user": user,
                    "link": link,
                })
            send_mail(mail_subject, message, "shoe@gmail.com", [email])
            print("email")
            messages.success(request, "An email has been sent with instructions to reset your password.")
            return redirect("login-view")
        else:
            messages.info(request, "No account found with that email address.")
    return render(request, "accounts/forgotpassword.html")



User = get_user_model()

def reset_password(request, uid, token):
    try:
        uid = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your password has been reset successfully.')
                return redirect('login-view')  # Redirect to a login page or any other page
            else:
                messages.error(request, 'Passwords do not match.')
        return render(request, 'accounts/reset_password_form.html', {'user': user})
    else:
        messages.error(request, 'The password reset link is invalid, possibly because it has already been used. Please request a new password reset.')
        return redirect('forgot-password')



@login_required(login_url="login-view")
def profile_update_view(request):
    if request.method == "POST":
        user_form = UserUpdateProfileForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Your profile has been updated successfully")
            return redirect("user-profile")
        else:
            messages.success(request, user_form.errors)
            return redirect("user-profile")
    return redirect("user-profile")


@login_required(login_url="login-view")
def profile_password_change(request):
    referer_url = request.META.get('HTTP_REFERER')  
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password has been changed successfully')
            return redirect(referer_url)
        else:
            messages.error(request, form.errors )
    return redirect(referer_url)



def logout_view(request):
    auth.logout(request)
    return redirect("login-view")




@login_required(login_url="login-view")
def user_profile(request):
    user_form = UserUpdateProfileForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)
    return render(request, "user-profile.html",{'form':user_form,'form1':password_form})