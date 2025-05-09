# Generated by Django 5.2 on 2025-04-26 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Full name of the person sending the message', max_length=255, verbose_name="Sender's Name")),
                ('email', models.EmailField(help_text='Valid email address for reply correspondence', max_length=254, verbose_name='Email Address')),
                ('content', models.TextField(help_text='The main body of the message', verbose_name='Message Content')),
                ('timestamp', models.DateTimeField(auto_now_add=True, help_text='When the message was submitted', verbose_name='Received Timestamp')),
            ],
            options={
                'verbose_name': 'Contact Message',
                'verbose_name_plural': 'Contact Messages',
                'ordering': ['-timestamp'],
            },
        ),
    ]
