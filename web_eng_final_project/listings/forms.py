from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Listing

# 1. Sign Up Form (Eita Sign Up Page sundor korbe)
class SignUpForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=15, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email Address'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Shob ghor-e Bootstrap class auto add kora
        for field in self.fields:
            if field != 'phone_number' and field != 'email':
                self.fields[field].widget.attrs.update({'class': 'form-control', 'placeholder': f'Enter {field}'})

# 2. Listing Form (Eita Basha Vara deyar form sundor korbe)
class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'location', 'bedrooms', 'price', 'description', 'image', 'phone_number']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2 Room Flat Available'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Khagan, Ashulia'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Per month rent'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write details about the flat...'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'}),
        }