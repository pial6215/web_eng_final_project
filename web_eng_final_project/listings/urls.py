from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('create-listing/', views.create_listing, name='create_listing'),
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('favorite/<int:listing_id>/', views.toggle_favorite, name='toggle_favorite'),
]