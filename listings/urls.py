from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('create-listing/', views.create_listing, name='create_listing'),
    path('listing/<int:listing_id>/', views.listing_detail, name='listing_detail'),
    path('favorite/<int:listing_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('my-favorites/', views.favorites_list, name='favorites_list'),
    path('my-ads/', views.my_listings, name='my_listings'),
    path('listing/<int:listing_id>/delete/', views.delete_listing, name='delete_listing'),
    path('listing/<int:listing_id>/edit/', views.edit_listing, name='edit_listing'),
    path('dashboard/', views.owner_dashboard, name='dashboard'),
]