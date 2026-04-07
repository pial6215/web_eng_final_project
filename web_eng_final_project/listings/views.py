from django.shortcuts import render
from .models import Listing

def home_view(request):

    all_listings = Listing.objects.all().order_by('-created_at')
    
    return render(request, 'listings/home.html', {'listings': all_listings})