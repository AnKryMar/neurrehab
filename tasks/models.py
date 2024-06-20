# models.py
from django.db import models
from accounts.models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.conf import settings


class Task(models.Model):
    CATEGORY_CHOICES = [
        ('fruits', _('Фрукты')),
        ('vegetables', _('Овощи')),
        ('vehicles', _('Транспортные средства')),
        ('appliances', _('Бытовые приборы')),
        ('animals', _('Животные')),
        ('plants', _('Растения')),
    ]

    TASK_TYPES = [
        ('word_scramble', _('Перемешанные буквы')),
        ('image_match', _('Сопоставление изображения и слова')),
        ('action_description', _('Описание действия')),
        ('word_assembly', _('Составление слова из обрывков')),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, null=True, blank=True)  # Сделано необязательным
    category_slug = models.SlugField(max_length=20, blank=True)
    task_type = models.CharField(max_length=20, choices=TASK_TYPES)
    task_type_slug = models.SlugField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField(default=dict)

    def save(self, *args, **kwargs):
        if self.category and not self.category_slug:
            self.category_slug = slugify(self.category)
        if not self.task_type_slug:
            self.task_type_slug = slugify(self.task_type)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_category_display() if self.category else 'No Category'} - {self.get_task_type_display()}"


class PersonType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Action(models.Model):
    action = models.CharField(max_length=50)

    def __str__(self):
        return self.action



class ActionImageTask(models.Model):
    image = models.ImageField(upload_to='action_image_tasks/')
    person_type = models.ForeignKey(PersonType, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.person_type} - {self.action}'



class Attempt(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, null=True, blank=True, on_delete=models.CASCADE)  # Оставляем для старых задач
    action_image_task = models.ForeignKey(ActionImageTask, null=True, blank=True, on_delete=models.CASCADE)  # Добавляем для новых задач
    score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)
    correct = models.BooleanField(default=False)

    def __str__(self):
        if self.task:
            return f"{self.user.email} - {self.task.category}"
        elif self.action_image_task:
            return f"{self.user.email} - {self.action_image_task}"
        return f"{self.user.email} - No task assigned"


class Word(models.Model):
    CATEGORY_CHOICES = [
        ('fruits', _('Фрукты')),
        ('vegetables', _('Овощи')),
        ('vehicles', _('Транспортные средства')),
        ('appliances', _('Бытовые приборы')),
        ('animals', _('Животные')),
        ('plants', _('Растения')),
    ]

    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    word = models.CharField(max_length=100)

    def __str__(self):
        return self.word

class WordImage(models.Model):
    word = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='generated_images/', default='generated_images/image.png')

    def __str__(self):
        return self.word

class MotivationalPhrase(models.Model):
    phrase = models.TextField()

    def __str__(self):
        return self.phrase


