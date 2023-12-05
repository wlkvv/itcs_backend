from datetime import datetime
from django.db import models
from django.utils import timezone


class Service(models.Model):
    name = models.CharField(verbose_name="Название", max_length=255)
    description = models.TextField(verbose_name="Описание", blank=True)
    price = models.IntegerField(verbose_name="Цена", default=1000)
    time = models.IntegerField(verbose_name="Срок выполнения", default=7)
    due_date = models.IntegerField(verbose_name="Срок поддержки", default=28)
    image = models.ImageField(upload_to="services")

    STATUS_CHOICES = [
        (1, 'Действует'),
        (2, 'Удалена'),
    ]
    status = models.IntegerField(default=1, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


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

    def __str__(self):
        return "Заявка №" + str(self.pk)

    class Meta:
        verbose_name = "Заявки"
        verbose_name_plural = "Заявки"

