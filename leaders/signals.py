from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image, ImageEnhance
from .models import Leader

@receiver(post_save, sender=Leader)
def process_leader_image(sender, instance, **kwargs):
    if instance.image:
        image_path = instance.image.path  # Get the file path of the uploaded image
        img = Image.open(image_path)

        # Enhance sharpness
        sharpness_enhancer = ImageEnhance.Sharpness(img)
        img = sharpness_enhancer.enhance(2.0)

        # Save the enhanced image back
        img.save(image_path)
