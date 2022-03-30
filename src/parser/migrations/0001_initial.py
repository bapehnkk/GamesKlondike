# Generated by Django 4.0.2 on 2022-03-26 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ParseUrl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SiteName', models.CharField(max_length=255, unique=True)),
                ('SiteURL', models.URLField()),
                ('SubPageURL', models.URLField(blank=True, null=True)),
                ('NextPageUrl', models.URLField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Parse URL',
                'verbose_name_plural': 'Parse URL',
            },
        ),
        migrations.CreateModel(
            name='SubpageSelector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Selector', models.TextField(blank=True, null=True)),
                ('UrlID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subpage_selector', to='parser.parseurl')),
            ],
            options={
                'verbose_name': 'Page selector',
                'verbose_name_plural': 'Page selector',
            },
        ),
        migrations.CreateModel(
            name='PageSelector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Selector', models.TextField(blank=True, null=True)),
                ('UrlID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='page_selector', to='parser.parseurl')),
            ],
            options={
                'verbose_name': 'Page selector',
                'verbose_name_plural': 'Page selector',
            },
        ),
    ]