from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput, EmailInput, Select, FileInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import Userprofile, Transactions
from .models import Account
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget



class TransferBeneficiary(forms.Form):
    account = forms.CharField(max_length=100)
    query = forms.CharField(max_length=100)
    amount = forms.CharField(max_length=100)
    description = forms.CharField(max_length=255)
    pin = forms.CharField(max_length=255)

# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Userprofile
#         fields = ('pin',)


# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Transactions
#         fields = ('test',)


class PicUpdateForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ('image',)
       

class OpenProfileForm(forms.ModelForm):
    middle_name = forms.CharField(max_length=100, required=False)
    class Meta:
        model = Userprofile
        fields = ('first_name', 'last_name', 'middle_name', 'phone', 'email', 'address', 'city', 'state', 'zip', 'country', 'gender', 'dob', 'occupation', 'annual_income')
     


class OpenAccountForm(forms.ModelForm):
    
    class Meta:
        model = Account
        fields = ('account_type', 'currency', 'initial_deposit')
        