from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = '/data/data/com.termux/files/usr/bin/tesseract'

def extract_text(image_field):
    try:
        image = Image.open(image_field)
        return pytesseract.image_to_string(image)
    except Exception as e:
        return f"[OCR Error] {e}"
