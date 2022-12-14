# Generated by Django 4.1 on 2022-08-11 21:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0003_user_subscribed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='subscriptionId',
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripeSubscriptionId', models.CharField(max_length=255, null=True)),
                ('status', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userSubscription', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
