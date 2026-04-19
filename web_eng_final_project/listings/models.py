from django.db import models
from django.conf import settings

class Listing(models.Model):
    # host field-e related_name='listings' add korlam jate 
    # user.listings.all() diye oi user-er shob post khuje pawa jay
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='listings'
    )
    
    image = models.ImageField(upload_to='listings/', null=True, blank=True)
    
    # Ei phone_number ta specific flat-er contact number (default remove kora bhalo)
    phone_number = models.CharField(max_length=15, help_text="Contact number for this property")
    
    title = models.CharField(max_length=200, help_text="e.g. 2 Room flat for rent in Dhanmondi")
    description = models.TextField()
    location = models.CharField(max_length=150)
    
    # DecimalField use kora-i best price-er jonno
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.location}"

class Favorite(models.Model):
    # related_name use korle query kora shohoj hoy
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='favorites'
    )
    listing = models.ForeignKey(
        Listing, 
        on_delete=models.CASCADE, 
        related_name='favorited_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ekjon user ekta post ekbar-i favorite korte parbe
        unique_together = ('user', 'listing') 

    def __str__(self):
        return f"{self.user.username} likes {self.listing.title}"