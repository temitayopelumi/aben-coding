# Generated by Django 4.1 on 2022-08-11 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_alter_user_stripeid_alter_user_subscriptionid'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='subscribed',
            field=models.BooleanField(default=False),
        ),
    ]
