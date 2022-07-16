from django.urls import path, include

from .views import get_current_page, get_on_week_page

urlpatterns = [
    path('now', get_current_page, name='now'),
    path('week', get_on_week_page, name='week')
]
