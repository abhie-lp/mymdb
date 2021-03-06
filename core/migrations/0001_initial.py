# Generated by Django 2.2.1 on 2019-05-18 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=155)),
                ('plot', models.TextField()),
                ('year', models.PositiveSmallIntegerField()),
                ('rating', models.PositiveSmallIntegerField(choices=[(0, 'NR - Not Rated'), (1, 'G - General Audience'), (2, 'PG - Parental Guidance'), (3, 'R - Restricted')], default=0)),
                ('runtime', models.PositiveSmallIntegerField()),
                ('website', models.URLField()),
            ],
        ),
    ]
