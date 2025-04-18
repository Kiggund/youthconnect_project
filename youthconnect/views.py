from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from .models import Message  # Import the Message model
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
#@csrf_exempt  # Remove this in production
#def send_message(request):
 #   if request.method == 'POST':
  #      print("Received POST data:", request.POST)  # Debugging statement
   #     name = request.POST.get('name')
    #    email = request.POST.get('email')
     #   message_content = request.POST.get('message_content')

        # Validate input
      #  if not name or not email or not message_content:
       #     messages.error(request, 'All fields are required!')
        #    return JsonResponse({"success": False, "message": "All fields are required!"}, status=400)

        # Save message to the database
      #  Message.objects.create(sender=name, email=email, content=message_content)

        # Success response
       # messages.success(request, 'Message sent successfully.')
        #return JsonResponse({"success": True, "message": "Message sent successfully!"})

    #return render(request, 'contact.html')
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
        #return HttpResponse('Invalid request method.')

# Return JSON response
        return JsonResponse({"success": True, "message": "Message sent successfully!"})
        return JsonResponse({"success": False, "message": "Invalid request method."})
