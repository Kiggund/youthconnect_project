# Generated by Django 5.2 on 2025-04-15 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('join', '0002_alter_member_dob_alter_member_marital_status_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={'ordering': ['-time_joined']},
        ),
        migrations.AlterField(
            model_name='member',
            name='signature',
            field=models.ImageField(blank=True, null=True, upload_to='signatures/', verbose_name='Signature (Optional)'),
        ),
        migrations.AlterField(
            model_name='member',
            name='time_joined',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Registration Timestamp'),
        ),
    ]
