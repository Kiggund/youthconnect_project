"""from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from .models import Message  # Import the Message model
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import re
import dns.resolver
from django.core.mail import send_mail
import random

#Email validation correct syntax
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

#Registration form
def send_message(request):
    if request.method == 'POST':
       # Capture form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_content = request.POST.get('message_content')
        # Save the data to the database
        if name and email and message_content:  # Ensure all fields are filled
            new_message = Message(name=name, email=email, message=message_content)
            new_message.save()  # Save to the database
            return HttpResponse('Message sent successfully!')
        else:
            return HttpResponse('Missing required fields.')
    else:
        return HttpResponse('Invalid request method.')

    #Allows correctly formatted emails
    if not is_valid_email(email):
        return JsonResponse({"success": False, "message": "Invalid email address!"}, status=400)

# Return JSON response
        return JsonResponse({"success": True, "message": "Message sent successfully!"})
        return JsonResponse({"success": False, "message": "Invalid request method."})
"""

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from join.forms import MemberForm  # Assuming join app has the form
import dns.resolver

# Disposable email domains list
DISPOSABLE_DOMAINS = [
    'mailinator.com', 'tempmail.com', 'yopmail.com', 'trashmail.com'
]

# Function to validate email domains
def validate_email_domain(email):
    #pass all domains during testing
    pass
    """Validate email domain for existence and disposability
    domain = email.split('@')[-1]  # Extract domain from email
    if domain in DISPOSABLE_DOMAINS:
        raise ValidationError("Temporary email providers are not allowed.")
    
    try:
        dns.resolver.resolve(domain, 'MX')  # Check for MX records
    except dns.resolver.NoAnswer:
        raise ValidationError("Email domain exists but can't receive emails.")
    except dns.resolver.NXDOMAIN:
        raise ValidationError("Email domain does not exist.")
    except Exception as e:
        raise ValidationError(f"Error during domain validation: {str(e)}")
"""

# Function for registration
def register_user(request):
    """Handle user registration with email validation"""
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")  # Extract email from form
            try:
                validate_email_domain(email)  # Validate the email domain
                form.save()  # Save the user data
                return redirect('join:success')  # Redirect to success page
            except ValidationError as e:
                # Pass the error to the registration template
                return render(request, 'join/register.html', {"form": form, "error": str(e)})
        else:
            # Handle form validation errors
            return render(request, 'join/register.html', {"form": form, "form_errors": form.errors})
    else:
        form = MemberForm()  # Blank form for GET requests
    return render(request, 'join/register.html', {"form": form})


# Function for handling user messages
def send_message(request):
    """Handle user messages submitted via the contact form"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_content = request.POST.get('message')

        if name and email and message_content:
            try:
                validate_email_domain(email)  # Validate email domain
                new_message = Message(name=name, email=email, content=message_content)
                new_message.save()  # Save message to database
                return HttpResponse('Message sent successfully')
            except ValidationError as e:
                return HttpResponse(f"Error: {str(e)}")
        return HttpResponse("All fields are required!")
    else:
        return render(request, 'join/contact.html')  # Render contact form template


# Success page view
def success(request):
    """Display a success message after successful operations"""
    return render(request, 'join/success.html', {"message": "Operation completed successfully!"})


# Index page view
def index(request):
    """Render the homepage"""
    return render(request, 'join/index.html')


# Contact page view
def contact(request):
    """Render the contact page"""
    return render(request, 'join/contact.html')
