from django.shortcuts import render , redirect
from django.contrib.auth import logout
from .forms import UserRegistrationForm

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserRegistrationForm()
        
    return render(request, "register.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

# Create your views here.
