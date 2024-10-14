"""
URL configuration for ljtalks project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from . import views

# Function to render the maintenance view (if needed)
# def maintenance_view(request):
#     return render(request, 'maintenance.html')

urlpatterns = [
    path('accounts/', include("allauth.urls")),
    path('admin/', admin.site.urls),
    # Restricted to testers
    # path('info/', views.youtube_info_view, name='youtube-info-view'),
    # path('booking/', include('booking.urls')),
    # Include the URLs from the services app
    # path('services/', include('services.urls')),
    path('youtube/', include('ytapi.urls')),
    path('summernote/', include('django_summernote.urls')),
    path("", include("blog.urls"), name="blog-urls"),
    # Think we replaced this with the restricted tester only api path above
    # Public or other features (different to the api path, not sure how!)
    # path('youtube/', include('ytapi.urls'), name="youtube-info-view")
]
