# ======================
# IMPORTS                              # ======================
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods, require_POST   
from django.views.decorators.cache import never_cache
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from django.utils import timezone
from django.db import transaction, IntegrityError
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
import logging
import secrets
from .forms import UserRegistrationForm, UserLoginForm, UserEditForm, ProfileEditForm, OTPVerificationForm
from accounts.models import Profile
from django.contrib import messages

User = get_user_model()
logger = logging.getLogger(__name__)


# ======================
# UTILITY FUNCTIONS
# ======================
def generate_secure_otp() -> str:
    """Generate 6-digit cryptographically secure OTP"""
    return str(secrets.randbelow(10**6)).zfill(6)

def store_otp(email: str, otp: str) -> None:
    """Store OTP with timeout and reset attempts"""
    cache.set(f'otp_{email}', otp, timeout=settings.OTP_CONFIG['TIMEOUT'])
    cache.set(f'otp_attempts_{email}', 0, timeout=settings.OTP_CONFIG['LOCKOUT_DURATION'])

def verify_stored_otp(email: str, submitted_otp: str) -> bool:
    """Secure OTP verification with attempt tracking"""
    attempts = cache.get(f'otp_attempts_{email}', 0)
    if attempts >= settings.OTP_CONFIG['MAX_ATTEMPTS']:
        return False

    stored_otp = cache.get(f'otp_{email}')
    if not stored_otp:
        return False

    if not secrets.compare_digest(stored_otp, submitted_otp):
        cache.incr(f'otp_attempts_{email}')
        return False

    return True


# ======================
# AUTHENTICATION VIEWS
# ======================
@never_cache
def redirect_to_register(request: HttpRequest) -> HttpResponse:
    """Redirect to registration page"""
    return redirect(reverse("join:register"))

@never_cache
@csrf_protect
@require_http_methods(["GET", "POST"])
def register(request: HttpRequest) -> HttpResponse:
    """Handle user registration with OTP workflow and NIN validation"""
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save(commit=False)
                    user.is_active = False
                    user.save()

                    otp = generate_secure_otp()
                    store_otp(user.email, otp)

                    send_mail(
                        "Your Verification Code",
                        f"Your OTP is: {otp} (Valid for {settings.OTP_CONFIG['TIMEOUT']//60} minutes)",
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )

                    request.session['otp_email'] = user.email
                    request.session['otp_verified'] = False
                    return redirect('join:verify_otp')

            except IntegrityError as e:
                if 'nin_number' in str(e):
                    form.add_error('nin_number', 'This NIN is already registered')
                else:
                    messages.error(request, 'An error occurred during registration')
                return render(request, "join/join.html", {"form": form})

        messages.error(request, "Please correct the errors below")
        return render(request, "join/join.html", {"form": form})

    return render(request, "join/join.html", {"form": UserRegistrationForm()})

@never_cache
@csrf_protect
@require_http_methods(["GET", "POST"])
def login_view(request):
    """Handle user login with both username and email"""
    if request.user.is_authenticated:
        return redirect('index')

    error = None

    # ✅ Show message if redirected from protected page
    if request.method == "GET" and 'next' in request.GET:
        messages.warning(request, "Only registered members can access the page. Please log in first.")

    if request.method == "POST":
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        user = None

        try:
            # Handle both email and username login
            if '@' in username_or_email:
                user_obj = User.objects.get(email__iexact=username_or_email)
                user = authenticate(
                    request,
                    username=user_obj.username,
                    password=password
                )
            else:
                user = authenticate(
                    request,
                    username=username_or_email,
                    password=password
                )

            if user is not None:
                login(request, user)
                return redirect(request.GET.get('next') or 'index')
            else:
                error = "Invalid credentials. Please try again."

        except User.DoesNotExist:
            error = "Account not found. Please check your credentials."
        except User.MultipleObjectsReturned:
            error = "Multiple accounts found. Please use username instead."
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            error = "An error occurred during login. Please try again."

    return render(request, 'join/login.html', {'error': error})

