# Generated by Django 4.1.7 on 2023-03-13 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1_manager', '0002_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='posts/'),
        ),
    ]