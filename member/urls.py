from django.urls import path
from . import views

urlpatterns = [
    path(
        'apply_for_beta_access/',
        views.apply_for_beta_access,
        name='apply_for_beta_access'
    ),
    path(
        'beta-contact/',
        views.beta_contact_view,
        name='beta_contact'
    ),
    path(
        'beta_features/',
        views.beta_features_view,
        name='beta_features'
    ),
    path(
        'login/',
        views.CustomLoginView.as_view(),
        name='account_login'
    ),
]
