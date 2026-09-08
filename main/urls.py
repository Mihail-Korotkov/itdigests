from django.urls import path
from main import views
from main.views import refresh_digest



app_name = "main"


urlpatterns = [
    path('', views.MainView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('refresh/', views.refresh_digest, name='refresh'),


]