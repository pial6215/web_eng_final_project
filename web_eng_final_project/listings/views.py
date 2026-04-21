from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q 
from django.http import HttpResponseForbidden
from .models import Listing, Favorite, ListingImage
from .forms import ListingForm 

# 1. Home View (Heart logic fix kora hoyeche)
def home_view(request):
    query = request.GET.get('search') 
    if query:
        listings = Listing.objects.filter(
            Q(title__icontains=query) | Q(location__icontains=query)
        ).order_by('-created_at')
    else:
        listings = Listing.objects.all().order_by('-created_at')
    
    # PREMIUM FIX: User favorite list pathano jate home page-e heart lal hoye thake
    user_favorite_ids = []
    if request.user.is_authenticated:
        user_favorite_ids = Favorite.objects.filter(user=request.user).values_list('listing_id', flat=True)
        
    return render(request, 'listings/home.html', {
        'listings': listings, 
        'user_favorite_ids': user_favorite_ids
    })

# 2. Create Listing (Multiple Image Support)
@login_required(login_url='/accounts/login/') 
def create_listing(request):
    if getattr(request.user, 'role', '') != 'owner':
        return HttpResponseForbidden("Oops! Only House Owners can post listings.")

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        images = request.FILES.getlist('images') 
        
        if form.is_valid():
            listing = form.save(commit=False)
            listing.host = request.user 
            listing.save() 
            
            for img in images:
                ListingImage.objects.create(listing=listing, image=img)
                
            return redirect('home')
    else:
        form = ListingForm()
    
    return render(request, 'listings/listing_form.html', {'form': form})

# 3. Listing Detail View
def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, listing=listing).exists()
        
    return render(request, 'listings/listing_detail.html', {'listing': listing, 'is_favorite': is_favorite})

# 4. Favorite Toggle View
@login_required(login_url='/accounts/login/')
def toggle_favorite(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, listing=listing)
    if not created:
        favorite.delete()
    
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('home')

# 5. Favorites List View
@login_required(login_url='/accounts/login/')
def favorites_list(request):
    # Ekhaneo heart icon check korar jonno list-ta dorkar
    favorites = Favorite.objects.filter(user=request.user).select_related('listing')
    listings = [fav.listing for fav in favorites]
    user_favorite_ids = Favorite.objects.filter(user=request.user).values_list('listing_id', flat=True)
    
    return render(request, 'listings/favorites.html', {
        'listings': listings, 
        'user_favorite_ids': user_favorite_ids
    })

# 6. My Listings View
@login_required(login_url='/accounts/login/')
def my_listings(request):
    user_ads = Listing.objects.filter(host=request.user).order_by('-created_at')
    return render(request, 'listings/my_listings.html', {'user_ads': user_ads})

# 7. Delete Listing
@login_required(login_url='/accounts/login/')
def delete_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, host=request.user)
    if request.method == 'POST':
        listing.delete()
        return redirect('my_listings')
    return render(request, 'listings/delete_confirm.html', {'listing': listing})

# 8. Edit Listing
@login_required(login_url='/accounts/login/')
def edit_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, host=request.user)
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            # Jodi naya chobi add korte chan editing-e:
            images = request.FILES.getlist('images')
            for img in images:
                ListingImage.objects.create(listing=listing, image=img)
            return redirect('my_listings')
    else:
        form = ListingForm(instance=listing)
    return render(request, 'listings/listing_form.html', {'form': form, 'edit_mode': True})
from django.shortcuts import redirect

@login_required(login_url='/accounts/login/')
def owner_dashboard(request):
    if getattr(request.user, 'role', '') != 'owner':
        return redirect('home') # Student-ra dashboard-e ashle home-e chole jabe
    
    user_listings = Listing.objects.filter(host=request.user).order_by('-id')
    return render(request, 'listings/dashboard.html', {'listings': user_listings})
from django.shortcuts import get_object_or_404, redirect

# --- DELETE LISTING ---
@login_required
def delete_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    
    # Security: Check korsi user owner kina ebong shei ei ad-er owner kina
    if getattr(request.user, 'role', '') == 'owner' and listing.host == request.user:
        listing.delete()
        return redirect('dashboard')
    else:
        return HttpResponseForbidden("Apnar ei ad delete korar khomota nai!")

# --- EDIT LISTING ---
@login_required
def edit_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    
    # Security check
    if getattr(request.user, 'role', '') != 'owner' or listing.host != request.user:
        return HttpResponseForbidden("Apni ei ad edit korte parben na.")

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ListingForm(instance=listing)
    
    return render(request, 'listings/listing_form.html', {'form': form, 'edit_mode': True})
