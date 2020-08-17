# Generated by Django 3.1 on 2020-08-17 19:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assortment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='DEFAULT', max_length=100, verbose_name='СОРТАМЕНТ')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='НАЗВАНИЕ ГОРОДА')),
            ],
        ),
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=100, verbose_name='НАИМЕНОВАНИЕ ДЕТАЛИ')),
                ('draw_pdf', models.FileField(default='PDF_DRAW/default.pdf', upload_to='PDF_DRAW', verbose_name='ЧЕРТЕЖ ДЕТАЛИ')),
                ('draw_png', models.ImageField(default='PNG_COVER/default.png', upload_to='PNG_COVER', verbose_name='ОБЛОЖКА ДЕТАЛИ')),
                ('create', models.DateTimeField(default=django.utils.timezone.now, verbose_name='ДАТА СОЗДАНИЯ')),
                ('assortment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MainApp.assortment', verbose_name='СОРТАМЕНТ')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='АВТОР ДЕТАЛИ')),
            ],
        ),
        migrations.CreateModel(
            name='Manufactured',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='НАЗВАНИЕ')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MainApp.city', verbose_name='ГОРОД')),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='DEFAULT', max_length=100, verbose_name='МАТЕРИАЛ')),
            ],
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='НАЗВАНЕ ОПЕРАЦИИ')),
                ('status', models.CharField(choices=[('CD', 'Created'), ('PD', 'Performed'), ('RD', 'Ready')], default='CD', max_length=20, verbose_name='СТАТУС')),
                ('remaining_parts', models.PositiveIntegerField(default=1, verbose_name='КОЛ-ВО ОСТАВШИХСЯ ДЕТАЛЕЙ')),
                ('qr_code', models.ImageField(default='QR_CODE/default.png', upload_to='QR_CODE', verbose_name='КОД ДЕТАЛИ')),
                ('manufactured', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MainApp.manufactured', verbose_name='МЕСТО ИЗГОТОВЛЕНИЯ')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='НАЗВАНИЕ ЗАКАЗА')),
                ('create', models.DateTimeField(default=django.utils.timezone.now)),
                ('readiness', models.DateTimeField(verbose_name='ПРИБЛИЗИТЕЛЬНЫЙ СРОК ГОТОВНОСТИ')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='АВТОР ЗАКАЗА')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='НАЗВАНИЕ ПРОЕКТА')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create', models.DateTimeField(default=django.utils.timezone.now, verbose_name='ДАТА СОЗДАНИЯ')),
                ('ready_quantity', models.PositiveIntegerField(default=1, verbose_name='КОЛ-ВО ГОТОВЫХ ДЕТАЛЕЙ')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='АВТОР ТРАНЗАКЦИИ')),
                ('operation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MainApp.operation', verbose_name='ОПЕРАЦИЯ')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Кол-во')),
                ('detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MainApp.detail', verbose_name='ДЕТАЛЬ')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MainApp.order', verbose_name='ЗАКАЗ')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MainApp.project', verbose_name='НАЗНАЧЕНИЕ ЗАКАЗА'),
        ),
        migrations.AddField(
            model_name='operation',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MainApp.position', verbose_name='ПОЗИЦИИ'),
        ),
        migrations.AddField(
            model_name='detail',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MainApp.material', verbose_name='МАТЕРИАЛ'),
        ),
    ]