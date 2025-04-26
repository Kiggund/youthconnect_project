import requests

def get_access_token(api_key):
    url = "https://sandbox.momodeveloper.mtn.com/collection/token/"
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("access_token")
    return None


def initiate_payment(api_key, token, amount, phone_number):
    url = "https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay"
    headers = {
        "Authorization": f"Bearer {token}",
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
        "X-Reference-Id": "UNIQUE_TRANSACTION_ID",  # Generate a unique transaction ID
    }
    payload = {
        "amount": amount,
        "currency": "UGX",
        "payer": {
            "partyIdType": "MSISDN",
            "partyId": phone_number,
        },
        "payerMessage": "Subscription Payment",
        "payeeNote": "Thank you for subscribing!",
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
