from django.apps import AppConfig

class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Để tránh cảnh báo của Django
    name = 'store'

    def ready(self):
        import store.signals  # Import signals khi app được load
