# Generated by Django 4.1.4 on 2022-12-11 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Repositorio', '0002_alter_comentarios_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentarios',
            name='cm_user',
            field=models.CharField(default='desconocido', max_length=1000000),
        ),
        migrations.AlterField(
            model_name='archivo',
            name='archivo',
            field=models.FileField(blank=True, upload_to='pdfs/'),
        ),
    ]
