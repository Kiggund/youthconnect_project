from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache
from django.core.cache import cache
from django.db import transaction
from django.conf import settings
import logging
from .models import Member
from .forms import MemberForm, OTPVerificationForm

logger = logging.getLogger(__name__)

### **INDEX VIEW**
@never_cache
def index(request):
    """Landing page that shows registration form"""
    logger.debug("🟢 Index view: Rendering registration form")
    return render(request, 'join/register.html', {
        'form': MemberForm(for_registration=True),
        'hide_registration_link': True
    })


### **REGISTRATION VIEW**
@never_cache
@require_http_methods(["GET", "POST"])
def register(request):
    """Handles user registration and OTP sending"""
    logger.debug(f"🟠 Register view: Received {request.method} request")

    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, for_registration=True)
        logger.debug(f"📝 Form validation - Valid: {form.is_valid()}, Errors: {form.errors}")

        if not form.is_valid():
            logger.warning("⚠️ Registration failed due to invalid form input.")
            return JsonResponse({'status': 'error', 'errors': form.errors.get_json_data()}, status=400)

        try:
            with transaction.atomic():
                logger.debug("🔄 Transaction started for member registration")

                member = form.save(commit=False)
                member.time_joined = timezone.now()
                otp = member.generate_otp()
                member.save()
                logger.info(f"✅ New member registered: {member.email}")

                # Send OTP email
                try:
                    logger.debug(f"📨 Attempting to send OTP to {member.email}")
                    send_mail(
                        subject='Your Verification Code',
                        message=f'Your OTP is: {otp}\nValid for 5 minutes',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[member.email],
                        fail_silently=False
                    )
                    logger.info(f"✉️ OTP email sent successfully to {member.email}")
                except Exception as email_error:
                    logger.error(f"❌ Failed to send OTP email: {email_error}", exc_info=True)

                # Redirect after successful registration
                redirect_url = reverse('join:verify_otp', kwargs={'email': member.email})
                logger.debug(f"🔗 Redirecting to OTP verification: {redirect_url}")
                response = HttpResponseRedirect(redirect_url)
                response['Cache-Control'] = 'no-store, no-cache, must-revalidate'
                return response

        except Exception as reg_error:
            logger.error(f"❌ Unexpected registration error: {reg_error}", exc_info=True)
            return JsonResponse({'status': 'error', 'message': 'Registration failed. Please try again.'}, status=500)

    logger.debug("🔵 Register view: Handling GET request")
    return render(request, 'join/register.html', {
        'form': MemberForm(for_registration=True),
        'hide_registration_link': True
    })


### **OTP VERIFICATION VIEW**
@never_cache
@require_http_methods(["GET", "POST"])
def verify_otp(request, email):
    """Handles OTP verification with strict redirect behavior"""
    logger.debug(f"🟣 Verify OTP view: Received request for {email}")

    ip = request.META.get('REMOTE_ADDR')
    cache_key = f"otp_attempts_{ip}"
    attempts = cache.get(cache_key, 0)

    if attempts >= 5:
        logger.warning(f"🚫 Too many OTP attempts from IP: {ip}")
        return JsonResponse({'status': 'error', 'message': 'Too many attempts. Please wait 15 minutes.'}, status=429)

    try:
        member = Member.objects.get(email=email)
        logger.debug(f"👤 Member found for OTP verification: {email}")
    except Member.DoesNotExist:
        logger.error(f"❌ Member with email {email} not found!")
        return JsonResponse({'status': 'error', 'message': 'Invalid email'}, status=404)

    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        logger.debug(f"🔢 OTP form validation - Valid: {form.is_valid()}, Errors: {form.errors}")

        if not form.is_valid():
            logger.warning(f"⚠️ Invalid OTP input for {email}")
            return JsonResponse({'status': 'error', 'errors': form.errors.get_json_data()}, status=400)

        cache.set(cache_key, attempts + 1, timeout=900)

        if member.is_account_locked():
            logger.warning(f"🚫 Account locked for {email}")
            return JsonResponse({'status': 'error', 'message': 'Account locked. Please try again later.'}, status=403)

        if member.is_otp_expired():
            logger.warning(f"⌛ OTP expired for {email}")
            return JsonResponse({'status': 'error', 'message': 'OTP expired. Please request a new code.'}, status=400)

        if member.otp == form.cleaned_data['otp']:
            member.is_verified = True
            member.reset_otp_security()
            member.save()
            logger.info(f"✅ OTP successfully verified for {email}")
            #return JsonResponse({'status': 'success', 'redirect': reverse('join:success')})
            return HttpResponseRedirect(reverse('join:success'))

        member.increment_otp_attempts()
        remaining = 3 - member.otp_attempts
        logger.warning(f"🚫 Invalid OTP attempt for {email}, {remaining} attempts left")
        return JsonResponse({'status': 'error', 'message': f'Invalid OTP. {remaining} attempts remaining'}, status=400)

    return render(request, 'join/verify_otp.html', {'form': OTPVerificationForm(), 'email': email, 'member': member})


### **RESEND OTP VIEW**
@never_cache
def resend_otp(request, email):
    """Handles OTP resend requests"""
    logger.debug(f"🔄 Resend OTP request received for {email}")

    try:
        member = Member.objects.get(email=email)

        if member.is_account_locked():
            logger.warning(f"🚫 Resend OTP blocked for locked account: {email}")
            return JsonResponse({'status': 'error', 'message': 'Account locked. Try again later.'}, status=403)

        otp = member.generate_otp()
        member.save()
        logger.debug(f"🆕 New OTP generated: {otp}")

        try:
            send_mail(
                subject='Your New Verification Code',
                message=f'Your new OTP is: {otp}\nValid for 5 minutes',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[member.email],
                fail_silently=False
            )
            logger.info(f"📨 New OTP sent to {email}")
        except Exception as email_error:
            logger.error(f"❌ Failed to send OTP email: {email_error}", exc_info=True)

        return JsonResponse({'status': 'success', 'message': 'New OTP sent successfully'})

    except Member.DoesNotExist:
        logger.error(f"❌ Resend OTP failed: Member {email} not found")
        return JsonResponse({'status': 'error', 'message': 'Member not found'}, status=404)


### **SUCCESS PAGE**
@never_cache
def success(request):
    """Success page after verification"""
    logger.debug("✅ Success page accessed")
    return render(request, 'join/success.html')
