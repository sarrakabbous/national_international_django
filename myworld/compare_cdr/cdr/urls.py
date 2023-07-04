from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('extract-columns/', views.extract_columns, name='extract_columns'),
    path('compare/', views.compare, name='compare'),


]