# Generated by Django 3.2.15 on 2022-12-14 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorvirtual', '0002_contenido_autor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contenido',
            name='autor',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='contenido',
            name='titulo',
            field=models.CharField(max_length=50),
        ),
    ]