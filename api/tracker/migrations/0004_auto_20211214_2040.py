# Generated by Django 3.2.9 on 2021-12-14 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_auto_20211214_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='last_updated_dt',
            field=models.DateTimeField(auto_now=True, verbose_name='Last Updated Date'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='study_name',
            field=models.CharField(default='', help_text='Name of Study or Dataset (if applicable)', max_length=250, verbose_name='Study Name'),
        ),
    ]