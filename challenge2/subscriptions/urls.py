from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.subscriptions_page, name="home"),
    path("success/", views.success, name="success"),
    path("canceled/", views.cancel, name="cancel"),
    path('webhook/', views.stripe_webhook, name="stripe_webhook"),
    path('cancel-sub', views.cancel_subscription, name="cancel_sub")
]