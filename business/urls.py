from django.urls import path
from . import views


urlpatterns = [
    path(
        'business/<slug:slug>/', views.business_detail, name='business_detail'
    ),
    path('directory/', views.directory, name='directory'),
]
