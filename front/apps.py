from django.apps import AppConfig

from front.tasks import create_tasks


class FrontConfig(AppConfig):
    name = 'front'

    def ready(self):
        create_tasks()
