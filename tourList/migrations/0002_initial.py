# Generated by Django 5.0.3 on 2024-05-20 08:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tourList', '0001_initial'),
        ('user', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.company'),
        ),
        migrations.AddField(
            model_name='order',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='review',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='savedplace',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tourlist',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.company'),
        ),
        migrations.AddField(
            model_name='touritem',
            name='tour_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tourList.tourlist'),
        ),
        migrations.AddField(
            model_name='savedplace',
            name='tour_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tourList.tourlist'),
        ),
        migrations.AddField(
            model_name='review',
            name='tour_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tourList.tourlist'),
        ),
        migrations.AddField(
            model_name='order',
            name='tour_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tourList.tourlist'),
        ),
    ]
