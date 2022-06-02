from django.urls import path
from Notes import views

app_name = 'notes'

urlpatterns = [
    path('register', views.user_register, name='registration'),
    path('login', views.user_login, name='login'),

]
