# Generated by Django 3.2.14 on 2022-07-18 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_programintent_lms_user_id_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='lms_user_id',
            field=models.IntegerField(db_index=True, null=True, unique=True),
        ),
    ]
