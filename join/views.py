from django.shortcuts import render, redirect
from .forms import MemberForm

def index(request):
    """Home page view"""
    return render(request, 'join/join.html')

def register(request):
    """Registration form view"""
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('join:success')
        else:
            print(form.errors)  # Debug form errors
    else:
        form = MemberForm()
    return render(request, 'join/register.html', {'form': form})

def success(request):
    """Success page after registration"""
    return render(request, 'join/success.html')

def contact(request):
    """Contact page view"""
    return render(request, 'join/contact.html')
