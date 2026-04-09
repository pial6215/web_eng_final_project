from django.contrib import admin
from django.urls import path, include
from listings import views # listings app theke views niye asha hochhe

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')), 
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')), 
    path('', views.home_view, name='home'), 
    path('create-listing/', views.create_listing, name='create_listing'),
    path('', views.home_view, name='home'), 
]