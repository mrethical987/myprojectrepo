# Generated by Django 3.2.7 on 2021-10-02 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_alter_post_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='desc',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
