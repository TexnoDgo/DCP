from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



class Material(models.Model):
    title = models.CharField(max_length=100, verbose_name='МАТЕРИАЛ', default='DEFAULT')  # Материал

    def __str__(self):
        return self.title


class Assortment(models.Model):
    title = models.CharField(max_length=100, verbose_name='СОРТАМЕНТ', default='DEFAULT')  # Сортамент

    def __str__(self):
        return self.title


class Detail(models.Model):
    title = models.TextField(max_length=100, verbose_name='НАИМЕНОВАНИЕ ДЕТАЛИ')  # Наименование детали
    # Чертеж PDF
    draw_pdf = models.FileField(upload_to='PDF_DRAW', verbose_name='ЧЕРТЕЖ ДЕТАЛИ', default='PDF_DRAW/default.pdf')
    # Чертеж PNG
    draw_png = models.ImageField(upload_to='PNG_COVER', verbose_name='ОБЛОЖКА ДЕТАЛИ', default='PNG_COVER/default.png')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='АВТОР ДЕТАЛИ')  # Автор детали
    create = models.DateTimeField(default=timezone.now, verbose_name='ДАТА СОЗДАНИЯ')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='МАТЕРИАЛ')  # Материал
    assortment = models.ForeignKey(Assortment, on_delete=models.CASCADE, verbose_name='СОРТАМЕНТ')   # Сортамент


class Project(models.Model):
    title = models.CharField(max_length=100, verbose_name='НАЗВАНИЕ ПРОЕКТА')

    def __str__(self):
        return self.title


class Order(models.Model):
    title = models.CharField(max_length=100, verbose_name='НАЗВАНИЕ ЗАКАЗА')  #
    create = models.DateTimeField(default=timezone.now)  #
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='АВТОР ЗАКАЗА')  #
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='НАЗНАЧЕНИЕ ЗАКАЗА')  #
    readiness = models.DateField(verbose_name='ПРИБЛИЗИТЕЛЬНЫЙ СРОК ГОТОВНОСТИ')  #
    table = models.FileField(upload_to='TABLES', verbose_name='ТАБЛИЦА', null=True)
    qr_code_list = models.FileField(upload_to='QR_CODE_LIST', verbose_name='ФАЙЛ С КОДАМИ', null=True)


class Position(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='ЗАКАЗ')  #
    detail = models.ForeignKey(Detail, on_delete=models.CASCADE, verbose_name='ДЕТАЛЬ')  #
    quantity = models.PositiveIntegerField(default=1, verbose_name='Кол-во')  #
    code = models.CharField(max_length=32, db_index=True)
    qr_code = models.ImageField(upload_to='QR_CODE', verbose_name='КОД ДЕТАЛИ', default='QR_CODE/default.png')


class City(models.Model):
    title = models.CharField(max_length=20, verbose_name='НАЗВАНИЕ ГОРОДА')

    def __str__(self):
        return self.title


class Manufactured(models.Model):
    title = models.CharField(max_length=50, verbose_name='НАЗВАНИЕ')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='ГОРОД')

    def __str__(self):
        return self.title + ' ' + str(self.city)


class Operation(models.Model):

    OPR_STATUS = (
        ('CD', 'Created'),
        ('PD', 'Performed'),
        ('RD', 'Ready'),
    )

    title = models.CharField(max_length=50, verbose_name='НАЗВАНЕ ОПЕРАЦИИ', default='DEFAULT')  #
    manufactured = models.ForeignKey(Manufactured, on_delete=models.CASCADE, verbose_name='МЕСТО ИЗГОТОВЛЕНИЯ')  #
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name='ПОЗИЦИИ')  #
    status = models.CharField(max_length=20, choices=OPR_STATUS, default='CD', verbose_name='СТАТУС')  #
    # Остаток деталей. Изначально равно quantity(Check).
    # Значение изменяет Transaction.
    remaining_parts = models.PositiveIntegerField(default=1, verbose_name='КОЛ-ВО ОСТАВШИХСЯ ДЕТАЛЕЙ')

    def __str__(self):
        return self.title


class Transaction(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='АВТОР ТРАНЗАКЦИИ')  #
    create = models.DateTimeField(default=timezone.now, verbose_name='ДАТА СОЗДАНИЯ')  #
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, verbose_name='ОПЕРАЦИЯ')
    ready_quantity = models.PositiveIntegerField(default=1, verbose_name='КОЛ-ВО ГОТОВЫХ ДЕТАЛЕЙ')  #
