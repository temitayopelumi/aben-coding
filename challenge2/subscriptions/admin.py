from django.contrib import admin
from subscriptions.models import User, Subscription
# Register your models here.
admin.site.register(User)
admin.site.register(Subscription)