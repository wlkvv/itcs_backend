from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from django.utils import timezone


class Service(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )

    name = models.CharField(verbose_name="Название", max_length=255)
    description = models.TextField(verbose_name="Описание", blank=True)
    price = models.IntegerField(verbose_name="Цена", default=1000)
    time = models.IntegerField(verbose_name="Срок выполнения", default=7)
    due_date = models.IntegerField(verbose_name="Срок поддержки", default=28)
    image = models.ImageField(upload_to="services")
    status = models.IntegerField(default=1, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Работа"
        verbose_name_plural = "Работы"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_moderator', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault('is_superuser', False)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    is_moderator = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    @property
    def full_name(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Order(models.Model):
    STATUS_CHOICES = [
        (1, 'Зарегистрирован'),
        (2, 'Проверяется'),
        (3, 'Принято'),
        (4, 'Отказано'),
        (5, 'Удалено')
    ]

    services = models.ManyToManyField(Service, verbose_name="Работы", null=True)
    status = models.CharField(max_length=255, blank=True, null=True, choices=STATUS_CHOICES)
    date_created = models.DateTimeField(verbose_name="Дата создания", default=datetime.now(tz=timezone.utc))
    date_of_formation = models.DateTimeField(verbose_name="Дата формирования", null=True)
    date_complete = models.DateTimeField(verbose_name="Дата завершения", null=True)
    id_moderator = models.ForeignKey('CustomUser', on_delete=models.CASCADE,  db_column='id_moderator', related_name='moderator_it', blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Покупатель", null=True)
    deadline = models.CharField(verbose_name="Фактический срок выполнения заказа", null=True)
    def __str__(self):
        return "Заявка №" + str(self.pk)

    class Meta:
        verbose_name = "Заявки"
        verbose_name_plural = "Заявки"