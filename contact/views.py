from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import ContactMessage  # Import your ContactMessage model
import logging

# Set up logging
logger = logging.getLogger(__name__)

@ensure_csrf_cookie
def contact_page(request):
    """
    Render the contact form page.
    This view also ensures a CSRF token is included in the page.
    """
    return render(request, 'contact/form.html')  # Replace with your actual form template path


@require_POST
@ensure_csrf_cookie
def send_message(request):
    """
    Handle contact form submissions.
    Supports both AJAX and normal POST requests.
    """
    # Check if the request is AJAX
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    # Extract form fields
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    message = request.POST.get('message', '').strip()

    # Validate fields
    if not name:
        error_message = "Name field cannot be empty."
        return _handle_error_response(is_ajax, error_message, request)

    if not email:
        error_message = "Email field cannot be empty."
        return _handle_error_response(is_ajax, error_message, request)

    if not message:
        error_message = "Message field cannot be empty."
        return _handle_error_response(is_ajax, error_message, request)

    try:
        # Save the message to the database
        contact_message = ContactMessage.objects.create(
            name=name,
            email=email.lower(),
            content=message
        )
        logger.info(f"Message successfully saved with ID: {contact_message.id}")

        success_message = "Your message has been received! We will respond shortly."
        if is_ajax:
            return JsonResponse({'status': 'success', 'message': success_message, 'id': contact_message.id})
        else:
            return render(request, 'contact/success.html', {'message': success_message})

    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        error_message = "Failed to process your message. Please try again."
        return _handle_error_response(is_ajax, error_message, request)


def _handle_error_response(is_ajax, error_message, request):
    """
    Helper function to handle errors and return the appropriate response.
    """
    if is_ajax:
        return JsonResponse({'status': 'error', 'message': error_message}, status=400)
    else:
        return render(request, 'contact/form.html', {'error_message': error_message})
