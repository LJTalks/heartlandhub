from django.urls import path
from . import views


urlpatterns = [
    path(
        '<slug:slug>/', views.business_detail, name='business_detail'
    ),
    path('', views.directory, name='directory'),
]
