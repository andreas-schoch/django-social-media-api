# Generated by Django 2.2.2 on 2019-06-21 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='validationcode',
            name='status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('VALIDATED', 'VALIDATED')], default='PENDING', max_length=12),
        ),
    ]
