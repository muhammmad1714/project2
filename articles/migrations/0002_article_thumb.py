# Generated by Django 4.1.7 on 2023-07-10 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='thumb',
            field=models.ImageField(blank=True, default='img.jpg', upload_to=''),
        ),
    ]
