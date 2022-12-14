# Generated by Django 3.2.15 on 2022-12-14 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contenido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50, unique=True)),
                ('contenido', models.TextField()),
                ('relacionados', models.ManyToManyField(related_name='_tutorvirtual_contenido_relacionados_+', to='tutorvirtual.Contenido')),
            ],
            options={
                'verbose_name': 'Contenido',
                'verbose_name_plural': 'Contenidos',
            },
        ),
    ]
