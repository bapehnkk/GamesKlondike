# Generated by Django 4.0.2 on 2022-04-11 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parseurl',
            name='NextPageUrl',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='parseurl',
            name='SubPageURL',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
