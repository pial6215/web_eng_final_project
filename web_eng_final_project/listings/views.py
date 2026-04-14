from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q  # Eita lagbe search er jonno
from .models import Listing
from .forms import ListingForm 

def home_view(request):
    query = request.GET.get('search') 
    if query:
        # Title ba Location jekonota match korlei result dekhabe
        listings = Listing.objects.filter(
            Q(title__icontains=query) | Q(location__icontains=query)
        ).order_by('-created_at')
    else:
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
    
    # Apnar file name anujayi Notesing.html-e thaklo
    return render(request, 'listings/Notesing.html', {'form': form})