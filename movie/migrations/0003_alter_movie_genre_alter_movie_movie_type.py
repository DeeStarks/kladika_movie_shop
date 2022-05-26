# Generated by Django 4.0.4 on 2022-05-26 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_alter_movie_genre_alter_movie_movie_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.genre'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='movie_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.movietype'),
        ),
    ]
