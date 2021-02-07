# Generated by Django 3.1.4 on 2021-01-02 17:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('kml', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='fileserver',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('filename', models.FileField(blank=True, upload_to='fileserver/')),
            ],
        ),
    ]
