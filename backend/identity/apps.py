from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler

class IdentityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'identity'

    def ready(self):
        from .jobs import github_task
        scheduler = BackgroundScheduler()
        scheduler.add_job(github_task, 'interval', minutes=1)
        scheduler.start()