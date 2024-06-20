# accounts/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Пациент'),
        ('specialist', 'Специалист'),
        ('admin', 'Администратор'),
    )

    username = None  # Удаляем поле username
    email = models.EmailField(_('email address'), unique=True)  # Уникальное поле email
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    first_name = models.CharField(_('Имя'), max_length=30)
    last_name = models.CharField(_('Фамилия'), max_length=30)
    middle_name = models.CharField(_('Отчество'), max_length=30, blank=True, null=True)
    birth_date = models.DateField(_('Дата рождения'), blank=True, null=True)
    phone_number = models.CharField(_('Телефон'), max_length=15, blank=True, null=True)
    country = models.CharField(_('Страна'), max_length=50, blank=True, null=True)
    city = models.CharField(_('Город'), max_length=50, blank=True, null=True)
    specialization = models.CharField(_('Специализация'), max_length=100, blank=True, null=True)
    experience = models.TextField(_('Опыт'), blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    email_notifications = models.BooleanField(_('Email уведомления'), default=True)
    sms_notifications = models.BooleanField(_('SMS уведомления'), default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Измените related_name
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  # Измените related_name
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_query_name='user',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email