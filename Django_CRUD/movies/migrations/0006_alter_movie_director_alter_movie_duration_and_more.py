# Generated by Django 4.2 on 2024-04-06 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_remove_usermovierating_watched'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='director',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='movie',
            name='duration',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='movie',
            name='image_url',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='movie',
            name='rating',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='release_year',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='trailer_url',
            field=models.URLField(),
        ),
    ]
