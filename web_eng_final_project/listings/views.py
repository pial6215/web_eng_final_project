from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q 
from .models import Listing, Favorite
from .forms import ListingForm 

# 1. Home View (Search shoho)
def home_view(request):
    query = request.GET.get('search') 
    if query:
        listings = Listing.objects.filter(
            Q(title__icontains=query) | Q(location__icontains=query)
        ).order_by('-created_at')
    else:
        listings = Listing.objects.all().order_by('-created_at')
        
    return render(request, 'listings/home.html', {'listings': listings})

# 2. Create Listing (Image Upload shoho)
@login_required(login_url='/accounts/login/') 
def create_listing(request):
    if request.method == 'POST':
        # Eikhane request.FILES thaka khub-i jaruri image upload-er jonno
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.host = request.user 
            listing.save() 
            return redirect('home') 
    else:
        form = ListingForm()
    return render(request, 'listings/Notesing.html', {'form': form})

# 3. Listing Detail View
def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, 'listings/listing_detail.html', {'listing': listing})

# 4. Favorite Toggle View
@login_required
def toggle_favorite(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    
    favorite, created = Favorite.objects.get_or_create(user=request.user, listing=listing)
    
    if not created:
        favorite.delete() # Age favorite thakle unfavorite hobe
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))