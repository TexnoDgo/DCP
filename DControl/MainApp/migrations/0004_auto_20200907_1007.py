# Generated by Django 3.1 on 2020-09-07 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0003_systemfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail',
            name='material',
            field=models.TextField(max_length=100, verbose_name='МАТЕРИАЛ'),
        ),
        migrations.DeleteModel(
            name='Material',
        ),
    ]
