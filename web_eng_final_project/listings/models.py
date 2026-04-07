from django.db import models
from django.conf import settings

class Listing(models.Model):
    # Ke biggapon dichhe tar sathe link
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Barir biboron
    title = models.CharField(max_length=200, help_text="Jemon: 2 Room flat for rent")
    description = models.TextField()
    location = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Vara koto
    bedrooms = models.IntegerField()
    
    # Kokhon post kora hoyeche
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title