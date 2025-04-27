from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from .models import ContactMessage  # Ensure your model import is correct
import logging

logger = logging.getLogger(__name__)

@ensure_csrf_cookie
def contact_page(request):
    """
    Render the contact form page with a CSRF token.
    """
    return render(request, 'contact/form.html')  # Ensure the template path matches your setup

@require_POST
def send_message(request):
    """
    Process contact form submissions (AJAX or normal POST).
    """
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    required_fields = ['name', 'email', 'message']
    missing_fields = [field for field in required_fields if field not in request.POST]

    if missing_fields:
        message = f"Missing required fields: {', '.join(missing_fields)}"
        if is_ajax:
            return JsonResponse({'status': 'error', 'message': message}, status=400)
        else:
            return render(request, 'contact/form.html', {'error_message': message})

    try:
        message = ContactMessage.objects.create(
            name=request.POST['name'].strip(),
            email=request.POST['email'].strip().lower(),
            content=request.POST['message'].strip()
        )
        logger.info(f"Message successfully saved with ID: {message.id}")

        success_message = "Your message has been received! We will respond shortly."
        if is_ajax:
            return JsonResponse({'status': 'success', 'message': success_message, 'id': message.id})
        else:
            return render(request, 'contact/success.html', {'message': success_message})

    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        error_message = "Failed to process your message. Please try again."
        if is_ajax:
            return JsonResponse({'status': 'error', 'message': error_message}, status=500)
        else:
            return render(request, 'contact/form.html', {'error_message': error_message})
