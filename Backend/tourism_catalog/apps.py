from django.apps import AppConfig


class TourismCatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tourism_catalog'
    verbose_name = 'Tourism Catalog'
    
    def ready(self):
        """Initialize the bounded context when Django starts"""
        # Import event handlers to register them
        try:
            from . import event_handlers
        except ImportError:
            pass
