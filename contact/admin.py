"""
Admin Interface Configuration for Contact Messages
================================================

Customizes how ContactMessage models appear in Django admin.
"""

from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactContactMessageAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for ContactMessage model.

    Features:
    - List display with key fields
    - Search capability
    - Date-based filtering
    - Read-only fields for auditing
    """

    list_display = ('name', 'email', 'short_content', 'timestamp')
    search_fields = ('name', 'email', 'content')
    list_filter = ('timestamp',)
    date_hierarchy = 'timestamp'
    readonly_fields = ('timestamp',)

    fieldsets = (
        (None, {
            'fields': ('name', 'email')
        }),
        ('Message Content', {
            'fields': ('content',)
        }),
        ('Metadata', {
            'fields': ('timestamp',),
            'classes': ('collapse',)
        })
    )

    def short_content(self, obj):
        """Display abbreviated content in list view."""
        return f"{obj.content[:50]}..." if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Content Preview'
