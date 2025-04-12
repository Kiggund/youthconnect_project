from django.shortcuts import render
from .models import Leader

def leader_list(request):
    leaders = Leader.objects.all()  # Retrieve all leaders
    return render(request, 'leaders/leader_list.html', {'leaders': leaders})
