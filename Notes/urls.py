from django.urls import path
from Notes import views

app_name = 'notes'

urlpatterns = [
    path('register', views.user_register, name='registration'),
    path('login', views.user_login, name='login'),
    path('', views.list_create, name='list_create'),
    path('<int:note_id>/details', views.detail, name='detail'),
    path('<int:note_id>/update', views.update, name='update'),
    path('<int:note_id>/delete', views.delete, name='delete'),
    path('search/', views.NoteSearchView.as_view(), name='search'),
]
