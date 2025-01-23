from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('proxpo/', views.proxpo, name = "proxpo"),
    path('',views.project_list, name = "project_list"),
    path('index/<int:project_id>/', views.index, name="index"),
    path('project_create/',views.project_create, name="project_create"),
    path('<int:project_id>/edit/',views.project_edit, name="project_edit"),
    path('<int:project_id>/delete/',views.project_delete, name="project_delete"),
    path('search/', views.search_users, name='search_users'),
    path('register/', views.register, name = "register"),

    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
]