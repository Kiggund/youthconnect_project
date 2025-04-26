from django.shortcuts import render
from django.conf import settings  # Add this line
from paypal.standard.forms import PayPalPaymentsForm

def subscribe(request):
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "10.00",  # Subscription price
        "item_name": "Premium Membership",
        "currency_code": "USD",
        "return_url": "http://yourdomain.com/payment-success/",
        "cancel_url": "http://yourdomain.com/payment-cancelled/",
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, "payments/payments.html", {"form": form})
# Create your views here.
