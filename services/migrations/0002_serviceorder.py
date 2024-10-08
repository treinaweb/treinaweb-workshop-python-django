# Generated by Django 5.1.1 on 2024-09-25 01:19

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('extra_info', models.TextField()),
                ('status', models.CharField(choices=[('OPEN', 'Aberta'), ('CANCELED', 'Cancelada'), ('DONE', 'Finalizada'), ('FINISHED', 'Concluída')], default='OPEN', max_length=10)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.service')),
            ],
            options={
                'verbose_name': 'Oderm de Serviço',
                'verbose_name_plural': 'Ordens de Serviço',
            },
        ),
    ]
