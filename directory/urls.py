from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submit/', views.submit_profile, name='submit_profile'),
    path('directory/', views.member_directory, name='directory'),
    path('delete/<int:pk>/', views.delete_profile, name='delete_profile'),
    path('edit/<int:id>/', views.edit_profile, name='edit_profile'),
    path('setup-notion/', views.setup_notion_config, name='setup_notion'),
]