@login_required
@never_cache
def logout_view(request: HttpRequest) -> HttpResponse:
    """Handle user logout with session cleanup"""
    logout(request)
    request.session.flush()
    messages.success(request, "You have been logged out successfully.")
    return redirect('join:login')


# ======================
# OTP RELATED VIEWS
# ======================
@never_cache
@csrf_protect
@require_http_methods(["GET", "POST"])
def verify_otp(request: HttpRequest) -> HttpResponse:
    """Handle OTP verification for both GET and POST"""
    if not request.session.get('otp_email'):
        return redirect('join:register')

    email = request.session['otp_email']

    if request.method == "GET":
        attempts = cache.get(f'otp_attempts_{email}', 0)
        return render(request, "join/verify_otp.html", {
            'email': email,
            'attempts_remaining': settings.OTP_CONFIG['MAX_ATTEMPTS'] - attempts
        })

    # Handle POST request
    otp = request.POST.get('otp', '')

    if not verify_stored_otp(email, otp):
        attempts = cache.get(f'otp_attempts_{email}', 0)
        remaining = settings.OTP_CONFIG['MAX_ATTEMPTS'] - attempts
        return JsonResponse({
            "valid": False,
            "message": f"Invalid OTP ({remaining} attempts remaining)",
            "attempts_remaining": remaining
        }, status=400)

    # Successful verification
    with transaction.atomic():
        user = get_object_or_404(User, email=email)
        user.is_active = True
        user.save()

        # Cleanup
        cache.delete(f'otp_{email}')
        cache.delete(f'otp_attempts_{email}')
        request.session['otp_verified'] = True
        del request.session['otp_email']

    return JsonResponse({
        "valid": True,
        "redirect": reverse("join:success")
    })

@never_cache
@csrf_protect
@require_POST
def resend_otp(request: HttpRequest) -> JsonResponse:
    """Handle OTP resend requests with rate limiting"""
    email = request.session.get('otp_email')
    if not email:
        return JsonResponse({"status": "error", "message": "Session expired"}, status=400)

    # Rate limiting check
    if cache.get(f'otp_resend_{email}'):
        return JsonResponse({
            "status": "error",
            "message": f"Please wait {settings.OTP_CONFIG['RESEND_COOLDOWN']} seconds before requesting a new code"
        }, status=429)

    # Generate and send new OTP
    otp = generate_secure_otp()
    store_otp(email, otp)

    send_mail(
        "Your New Verification Code",
        f"Your new OTP is: {otp}",
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

    # Set cooldown
    cache.set(f'otp_resend_{email}', True, timeout=settings.OTP_CONFIG['RESEND_COOLDOWN'])
    return JsonResponse({"status": "success", "message": "New OTP sent!"})

#======================
# PROFILE VIEWS
# ======================
@login_required
@never_cache
def dashboard(request: HttpRequest) -> HttpResponse:
    """User dashboard view"""
    return render(request, "join/dashboard.html", {
        'user': request.user,
        'profile': request.user.profile
    })

@login_required
@never_cache
@csrf_protect
@require_http_methods(["GET", "POST"])
def edit_profile(request: HttpRequest) -> HttpResponse:
    """Handle profile updates"""
    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=getattr(request.user, 'profile', None))

    return render(request, "accounts/edit_profile.html", {
        'user_form': user_form,
        'profile_form': profile_form
    })


# ======================
# MISC VIEWS
# ======================
@never_cache
def success(request: HttpRequest) -> HttpResponse:
    """Display success page after verification"""
    if not request.session.get('otp_verified'):
        return redirect('join:register')
    return render(request, "join/success.html")

def csrf_failure(request, reason=""):
    """Custom CSRF failure handler"""
    return JsonResponse({
        "status": "error",
        "message": "CSRF verification failed. Please refresh and try again."
    }, status=403)

#id upload

def capture_id_front(request):
    return render(request, 'join/capture_id_front.html')

def capture_id_back(request):
    return render(request, 'join/capture_id_back.html')
