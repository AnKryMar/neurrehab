import logging
import random
from .models import Task, Word, WordImage, PersonType, Action


# Настройка логгера
logger = logging.getLogger(__name__)


def get_random_word(category):
    words = Word.objects.filter(category=category)
    if not words.exists():
        raise ValueError(f"Категория '{category}' не найдена или не содержит слов.")
    return random.choice(words).word


def shuffle_word(word):
    word_list = list(word)
    random.shuffle(word_list)
    return ''.join(word_list)


def generate_task(user, task_type, category=None):
    task_data = {}

    if task_type == 'word_scramble':
        if category:
            word = get_random_word(category)
            scrambled_word = shuffle_word(word)
            task_data = {'word': word, 'scrambled_word': scrambled_word}
        else:
            raise ValueError("Категория обязательна для задач типа 'word_scramble'")

    elif task_type == 'image_match':
        if category:
            words = list(Word.objects.filter(category=category).values_list('word', flat=True))
            images = [WordImage.objects.get(word=word).image.url for word in words if
                      WordImage.objects.filter(word=word).exists()]
            task_data = {
                'words': words,
                'images': images
            }
        else:
            raise ValueError("Категория обязательна для задач типа 'image_match'")

    elif task_type == 'action_description':
        actions = list(Action.objects.all())
        persons = list(PersonType.objects.all())
        if category:
            questions = [{'person': random.choice(persons).name, 'action': random.choice(actions).action,
                          'image': random.choice(WordImage.objects.filter(category=category)).image.url} for _ in
                         range(10)]
        else:
            questions = [{'person': random.choice(persons).name, 'action': random.choice(actions).action,
                          'image': random.choice(WordImage.objects.all()).image.url} for _ in range(10)]
        task_data = {'questions': questions}

    elif task_type == 'word_assembly':
        if category:
            word = get_random_word(category)
            parts = [word[:len(word) // 2], word[len(word) // 2:]]
            task_data = {'word': word, 'word_parts': parts}
        else:
            raise ValueError("Категория обязательна для задач типа 'word_assembly'")

    task = Task.objects.create(user=user, task_type=task_type, category=category, data=task_data)
    return {'id': task.id, 'task_type': task_type, 'category': category, 'data': task_data}
