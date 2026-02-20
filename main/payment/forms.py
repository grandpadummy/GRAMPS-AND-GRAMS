from django import forms
from .models import ShippingAddress 


class ShippingForm(forms.ModelForm):
           

           shipping_full_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full Name'}))

           shipping_email = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}))

           shipping_address1 = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address Line 1'}))

           shipping_address2 = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address Line 2'}))

           shipping_city = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}))

           shipping_state = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}))

           shipping_zip_code = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zip Code'}))

           shipping_country = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}))

           shipping_phone_number = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}))

           class Meta:
                model = ShippingAddress
                fields = ['shipping_full_name', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_state', 'shipping_zip_code', 'shipping_country', 'shipping_phone_number']  

           exclude = ['user',]


class PaymentForm(forms.Form):
    card_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name On Card'}))

    card_number = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Number'}))
    card_exp_date = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Expiration'}))
    card_cvv_number = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'CVV Number'}))
    card_address1 = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing Address 1'}))
    card_address2 = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing Address 2'}))
    card_city = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing City'}))
    card_state = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing State'}))
    card_zip_code = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing Zip Code'}))
    card_country = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing Country'}))

