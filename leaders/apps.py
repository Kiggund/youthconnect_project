from django.apps import AppConfig


class LeadersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'leaders'
        
    def ready(self):
        import leaders.signals #connect signals
