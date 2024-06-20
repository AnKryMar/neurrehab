# Generated by Django 5.0.6 on 2024-06-08 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_remove_wordimage_image_url_wordimage_image_data_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wordimage',
            name='image_data',
        ),
        migrations.AddField(
            model_name='wordimage',
            name='image',
            field=models.ImageField(default='generated_images/image.png', upload_to='generated_images/'),
        ),
    ]