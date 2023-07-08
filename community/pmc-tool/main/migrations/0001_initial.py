# Generated by Django 4.2.2 on 2023-07-07 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PullRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_username', models.CharField(max_length=100)),
                ('count', models.IntegerField()),
                ('creation_timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'pullRequests',
            },
        ),
    ]
