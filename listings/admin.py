from django.contrib import admin
from .models import Listing, ListingImage, Favorite

# Listing images gulo jate admin panel-e ekshathe dekha jay
class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price', 'host', 'bedrooms', 'created_at')
    search_fields = ('title', 'location', 'description')
    list_filter = ('location', 'bedrooms', 'created_at')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    inlines = [ListingImageInline]

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'created_at')
    search_fields = ('user__username', 'listing__title')
    list_filter = ('created_at',)

@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'listing')
    search_fields = ('listing__title',)