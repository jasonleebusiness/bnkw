from django.db import models

# Create your models here.
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
# from django.forms import ModelForm
from django.forms import ModelForm, TextInput, Textarea
from django.db.models import Avg, Count
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe
# from mptt.fields import TreeForeignKey
# from mptt.models import MPTTModel

from django.dispatch import receiver
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget




class Setting(models.Model):
    # STATUS = (
    #     ('True', 'True'),
    #     ('False', 'False'),
    # )
    otp_status = models.BooleanField(default=False, help_text="Check box to 'Enable use of OTP in transfer' and Uncheck box to 'Disable use of OTP in transfer' ")
    name = models.CharField(max_length=150, blank=True, null=True,)
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(max_length=50)
    address = RichTextUploadingField(blank=True)
    phone = models.CharField(blank=True, max_length=15)
    address2 = RichTextUploadingField(blank=True)
    phone2 = models.CharField(blank=True, null=True, max_length=15)
    email = models.CharField(blank=True, max_length=50)
    icon = models.ImageField(blank=True, null=True, upload_to='images/logo/')
    icontext = models.ImageField(blank=True, null=True, upload_to='images/logo/')
    iconblue = models.ImageField(blank=True, null=True, upload_to='images/logo/')
    iconwhite = models.ImageField(blank=True, null=True, upload_to='images/logo/')
    iconfav = models.ImageField(blank=True, null=True, upload_to='images/logo/')
    

    def __str__(self):
        return self.title


class ContactMessage(models.Model):

   
    name = models.CharField(blank=True, max_length=150)
    email = models.CharField(blank=True, max_length=50)
    phone = models.CharField(blank=True, max_length=25) 
    subject = models.CharField(blank=True, max_length=150) 
    message = models.TextField(blank=True, max_length=255)
    ip = models.CharField(blank=True, max_length=100)
    note = models.CharField(blank=True, max_length=100)
    # date = models.DateTimeField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.phone}'


class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name','phone', 'email', 'message', 'subject']
        # widgets = {
        #     'name': TextInput(attrs={'class': 'input col-lg-6 col-md-6 col-sm-6', 'placeholder': 'Name & Surname'}),
        #     'subject': TextInput(attrs={'class': 'input col-lg-6 col-md-6 col-sm-6', 'placeholder': 'Subject'}),
        #     'phone': TextInput(attrs={'class': 'input col-lg-6 col-md-6 col-sm-6', 'placeholder': 'phone'}),
        #     'email': TextInput(attrs={'class': 'input col-lg-6 col-md-6 col-sm-6', 'placeholder': 'Email Address'}),
        #     'message': Textarea(attrs={'class': 'input col-12', 'placeholder': 'Your Message', 'rows': '5'}),
        # }


class Faqs(models.Model):

    question = models.CharField(max_length=200)
    answer = RichTextUploadingField()

    def __str__(self):
        return self.question





class Subscribe(models.Model):
    email = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return self.email


class SubscribeForm(ModelForm):
    class Meta:
        model = Subscribe
        fields = ['email']
        widgets = {

            'email': TextInput(attrs={'class': 'email-box', 'placeholder': 'Email Address'}),

        }



        
class BillCode(models.Model):
    
    name = models.CharField( max_length=120)
    code = models.CharField( max_length=20)
    description = RichTextUploadingField()
    status = models.BooleanField(default=False, help_text="Check box to 'Enable' and Uncheck box to 'Disable' this Code ")

    def __str__(self):
        return self.name