from django.urls import path
from .views import viewHandler
urlpatterns=[
    path('settings/',viewHandler.as_view(),name='settings_history')
]