# Generated by Django 4.2 on 2024-04-02 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_usermovierating_watched'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='age_rating',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
