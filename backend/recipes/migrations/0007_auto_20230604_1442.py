# Generated by Django 3.2.18 on 2023-06-04 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20230604_1325'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='tag',
            name='unique tag',
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(fields=('name', 'color', 'slug'), name='unique tag'),
        ),
    ]
