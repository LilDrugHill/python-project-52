# Generated by Django 4.1.1 on 2022-10-15 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0002_alter_labelmodel_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labelmodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
    ]
