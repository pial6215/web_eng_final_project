from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.conf import settings
from pathlib import Path
from decimal import Decimal, InvalidOperation
from .models import Listing, Favorite, ListingImage
from .forms import ListingForm

# 1. Home View (Heart logic fix kora hoyeche)
def home_view(request):
    query = request.GET.get('search', '').strip()
    selected_location = request.GET.get('location', '').strip()
    min_price_raw = request.GET.get('min_price', '').strip()
    max_price_raw = request.GET.get('max_price', '').strip()

    listings = Listing.objects.all()
    if query:
        listings = listings.filter(
            Q(title__icontains=query) | Q(location__icontains=query)
        )
    if selected_location:
        listings = listings.filter(location__iexact=selected_location)

    try:
        min_price = Decimal(min_price_raw) if min_price_raw else None
    except InvalidOperation:
        min_price = None

    try:
        max_price = Decimal(max_price_raw) if max_price_raw else None
    except InvalidOperation:
        max_price = None

    if min_price is not None and max_price is not None and min_price > max_price:
        min_price, max_price = max_price, min_price

    if min_price is not None:
        listings = listings.filter(price__gte=min_price)
    if max_price is not None:
        listings = listings.filter(price__lte=max_price)

    listings = listings.order_by('-created_at')
    raw_location_options = Listing.objects.exclude(location__isnull=True).exclude(
        location__exact=''
    ).values_list('location', flat=True).distinct().order_by('location')
    location_options = [
        {
            'name': loc,
            'selected': bool(selected_location and selected_location.lower() == loc.lower()),
        }
        for loc in raw_location_options
    ]

    gallery_dir = Path(settings.MEDIA_ROOT) / 'listings' / 'gallery'
    recent_gallery_urls = []
    if gallery_dir.exists():
        valid_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
        gallery_files = [
            path for path in gallery_dir.iterdir()
            if path.is_file()
            and path.suffix.lower() in valid_extensions
            and path.name.lower() != 'logo.png'
        ]
        gallery_files.sort(key=lambda path: path.stat().st_mtime, reverse=True)
        recent_gallery_urls = [
            f"{settings.MEDIA_URL}listings/gallery/{path.name}" for path in gallery_files[:6]
        ]

    listings = list(listings)
    fallback_count = len(recent_gallery_urls)
    for index, listing in enumerate(listings):
        image_url = listing.primary_image_url
        if image_url and not image_url.lower().endswith('/logo.png'):
            listing.display_image_url = image_url
        elif fallback_count:
            listing.display_image_url = recent_gallery_urls[index % fallback_count]
        else:
            listing.display_image_url = None

    # PREMIUM FIX: User favorite list pathano jate home page-e heart lal hoye thake
    user_favorite_ids = []
    if request.user.is_authenticated:
        user_favorite_ids = Favorite.objects.filter(user=request.user).values_list('listing_id', flat=True)

    return render(request, 'listings/home.html', {
        'listings': listings,
        'user_favorite_ids': user_favorite_ids,
        'location_options': location_options,
        'selected_location': selected_location,
        'search_query': query,
        'selected_min_price': min_price_raw,
        'selected_max_price': max_price_raw,
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
