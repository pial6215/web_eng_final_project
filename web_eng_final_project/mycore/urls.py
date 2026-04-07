from django.contrib import admin
from django.urls import path, include
from listings import views # listings app theke views niye asha hochhe

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')), 
    
    # Ei nicher line-tai ashole Home Page er rasta!
    path('', views.home_view, name='home'), 
]