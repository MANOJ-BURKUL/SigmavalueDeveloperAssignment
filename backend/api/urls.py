from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('localities/', views.get_localities, name='get_localities'),
    path('analyze/', views.analyze_query, name='analyze_query'),
]
