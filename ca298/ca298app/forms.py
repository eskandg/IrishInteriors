from django import forms
from django.forms import ModelForm, ModelChoiceField
from .models import Product, CaUser, ProductCategory, Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction


class CategoryChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class ProductForm(ModelForm):
    category = CategoryChoiceField(queryset=ProductCategory.objects.all())

    class Meta:
        model = Product
        fields = ['name', 'description', 'weight', 'dimensions', 'price', 'picture', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'maxlength': 400,'placeholder': 'Enter product name here..'}),
            'description': forms.TextInput(attrs={'maxlength': 400, 'placeholder': 'Enter product description here..'}),
            'weight': forms.TextInput(attrs={'maxlength': 10000, 'placeholder': 'Enter the weight here..'}),
            'dimensions': forms.TextInput(attrs={'maxlength': 400, 'placeholder': 'Enter the dimensions here..'}),
            'price': forms.NumberInput(attrs={'maxlength': 10, 'placeholder': 'Enter product price here..'}),
        }


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['cardholder_name', 'card_number', 'cvv_number', 'shipping_address']
        widgets = {
            'cardholder_name': forms.TextInput(attrs={'maxlength': 100, 'placeholder': 'Enter name on card here...'}),
            'card_number': forms.NumberInput(attrs={'min': 0, 'max': 9999999999999999999, 'placeholder': 'Enter your card number here...'}),
            'cvv_number': forms.NumberInput(attrs={'min': 0, 'max': 999, 'placeholder': 'Enter 3 digit cvv number...'}),
            'shipping_address': forms.TextInput(attrs={'maxlength': 500, 'placeholder': 'Enter your address here...'})
        }


class CASignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CaUser

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = False
        user.save()
        return user


class AdminSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CaUser

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = True
        user.save()
        return user


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
    username = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username...'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password...'}))

