# Generated by Django 3.2.4 on 2021-06-25 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Complex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=32)),
                ('price', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'Complex',
                'verbose_name_plural': 'Complexes',
                'db_table': 'complex',
            },
        ),
        migrations.CreateModel(
            name='Procedures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=32)),
                ('price', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'Procedure',
                'verbose_name_plural': 'Procedures',
                'db_table': 'procedure',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.CharField(editable=False, max_length=32)),
                ('username', models.CharField(max_length=32)),
                ('name', models.CharField(blank=True, max_length=32, null=True)),
                ('surname', models.CharField(blank=True, max_length=32, null=True)),
                ('black_list', models.BooleanField(default=False)),
                ('subscribe', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('admin', 'Admin'), ('user', 'User')], default='user', max_length=5)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'users',
            },
        ),
    ]
