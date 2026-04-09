from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Listing
from .forms import ListingForm 

def home_view(request):
    listings = Listing.objects.all().order_by('-created_at')
    return render(request, 'listings/home.html', {'listings': listings})


@login_required(login_url='/accounts/login/') 
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            
            listing = form.save(commit=False)
            
            listing.host = request.user 
            listing.save() 
            return redirect('home') 
    else:
        form = ListingForm()
    
    return render(request, 'listings/Notesing.html', {'form': form})