from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser
import re

class SignUpForm(UserCreationForm):
    # Role choices: Admin bad diye shudhu Student ar Owner
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('owner', 'House Owner'),
    ]
    
    role = forms.ChoiceField(
        choices=ROLE_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    phone_number = forms.CharField(
        max_length=15, 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. 017XXXXXXXX'})
    )
    
    university_id = forms.CharField(
        max_length=50, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Required for students'})
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # Default fields er sathe email, role, phone ar uni_id jog kora hoyeche
        fields = UserCreationForm.Meta.fields + ('email', 'role', 'phone_number', 'university_id',)

    # 1. Phone Number Validation (Live check er por backend check)
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not re.match(r'^\d{11,15}$', phone):
            raise ValidationError("Valid phone number din (11-15 digits).")
        return phone

    # 2. Role-wise Validation (Student hole ID chara submit hobe na)
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        uni_id = cleaned_data.get('university_id')

        if role == 'student' and not uni_id:
            self.add_error('university_id', "Give a valid University ID!")
        
        return cleaned_data

    # 3. Bootstrap Styling apply kora shob field-e
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Role field-er class already Select widget-e deya hoyeche
            if field_name != 'role':
                field.widget.attrs.update({'class': 'form-control'})
# accounts/forms.py
def clean_username(self):
    username = self.cleaned_data.get('username')
    if username.isdigit():
        raise ValidationError("Username must contain at least one letter.")
    return username