from django.urls import path
from . import views


urlpatterns = [
    path('submit/', views.submit_business, name='submit_business'),
    path('<slug:slug>/update/', views.update_business, name='update_business'),
    path('<slug:slug>/', views.business_detail, name='business_detail'),
    path('', views.directory, name='directory'),
]
