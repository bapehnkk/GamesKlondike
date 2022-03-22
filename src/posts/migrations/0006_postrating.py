# Generated by Django 4.0.2 on 2022-03-22 20:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0005_posttag_alter_commentlikedislike_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Stars', models.SmallIntegerField()),
                ('Email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating_user', to=settings.AUTH_USER_MODEL)),
                ('PostID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating_post', to='posts.postgame')),
            ],
        ),
    ]
