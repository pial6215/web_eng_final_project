from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'location', 'bedrooms', 'price', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2 Room Flat Available'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Dhanmondi, Dhaka'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Per month rent'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write details about the flat...'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }