from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe
from django.shortcuts import reverse
from django.forms import ModelForm, Textarea, TextInput
from ckeditor.fields import RichTextField
# from mptt.fields import TreeForeignKey
# from mptt.models import MPTTModel


from PIL import Image


class Account(models.Model):
    ACCOUNT_TYPE = (
        ('BCA', 'Basic Checking Account'),
        ('BRA', 'Brokerage Account'),
        ('BA', 'Business Account'),
        ('CDA', 'CDs Account'),
        ('CA', 'Current Account'),
        ('IBCA', 'Interest Bearing Checking Account'),
        ('IRA', 'IRAs Account'),
        ('MMA', 'Money Market Account'),
        ('OFA', 'Offshore Account'),
        ('SA', 'Savings Account'),
    )
    CURRENCY = (
        ('USD', 'USD'),
        ('GBP', 'GPB'),
        ('EUR', 'EUR'),
        ('TRY', 'TRY'),
        ('CNY', 'CNY'),
    )
    STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        
    )

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    acc_no = models.CharField(max_length=50, blank=True, null=True, unique=True)
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPE)
    balance = models.IntegerField(blank=True, null=True)
    
    initial_deposit = models.IntegerField(blank=True, null=True, default=5000)
    currency = models.CharField(max_length=10, choices=CURRENCY, default='USD')
    status = models.CharField(max_length=10, choices=STATUS, default='Pending')
    reg_date = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.get_account_type_display()} - {self.acc_no}" 

    def get_absolute_url(self):
        return reverse("myaccounts_detail", kwargs={"id": self.id})

    
class AccountForm(ModelForm):




    class Meta:
        model = Account
        fields = ['account_type', 'currency', 'initial_deposit']
       
        help_texts = {
            'initial_deposit': 'The mininum deposit is $25',
        }


class Emailsender(models.Model):
    subject = models.CharField(max_length=150)
    to = models.EmailField(max_length=150)
    message = RichTextField()

    def __str__(self):
        return self.subject

class EmailsenderForm(ModelForm):
    class Meta:
        model = Emailsender
        fields = ['subject', 'to', 'message']
       

class Xtransfer(models.Model):
    account = models.IntegerField()
    amount = models.IntegerField()
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True, max_length=255)

    def __str__(self):
        return self.account



# class XtransferForm(ModelForm):
#     class Meta:
#         model = Xtransfer
#         fields = ['account', 'amount', 'name', 'description']


class XtransferForm(ModelForm):
    class Meta:
        model = Xtransfer
        fields = ['account', 'amount', 'name', 'description']

