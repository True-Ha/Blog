# Generated by Django 4.1.7 on 2023-04-26 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_remove_post_views'),
    ]

    operations = [
        migrations.CreateModel(
            name='IpModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='views',
            field=models.ManyToManyField(blank=True, related_name='post_views', to='posts.ipmodel'),
        ),
    ]