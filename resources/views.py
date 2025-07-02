from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required  # ✅ Add this line

# 🔐 Protect the view with login_required
@login_required(login_url='join:login')
def index(request):
    return render(request, 'resources.html')
