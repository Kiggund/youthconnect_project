import re
from difflib import SequenceMatcher

def match_score(field_value, text, threshold=0.7):
    ratio = SequenceMatcher(None, field_value.lower(), text.lower()).ratio()
    return ratio >= threshold

def validate_ocr_fields(nin, full_name, dob, gender, place_of_birth, ocr_text):
    result = {'NIN': False, 'Name': False, 'DOB': False, 'Gender': False, 'POB': False}

    text_cleaned = ocr_text.replace(" ", "").lower()

    # NIN exact
    result['NIN'] = nin.lower() in text_cleaned

    # Name fuzzy
    result['Name'] = match_score(full_name, ocr_text)

    # DOB as YYYY-MM-DD or DD/MM/YYYY
    result['DOB'] = (
        dob.strftime("%Y-%m-%d") in ocr_text or
        dob.strftime("%d/%m/%Y") in ocr_text
    )

    # Gender loose match
    result['Gender'] = gender.lower() in ocr_text.lower()

    # Place of Birth fuzzy
    result['POB'] = match_score(place_of_birth, ocr_text)

    return result
