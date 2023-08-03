# Generated by Django 4.2.3 on 2023-08-03 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Upcoming_movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('release_date', models.CharField(max_length=200)),
                ('genres', models.CharField(max_length=200)),
                ('director', models.CharField(max_length=200)),
                ('cast', models.CharField(max_length=200)),
                ('duration', models.CharField(max_length=200)),
                ('views', models.IntegerField()),
                ('nationality', models.CharField(max_length=100)),
                ('distributor', models.CharField(max_length=200)),
                ('prediction', models.FloatField(blank=True, null=True)),
                ('image_url', models.CharField(max_length=200)),
                ('prediction_cinema', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'main_upcoming_movies',
            },
        ),
    ]
