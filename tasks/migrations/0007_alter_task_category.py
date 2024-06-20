# Generated by Django 5.0.6 on 2024-06-13 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_attempt_action_image_task_alter_attempt_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='category',
            field=models.CharField(blank=True, choices=[('fruits', 'Фрукты'), ('vegetables', 'Овощи'), ('vehicles', 'Транспортные средства'), ('appliances', 'Бытовые приборы'), ('animals', 'Животные'), ('plants', 'Растения')], max_length=20, null=True),
        ),
    ]
