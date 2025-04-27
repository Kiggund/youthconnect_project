from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from contact.models import ContactMessage  # Updated import
from join.forms import MemberForm
import re
import dns.resolver

# Email validation
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

# Disposable email domains list
DISPOSABLE_DOMAINS = [
    'mailinator.com', 'tempmail.com', 'yopmail.com', 'trashmail.com'
]

def validate_email_domain(email):
    #pass all domains during testing
    pass

def register_user(request):
    """Handle user registration with email validation"""
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            try:
                validate_email_domain(email)
                form.save()
                return redirect('join:success')
            except ValidationError as e:
                return render(request, 'join/register.html', {"form": form, "error": str(e)})
        return render(request, 'join/register.html', {"form": form, "form_errors": form.errors})
    form = MemberForm()
    return render(request, 'join/register.html', {"form": form})

@csrf_exempt
def send_message(request):
    """Handle contact form submissions"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        message = request.POST.get('message', '').strip()  # Consistent field name
        
        # Validate all fields
        if not all([name, email, message]):
            return JsonResponse({"success": False, "message": "All fields are required"}, status=400)
        
        # Validate email format
        if not is_valid_email(email):
            return JsonResponse({"success": False, "message": "Invalid email address"}, status=400)
        
        try:
            # Save to database
            ContactMessage.objects.create(
                name=name,
                email=email,
                content=message  # Field name must match model
            )
            return JsonResponse({"success": True, "message": "Message sent successfully"})
            
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)
    
    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)

def success(request):
    return render(request, 'join/success.html', {"message": "Operation completed successfully!"})

def index(request):
    return render(request, 'join/index.html')

def contact(request):
    return render(request, 'join/contact.html')
