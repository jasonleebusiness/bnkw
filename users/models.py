from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.forms import ModelForm, Textarea, TextInput
from django.shortcuts import reverse
from home.models import BillCode
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

from account.models import Account

from django import forms


class Userprofile(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )


    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150,blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=150, blank=True, null=True)
    dob = models.DateField()
    gender = models.CharField(max_length=7, choices=GENDER, blank=True, null=True)
    address = models.CharField(max_length=150)
    occupation = models.CharField(max_length=150, blank=True, null=True)
    annual_income = models.IntegerField(blank=True, null=True)
    country = CountryField(blank_label='(select country)', multiple=False)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=10)
    zip = models.CharField(max_length=10)
    image = models.ImageField(
        blank=True, null=True, upload_to='images/users/', default="/avatar/avatar.png")
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'


    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    # img = Image.open(self.image.path)

    # if img.height > 250 or img.width > 250:
    #     output_size = (250,250)
    #     img.thumbnail(output_size)
    #     img.save(image.path)



    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    
    image_tag.short_description = 'Image'





class Transactions(models.Model):
    ACTION = (
        ('Debit', 'Debit'),
        ('Credit', 'Credit'),
    )
    
    CHANNEL = (
        ('Mobile Transfer', 'Mobile Transfer'),
        ('Online Transfer', 'Online Transfer'),
        ('Wire Transfer', 'Wire Transfer'),
        ('Inter Bank Transfer', 'Inter Bank Transfer'),
        ('P.O.S', '	P.O.S'),
        ('Cheque', 'Cheque'),
    )

    STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Completed', 'Completed'),
        ('Incompleted', 'Incompleted'),
        ('On Hold', 'On Hold'),
    )
    LOCALITY = (
        ('Same Country', 'Same Country'),
        ('Overseas Bank', 'Overseas Bank'),
        
    )


    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    beneficiary = models.CharField(max_length=250)
    bank_acc = models.CharField(max_length=250)
    bank = models.CharField(max_length=250)
    bank_branch = models.CharField(max_length=250, blank=True, null=True, default='Nil')
    bank_locality = models.CharField(max_length=20, choices=LOCALITY, default='Same Country', blank=True, null=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=250, blank=True, null=True, default='Nil')
    email = models.CharField(max_length=250, blank=True, null=True, default='Nil')
    swift = models.CharField(max_length=250, blank=True, null=True, default='Nil')
    iban = models.CharField(max_length=250, blank=True, null=True, default='Nil')
    routing = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS, default='Incompleted')
    action = models.CharField(max_length=10, choices=ACTION, default='Debit')
    channel = models.CharField(max_length=30, choices=CHANNEL, default='Online Transfer')
    date = models.DateTimeField(null=True, blank=True)
    address = models.CharField(max_length=250, blank=True, null=True, default='Nil')
    country = CountryField(blank_label='(select country)', multiple=False)
    # zip = models.CharField(max_length=10, blank=True, null=True)
    description = models.TextField(blank=True, null=True, max_length=255)
    code = models.CharField(max_length=8)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)
    confirm_code = models.BooleanField(default=False)
    bill_count = models.IntegerField(blank=True, null=True, default=0)
    created = models.DateTimeField(auto_now_add=True)
    

    def get_absolute_url(self):
        return reverse("transfer_detail", kwargs={"id": self.id})

    def __str__(self):
        return f"{self.amount} - {self.action} - {self.status}"

    class Meta:
            verbose_name = "Transaction"
            verbose_name_plural = "Transactions"


class TransferForm(ModelForm):
    class Meta:
        model = Transactions
        fields = ['beneficiary', 'bank_acc', 'bank', 'bank_locality', 'bank_branch', 'account', 'amount', 'swift', 'iban', 'phone', 'email', 'country', 'routing', 'address','description']
        labels = {
            'beneficiary': 'Beneficiary Account Name',
            'bank_acc': 'Beneficiary Account Number ',
            'account': 'Account(s)'
        }
        widgets = {
            # 'beneficiary': TextInput(attrs={'class':'form-control input-rounded', 'placeholder':'John Doe'}),
            # 'bank_acc': TextInput(attrs={'class':'form-control input-rounded', 'placeholder':'405667189905'}),
            'country': CountrySelectWidget()
        }


