from django.db import models
from django.conf import settings

class Listing(models.Model):
    # Ke biggapon dichhe tar sathe link
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='listings/', null=True, blank=True)
    phone_number = models.CharField(max_length=15, default="01700000000")
    title = models.CharField(max_length=200, help_text="Jemon: 2 Room flat for rent")
    description = models.TextField()
    location = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Vara koto
    bedrooms = models.IntegerField()
    
    # Kokhon post kora hoyeche
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Listing class theke ber hoye ebar Favorite class shuru
class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing') # Ekjon user ekta post ekbar-i favorite korte parbe

    def __str__(self):
        return f"{self.user.username} favorited {self.listing.title}"