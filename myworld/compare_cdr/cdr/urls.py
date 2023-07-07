from django.urls import path
from . import views
from django.urls import path
from .views import login_view, register_user
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.main, name='main'),
    path('extract-columns/', views.extract_columns, name='extract_columns'),
    path('compare/', views.compare, name='compare'),
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),

]