class Beneficiary(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=250)
    bank_acc = models.CharField(max_length=250)
    bank = models.CharField(max_length=250)
    bank_branch = models.CharField(max_length=250, blank=True, null=True)
    phone = models.CharField(max_length=250, blank=True, null=True)
    email = models.CharField(max_length=250, blank=True, null=True)
    swift = models.CharField(max_length=250)
    iban = models.CharField(max_length=250, blank=True, null=True)
    routing = models.IntegerField(blank=True, null=True)  
    address = models.CharField(max_length=250, blank=True, null=True, default='Nil')
    country = CountryField(blank_label='(select country)', multiple=False)
    description = models.TextField(blank=True, null=True, max_length=255)
    amount = models.IntegerField(blank=True, null=True,)
    query = models.CharField(max_length=250, blank=True, null=True)
    account = models.ForeignKey(Account, blank=True, null=True, on_delete=models.CASCADE)
    
    # zip = models.CharField(max_length=10, blank=True, null=True)
   

    def __str__(self):
        return self.name

    class Meta:
            verbose_name = "Beneficiary"
            verbose_name_plural = "Beneficiaries"


class BeneficiaryForm(ModelForm):
    class Meta:
        model = Beneficiary
        fields = ['name', 'bank_acc', 'bank', 'bank_branch', 'swift', 'iban', 'phone', 'email','country', 'routing', 'address']
       

class BeneficiaryForm2(ModelForm):
    class Meta:
        model = Beneficiary
        fields = ['account', 'query', 'amount', 'description']
       


class Cheque(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Select an Account')
    amount = models.IntegerField(blank=True, null=True)
    issuer = models.CharField(max_length=250, verbose_name='Name of Cheque Issuer')
    bank = models.CharField(max_length=250, verbose_name='Issuer Bank Name')
    country = CountryField(blank_label='(select country)', multiple=False)
    front_img = models.ImageField(blank=True, null=True, upload_to='images/cheques/', verbose_name='Cheque Front View')
    back_img = models.ImageField(blank=True, null=True, upload_to='images/cheques/', verbose_name='Cheque Back View')
    code = models.CharField(max_length=8)
    date = models.DateField(blank=True, null=True, verbose_name='Cheque issued date')
    status = models.CharField(max_length=10, choices=STATUS, default='Pending')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"cheque -{self.issuer} - {self.amount}"



class ChequeForm(ModelForm):
    class Meta:
        model = Cheque
        fields = ['account', 'amount', 'issuer', 'bank', 'date', 'country', 'front_img', 'back_img',]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
       
class Card(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
    )
    CARDNETWORK = (
        ('MasterCard', 'MasterCard'),
        ('Visa', 'Visa'),
    )
    CARDTYPE = (
        ('Credit', 'Credit'),
        ('Debit', 'Debit'),
    )
    REQUESTTYPE = (
        ('CAR', 'Card Activated Request'),
        ('CDR', 'Card Deactivation Request'),
        ('CNR', 'Card Renewal Request'),
        ('CRR', 'Card Retrieval Request'),
        ('NCR', 'New Card Request'),
 
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)    
    status = models.CharField(max_length=10, choices=STATUS, default='Pending', blank=True, null=True)
    card_network = models.CharField(max_length=10, choices=CARDNETWORK)
    card_type = models.CharField(max_length=10, choices=CARDTYPE)
    request_type = models.CharField(max_length=10, choices=REQUESTTYPE)
    date = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Card -{self.account} - {self.card_network}"



class CardForm(ModelForm):
    class Meta:
        model = Card
        fields = ['account', 'card_network', 'card_type', 'request_type', 'description']
        
       
class Echeque(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    f_name = models.CharField(max_length=250, verbose_name = "First name")
    l_name = models.CharField(max_length=250, verbose_name = "Last name")
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=250)
    email = models.CharField(max_length=250)

    address = models.CharField(max_length=250, blank=True, null=True)
    country = CountryField(blank_label='(select country)', multiple=False)
    
    zip = models.CharField(max_length=220)
    state = models.CharField(max_length=225)
    city = models.CharField(max_length=225)
    code = models.CharField(max_length=8)
    status = models.CharField(max_length=10, choices=STATUS, default='Pending')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Echeque -{self.f_name} - {self.amount}"



class EchequeForm(ModelForm):
    class Meta:
        model = Echeque
        fields = ['f_name', 'l_name', 'city', 'state', 'account', 'amount', 'zip', 'phone', 'email','country', 'address']
       
