# Generated by Django 4.0.2 on 2022-04-13 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser', '0002_alter_parseurl_nextpageurl_alter_parseurl_subpageurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parseurl',
            name='SubPageURL',
            field=models.CharField(max_length=255, null=True),
        ),
    ]