from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from contact.models import ContactMessage 
from join.forms import UserRegistrationForm, UserLoginForm
import re
import dns.resolver
import shutil

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

# youthconnect/views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache

@never_cache
@csrf_protect
@require_http_methods(["GET", "POST"])
def login_view(request):
    """Custom login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')  # Update with your actual dashboard URL name
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Update with your actual dashboard URL name
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'join/login.html')

# views.py
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.forms import PasswordResetForm

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get email from session
        context['email'] = self.request.session.get('password_reset_email', 'your@email.com')
        return context

class CustomPasswordResetForm(PasswordResetForm):
    def save(self, request, **kwargs):
        # Store email in session
        request.session['password_reset_email'] = self.cleaned_data['email']
        return super().save(request, **kwargs)

from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class CustomPasswordResetForm(PasswordResetForm):
    def save(self, request, **kwargs):
        email = self.cleaned_data["email"]
        request.session['reset_email'] = email  # Store email in session
        return super().save(
            request=request,
            use_https=request.is_secure(),
            token_generator=default_token_generator,
            from_email=None,
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt',
            html_email_template_name=None,
            extra_email_context=None
        )

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.request.session.get('reset_email', 'your@email.com')
        return context
