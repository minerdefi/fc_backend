from django.urls import path
from .views import home, health_check

urlpatterns = [
    path('home/', home),
    path('health/', health_check),
    path('', home),
]
