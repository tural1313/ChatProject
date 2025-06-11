from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib import messages
from chatapp.models import UserMessage


def index(request):
    context = {}
    if request.user.is_authenticated:
        now = timezone.now()
        login_time = request.user.last_login
        login_duration = now - login_time
        login_seconds = login_duration.seconds
        login_minutes = login_seconds // 60
        context["login_minutes"] = login_minutes

        users = User.objects.filter(
            last_login__day = now.day
        )

        context["users"] = users

    return render(request, 'index.html', context)

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if username and email and password:
            if User.objects.filter(username=username).exists():
                messages.error(request, f"{username} movcuddur.")
            else:
                user = User.objects.create_user(
                    username = username, 
                    email = email,
                    password = password
                )
                login(request, user)
                return redirect("index")
        elif not username and not email and not password:
            messages.error(request, "Zehmet olmasa, melumatlari daxil edin.")
            return redirect('signup')
        else:
            if not username:
                messages.error(request, "Username daxil edin")
            if not email:
                messages.error(request, "Email daxil edin")
            if not password:
                messages.error(request, "Password daxil edin")
            return redirect('signup')

    return render(request, 'register.html')

def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')

    return render(request, 'login.html')

def signout(request):
    logout(request)
    return redirect("index")


def contact(request):
    if not request.user.is_authenticated:
        return redirect('error')

    if request.method == "POST":
        username = request.POST.get("full_name") 
        message = request.POST.get("message")

        if username and message:
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                if user == request.user:
                    messages.error(request, "Basqa bir istifadeci daxil edin.")
                else:
                    UserMessage.objects.create(
                        from_user = request.user,
                        to_user = user,
                        message = message
                    )
                    messages.success(request, "Mesajiniz gonderildi.")
            else:
                messages.error(request, "Bele bir istifadeci movcud deyil!")
        else:
            messages.error(request, 'Zehmet olmasa butun xanalari doldurun!')
        return redirect("direct")
    
        
    return render(request, 'contact.html')


def passwordreset(request):
    if not request.user.is_authenticated:
        return redirect('error')
    
    if request.method == "POST":
        choice = request.POST.get("choice")
        if choice == "create":
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            if password and confirm_password:
                if password == confirm_password:
                    user = request.user
                    user.set_password(password)
                    user.save()
                    messages.success(request, 'Parol yenilendi')
                else:
                    messages.error(request, 'Parollar uygun deyil')
            else:
                if not password:
                    messages.error(request, 'Parol daxil edin')
                else:
                    messages.error(request, "Parolu tesdiqleyin")
        return redirect('resetpassword')
    return render(request, 'password-reset.html')

def errorpage(request):
    return render(request, '404.html')

def inbox(request):
    if not request.user.is_authenticated:
        return redirect('error')
    inbox_messages = request.user.in_messages.all()

    if request.method == "POST":
        message_id = request.POST.get("message_id") # 5
        message = UserMessage.objects.get(id=message_id)
        message.delete()
        messages.success(request, 'Mesajiniz silindi.')
        return redirect('inbox')

    context = {
        'inbox_messages': inbox_messages
    }
    return render(request, 'inbox.html', context)

def outbox(request):
    if not request.user.is_authenticated:
        return redirect('error')
    return render(request, 'outbox.html')