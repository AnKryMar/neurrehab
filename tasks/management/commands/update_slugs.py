# tasks/management/commands/update_slugs.py
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from tasks.models import Task

class Command(BaseCommand):
    help = 'Update slug fields for existing tasks'

    def handle(self, *args, **kwargs):
        tasks = Task.objects.all()
        for task in tasks:
            task.category_slug = slugify(task.category)
            task.task_type_slug = slugify(task.task_type)
            task.save()
        self.stdout.write(self.style.SUCCESS('Successfully updated slugs for all tasks'))
