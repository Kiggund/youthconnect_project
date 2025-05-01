from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from django.shortcuts import redirect
import logging
from .models import Member
from .forms import MemberForm, OTPVerificationForm
from django.views.decorators.csrf import csrf_exempt
import json

logger = logging.getLogger(__name__)

# Add this new view function
@csrf_exempt
@require_POST
def api_verify_otp(request):
    """API endpoint for OTP verification"""
    try:
        data = json.loads(request.body)
        email = data.get('email')
        otp = data.get('otp')
        
        if not email or not otp:
            return JsonResponse({'valid': False, 'message': 'Missing parameters'}, status=400)
            
        member = get_object_or_404(Member, email=email)
        
        if member.is_account_locked():
            return JsonResponse({
                'valid': False,
                'message': f'Account locked. Try again in {(member.lock_until - timezone.now()).seconds // 60} minutes.'
            }, status=403)
            
        if member.is_otp_expired():
            return JsonResponse({
                'valid': False,
                'message': 'OTP expired. Request new code.'
            }, status=400)
            
        if member.otp == otp:
            member.is_verified = True
            member.reset_otp_security()
            member.save()
            return JsonResponse({
                'valid': True,
                'message': 'OTP verified successfully!',
                'redirect_url': reverse('join:success')
            })
        else:
            member.increment_otp_attempts()
            remaining = max(0, 3 - member.otp_attempts)
            return JsonResponse({
                'valid': False,
                'message': f'Invalid OTP. {remaining} attempts left.'
            }, status=400)
            
    except Exception as e:
        logger.error(f"API OTP verification failed: {e}")
        return JsonResponse({
            'valid': False,
            'message': 'Server error during verification'
        }, status=500)

# 1. Index View (Class-Based)
"""class IndexView(View):
    #Landing page view
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        register_url = reverse('join:register')
        return render(request, 'join/register.html', {'register_url': register_url})"""

def redirect_to_register(request):
    return redirect('join:register')

# 2. Registration View
@never_cache
@require_http_methods(["GET", "POST"])
def register(request):
    """Handle user registration"""
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, for_registration=True)
        if not form.is_valid():
            return render(request, 'join/register.html', {'form': form})
        
        try:
            with transaction.atomic():
                member = form.save(commit=False)
                member.time_joined = timezone.now()
                otp = member.generate_otp()
                member.save()
                
                send_mail(
                    'Your Verification Code',
                    f'Your OTP: {otp}\nValid for 5 minutes',
                    settings.DEFAULT_FROM_EMAIL,
                    [member.email],
                    fail_silently=False
                )
                return redirect('join:verify_otp', email=member.email)
        except Exception as e:
            logger.error(f"Registration failed: {e}")
            messages.error(request, 'Registration failed. Please try again.')
            return render(request, 'join/register.html', {'form': form})

    return render(request, 'join/register.html', {
        'form': MemberForm(for_registration=True)
    })

# 3. OTP Verification View
@never_cache
@require_http_methods(["GET", "POST"])
def verify_otp(request, email):
    """Handle OTP verification"""
    member = get_object_or_404(Member, email=email)
    
    if member.is_account_locked():
        lock_time = (member.lock_until - timezone.now()).seconds // 60
        messages.error(request, f"Account locked. Try again in {lock_time} minutes.")
    elif request.method == 'POST':
        otp = request.POST.get('otp', '')
        
        if len(otp) != 6 or not otp.isdigit():
            messages.error(request, "Invalid OTP format")
        elif member.is_otp_expired():
            messages.error(request, "OTP expired. Request new code.")
        elif member.otp == otp:
            member.is_verified = True
            member.reset_otp_security()
            member.save()
            return redirect('join:success')
        else:
            member.increment_otp_attempts()
            remaining = max(0, 3 - member.otp_attempts)
            messages.error(request, f"Invalid OTP. {remaining} attempts left.")

    return render(request, 'join/verify_otp.html', {
        'email': email,
        'member': member
    })

# 4. Resend OTP View
@never_cache
@require_POST
def resend_otp(request, email):
    """Handle OTP resend requests"""
    try:
        member = get_object_or_404(Member, email=email)
        
        if member.is_account_locked():
            return JsonResponse({
                'status': 'error',
                'message': 'Account locked. Try again later.'
            }, status=400)
        
        otp = member.generate_otp()
        member.save()
        
        send_mail(
            'Your New Verification Code',
            f'New OTP: {otp}\nValid for 5 minutes',
            settings.DEFAULT_FROM_EMAIL,
            [member.email],
            fail_silently=False
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'New OTP sent! Check your email.'
        })

    except ValueError as e:  # Cooldown error
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=429)
    except Exception as e:
        logger.error(f"Resend failed: {e}")
        return JsonResponse({
            'status': 'error',
            'message': 'Failed to resend OTP'
        }, status=500)

# 5. Success View
@never_cache
def success(request):
    """Verification success page"""
    return render(request, 'join/success.html')
