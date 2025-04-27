"""
Contact Application Models
=========================

This module defines the database models for handling contact form submissions.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

class ContactMessage(models.Model):
    """
    Represents a message submitted through the contact form.

    Attributes:
        name (CharField): The sender's full name. Max length 255 characters.
        email (EmailField): The sender's email address. Validated as proper email format.
        content (TextField): The message body/content. No length limit.
        timestamp (DateTimeField): Automatic timestamp of when the message was received.

    Meta:
        ordering: Messages are ordered newest first by default.
        verbose_name: Human-readable singular name for admin interface.
        verbose_name_plural: Human-readable plural name for admin interface.

    Methods:
        __str__: Returns a string representation combining name and timestamp.
    """

    name = models.CharField(
        max_length=255,
        verbose_name=_("Sender's Name"),
        help_text=_("Full name of the person sending the message")
    )

    email = models.EmailField(
        verbose_name=_("Email Address"),
        help_text=_("Valid email address for reply correspondence")
    )

    content = models.TextField(
        verbose_name=_("Message"),
        help_text=_("The main body of the message")
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Received Timestamp"),
        help_text=_("When the message was submitted")
    )

    class Meta:
        ordering = ['-timestamp']
        verbose_name = _("Contact Message")
        verbose_name_plural = _("Contact Messages")

    def __str__(self):
        """String representation for admin and debugging."""
        return f"Contact message from {self.name} at {self.timestamp}"
