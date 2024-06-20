# views.py
import random
from random import shuffle, sample
from django.shortcuts import render, redirect
from django.views import View
from .models import Attempt, Task, MotivationalPhrase, Word, WordImage, ActionImageTask
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponse
from .task_generator import generate_task
import json
import logging
from django.db.models import Sum, Count, Q
from datetime import datetime, timedelta
from django.utils import timezone

categories = [
    ('fruits', 'Фрукты'),
    ('vegetables', 'Овощи'),
    ('vehicles', 'Транспортные средства'),
    ('appliances', 'Бытовые приборы'),
    ('animals', 'Животные'),
    ('plants', 'Растения'),
]

task_types = ['word_scramble', 'image_match', 'action_description', 'word_assembly']

logger = logging.getLogger(__name__)

def auto_task(request):
    return HttpResponse("Auto Task Response")

def image_match_auto(request):
    return HttpResponse("Image Match Auto Response")

def get_words_without_images(request):
    category = request.GET.get('category')
    words_without_images = Word.objects.filter(category=category).exclude(word__in=WordImage.objects.values_list('word', flat=True))
    words = [word.word for word in words_without_images]
    return JsonResponse({'words': words})

def get_daily_score(user, task_type, category):
    today = timezone.now().replace(hour=0, minute=0, second=0)
    score = Attempt.objects.filter(
        user=user,
        task__task_type=task_type,
        task__category=category,
        completed_at__gte=today
    ).aggregate(Sum('score'))['score__sum'] or 0  # Здесь важно проверить
    return score

@method_decorator(login_required, name='dispatch')
class TaskListView(View):
    def get(self, request):
        tasks_by_type = {tt: [] for tt in task_types}
        for cat, cat_name in categories:
            for tt in task_types:
                if tt != 'action_description':
                    tasks_by_type[tt].append({'category': cat, 'category_name': cat_name, 'task_type': tt})

        # Отдельно добавляем задачу без категорий для action_description
        tasks_by_type['action_description'].append({'category': None, 'category_name': None, 'task_type': 'action_description'})

        return render(request, 'tasks/task_list.html', {'tasks_by_type': tasks_by_type})

@method_decorator(login_required, name='dispatch')
class TaskDetailView(View):
    def get(self, request, category, task_type):
        today = timezone.now().replace(hour=0, minute=0, second=0)
        correct_attempts_today = Attempt.objects.filter(
            user=request.user,
            task__task_type=task_type,
            completed_at__gte=today,
            correct=True
        )
        if task_type != 'action_description':
            correct_attempts_today = correct_attempts_today.filter(task__category=category)

        correct_attempts_count = correct_attempts_today.count()

        if correct_attempts_count >= 10:
            return redirect('tasks:task_list')

        # Для action_description не используем категории
        if task_type != 'action_description':
            task = generate_task(request.user, task_type, category)
        else:
            task = generate_task(request.user, task_type, None)

        request.session['task_id'] = task['id']
        request.session['image_index'] = 0  # Инициализация текущего индекса изображения
        context = {
            'task': task,
            'daily_score': get_daily_score(request.user, task_type, category if task_type != 'action_description' else None)
        }

        if task['task_type'] == 'word_scramble':
            scrambled_word = task['data']['scrambled_word']
            context['scrambled_word'] = scrambled_word

        elif task['task_type'] == 'image_match':
            words = task['data']['words']
            combined_list = []
            for word in words:
                word_image = WordImage.objects.filter(word=word).first()
                if word_image:
                    image_url = word_image.image.url
                    choices = sample(words, 4) + [word]
                    shuffle(choices)
                    combined_list.append((image_url, choices, word))
                else:
                    logger.error(f"No image found for word '{word}'")
            context['combined_list'] = combined_list
            context['category_name'] = dict(categories).get(category, category).lower() if task_type != 'action_description' else None

        elif task['task_type'] == 'action_description':
            questions = task['data']['questions']
            context['questions'] = questions

        return render(request, f'tasks/task_detail_{task["task_type"]}.html', context)

    def post(self, request, category, task_type):
        try:
            task_id = request.session.get('task_id')
            if not task_id:
                logger.error('Task ID not found in session')
                return JsonResponse({'error': 'Task ID not found in session'}, status=400)

            data = json.loads(request.body)
            user_answer = data.get('answer')
            current_question_index = data.get('current_question_index', 0)

            if user_answer is None:
                logger.error('Answer is missing')
                return JsonResponse({'error': 'Answer is missing'}, status=400)

            task = Task.objects.get(id=task_id)
            correct_answer = task.data['questions'][current_question_index]['action']
            correct = user_answer == correct_answer

            Attempt.objects.create(user=request.user, task=task, score=1 if correct else 0, correct=correct)

            motivational_phrase = None
            if correct:
                phrases = MotivationalPhrase.objects.all()
                if phrases:
                    motivational_phrase = random.choice(phrases).phrase

            next_question_index = current_question_index + 1
            if next_question_index < len(task.data['questions']):
                next_question = task.data['questions'][next_question_index]
                next_image_data = {
                    'image_url': next_question['image'],
                    'person': next_question['person']
                }
            else:
                next_image_data = None

            request.session['question_index'] = next_question_index

            response_data = {
                'correct': correct,
                'feedback': "Правильно!" if correct else "Неправильно.",
                'motivational_phrase': motivational_phrase,
                'daily_score': get_daily_score(request.user, task_type,
                                               category if task_type != 'action_description' else None),
                'next_image_data': next_image_data
            }
            return JsonResponse(response_data)

        except Task.DoesNotExist:
            logger.error(f"Task with ID {task_id} does not exist.")
            return JsonResponse({'error': 'Task does not exist'}, status=400)

        except Exception as e:
            logger.error(f"Error processing task submission: {e}")
            return JsonResponse({'error': 'An error occurred'}, status=500)

@method_decorator(login_required, name='dispatch')
class ProfileStatisticsView(View):
    def get(self, request):
        game_type = request.GET.get('game_type')
        category = request.GET.get('category')
        date_filter = request.GET.get('date_filter')
        date_specific = request.GET.get('date_specific')
        user_attempts = Attempt.objects.filter(user=request.user)

        if game_type:
            user_attempts = user_attempts.filter(task__task_type=game_type)

        if category:
            user_attempts = user_attempts.filter(task__category=category)

        if date_filter == 'yesterday':
            start_date = timezone.now() - timedelta(days=1)
            end_date = timezone.now()
        elif date_filter == 'today':
            start_date = timezone.now().replace(hour=0, minute=0, second=0)
            end_date = timezone.now()
        elif date_specific:
            start_date = timezone.make_aware(datetime.strptime(date_specific, '%Y-%m-%d'))
            end_date = start_date + timedelta(days=1)
        else:
            start_date = None
            end_date = None

        if start_date and end_date:
            user_attempts = user_attempts.filter(completed_at__range=(start_date, end_date))

        # Группировка по дате, типу игры и категории
        statistics = user_attempts.values('task__task_type', 'task__category', 'completed_at__date').annotate(
            total_attempts=Count('id'),
            correct_attempts=Count('id', filter=Q(correct=True)),
            score=Sum('score')
        ).order_by('completed_at__date')

        context = {
            'statistics': statistics,
            'game_type': game_type,
            'category': category,
            'date_filter': date_filter,
            'date_specific': date_specific,
            'game_types': set(user_attempts.values_list('task__task_type', flat=True).distinct()),
            'categories': set(user_attempts.values_list('task__category', flat=True).distinct()),
        }

        return render(request, 'tasks/profile_statistics.html', context)
