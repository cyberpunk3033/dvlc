from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# TODO: Доделать хранение пароля для email с шифрованием
'''
from encrypted_model_fields.fields import EncryptedCharField

class EncryptedFieldModel(models.Model):
    encrypted_char_field = EncryptedCharField()
'''

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError(_('Email обязателен для заполнения!'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Суперпользователь должен иметь  is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

# Создаем объект пользователя с помощью метода model,
# который возвращает класс модели, связанный с менеджером CustomUserManager

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(('email address'), unique=True)
    fio=models.CharField(verbose_name='ФИО',max_length=50, blank=True, null=True,default=None)
    user_email_password = models.CharField(verbose_name='Пароль email для отправки сообщений',
                                           max_length=50, help_text='Введите пароль от вашего емейла',blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Устанавливаем объект CustomUserManager в качестве objects,
    # то есть менеджера, который управляет операциями с пользователями
    objects = CustomUserManager()

    def __str__(self):
        return self.email