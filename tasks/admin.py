# admin.py
from django.contrib import admin
from .models import Task, Attempt, Word, WordImage, MotivationalPhrase, PersonType, Action, ActionImageTask
from .forms import WordImageForm

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_type', 'category')
    list_filter = ('task_type', 'category')

@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'task', 'score', 'completed_at')
    list_filter = ('task',)

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('category', 'word')
    list_filter = ('category',)

@admin.register(WordImage)
class WordImageAdmin(admin.ModelAdmin):
    form = WordImageForm
    list_display = ('word', 'image')

@admin.register(MotivationalPhrase)
class MotivationalPhraseAdmin(admin.ModelAdmin):
    list_display = ('phrase',)


@admin.register(PersonType)
class PersonTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('action',)

@admin.register(ActionImageTask)
class ActionImageTaskAdmin(admin.ModelAdmin):
    list_display = ('person_type', 'action', 'image')