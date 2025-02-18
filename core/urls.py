from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('multiplication/', views.multiplication_game, name='multiplication_game'),
    path('quick-math/', views.quick_math, name='quick_math'),
    path('practice/', views.practice_mode, name='practice_mode'),
    path('profile/', views.profile, name='profile'),
] 