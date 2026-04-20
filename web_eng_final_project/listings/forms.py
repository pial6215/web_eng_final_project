from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Listing

# --- 1. Multiple Image Support Helper ---
# Django default FileInput multiple files read korte pare na, tai eita dorkar.
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

# --- 2. Sign Up Form ---
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
        for field in self.fields:
            if field not in ['phone_number', 'email']:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control', 
                    'placeholder': f'Enter {field.replace("_", " ").capitalize()}'
                })

# --- 3. Listing Form (The Fix) ---
class ListingForm(forms.ModelForm):
    # Eikhane 'MultipleFileField' use kora hoyeche jate validation error na dey
    images = MultipleFileField(
        widget=MultipleFileInput(attrs={
            'class': 'd-none', 
            'id': 'image-upload',
            'multiple': True,
            'accept': 'image/*'
        }),
        required=False,
        label="Upload Property Images"
    )

    class Meta:
        model = Listing
        # 'host' field-ta exclude kora hoyeche karon views theke request.user boshabo
        fields = ['title', 'location', 'bedrooms', 'price', 'description', 'phone_number']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2 Room Flat Available'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Khagan, Ashulia'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Per month rent'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write details about the flat...'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'}),
        }