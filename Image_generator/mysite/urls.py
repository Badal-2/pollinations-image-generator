from django.contrib import admin
from django.urls import path,include
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/generate/', views.generate_image, name='generate_image'),
    path('api/gallery/', views.get_gallery, name='get_gallery'),
    path('api/download/<int:image_id>/', views.download_image, name='download_image'),
]