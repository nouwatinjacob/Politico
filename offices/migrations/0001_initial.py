# Generated by Django 2.1.5 on 2019-03-26 12:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='OfficeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('office_type', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='candidate',
            name='office',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='offices.OfficeModel'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='candidate',
            unique_together={('office', 'user')},
        ),
    ]
