# Generated by Django 4.1.7 on 2023-04-24 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_rename_post_comment_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
