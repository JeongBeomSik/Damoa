# Generated by Django 2.2.3 on 2019-08-09 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BoardWrite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('writer', models.CharField(max_length=10)),
                ('up_date', models.DateTimeField(auto_now=True, verbose_name='date published')),
                ('title', models.CharField(max_length=30)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('content', models.TextField(blank=True, null=True)),
                ('lookup', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
