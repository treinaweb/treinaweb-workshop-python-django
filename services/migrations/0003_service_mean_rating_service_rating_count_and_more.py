# Generated by Django 5.1.1 on 2024-09-25 05:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_serviceorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='mean_rating',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=3),
        ),
        migrations.AddField(
            model_name='service',
            name='rating_count',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.CreateModel(
            name='ServiceOrderReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField()),
                ('comment', models.TextField()),
                ('service_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.serviceorder')),
            ],
            options={
                'verbose_name': 'Avaliação',
                'verbose_name_plural': 'Avaliações',
            },
        ),
    ]
