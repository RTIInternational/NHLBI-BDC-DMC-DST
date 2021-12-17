# Generated by Django 3.2.9 on 2021-12-17 18:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_alter_ticket_ticket_review_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='aws_iam',
            field=models.CharField(blank=True, default='', help_text="If you're uploading to Amazon, please provide your AWS IAM (ex: arn:aws:iam::123456789012:user/username)", max_length=100, validators=[django.core.validators.RegexValidator('^arn:aws:iam::[0-9]{12}:user/[a-zA-Z0-9-_]{1,64}$', 'AWS IAM format invalid. Please use the following format: arn:aws:iam::123456789012:user/username')], verbose_name='AWS IAM'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='consent_code',
            field=models.CharField(default='', help_text='Please refer to Data Custodian Instructions for more information', max_length=100, validators=[django.core.validators.RegexValidator('^[a-z0-9][a-z0-9.]{0,59}[a-z0-9]$', 'Consent Code format invalid')], verbose_name='Consent Code'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='google_email',
            field=models.EmailField(blank=True, default='', help_text="If you're uploading to Google, please provide your google email for access", max_length=254, verbose_name='Google Email'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='study_id',
            field=models.CharField(default='', help_text='Please refer to Data Custodian Instructions for more information', max_length=100, validators=[django.core.validators.RegexValidator('^[a-z0-9][a-z0-9.]{0,59}[a-z0-9]$', 'Study ID format invalid')], verbose_name='Study ID'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='study_name',
            field=models.CharField(default='', help_text='Name of Study or Dataset', max_length=250, verbose_name='Study Name'),
        ),
    ]
