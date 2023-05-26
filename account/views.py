from ast import Try
from email.policy import HTTP
from typing import Tuple
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.urls import reverse_lazy
from urllib3 import HTTPResponse
from users.models import Userprofile, Transactions, Beneficiary, BillCode, Cheque, ChequeForm, Card, CardForm, BeneficiaryForm, TransferForm, BeneficiaryForm2, EchequeForm, Echeque
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.crypto import get_random_string
from .forms import PicUpdateForm, OpenAccountForm, OpenProfileForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import views as auth_views
from .models import Account, AccountForm, Emailsender, EmailsenderForm, Xtransfer, XtransferForm
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from home.models import Setting
from validate_email import validate_email
from .utils import generate_token, auth_user_should_not_access, generate_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
# from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading
import qrcode
from io import BytesIO
from django.core.files import File
import datetime
# from PIL import Image, ImageDraw


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

        print('sent i guess')





# Create your views here.
@login_required()
def account(request):
    current_user = request.user
    profile = Userprofile.objects.get(user_id=current_user.id)
    transaction = Transactions.objects.filter(
        user_id=current_user.id).exclude(status='Incompleted').order_by('-date')[:10]
    account1 = Account.objects.filter(user_id=current_user.id)[0]

    # accounts = Account.objects.filter(user_id=current_user.id)[1:]
    context = {
        'profile': profile,
        'transaction': transaction,
        'account1': account1,
        # 'accounts': accounts
    }
    return render(request, 'account/index.html', context)


def render_pdf_view(request, *args, **kwargs):
    pk = kwargs.get('pk')
    receipt = get_object_or_404(Transactions, pk=pk)
    setting = get_object_or_404(Setting, pk=1)
    template_path = 'account/pdf.html'
    context = {'receipt': receipt,
               'setting': setting,
               }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    response['Content-Disposition'] = 'inline; filename="receipt.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required()
def transferview(request):
    current_site = get_current_site(request)
    url = request.META.get('HTTP_REFERER')
    current_user = request.user

    accounts = Account.objects.filter(
        user_id=current_user.id, status='Approved')

    if request.method == 'POST':  # check post
        form = TransferForm(request.POST or None)

        if form.is_valid():
            # data1 = form.cleaned_data
            data = Transactions()

            data.account = form.cleaned_data['account']
            amount = form.cleaned_data['amount']
            data.amount = int(amount)
            data.beneficiary = form.cleaned_data['beneficiary']
            data.bank = form.cleaned_data['bank_acc']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.bank = form.cleaned_data['bank']
            data.bank_branch = form.cleaned_data['address']
            data.address = form.cleaned_data['address']
            data.zip = form.cleaned_data['zip']

            data.swift = form.cleaned_data['swift']
            data.routing = form.cleaned_data['routing']
            data.iban = form.cleaned_data['iban']
            data.country = form.cleaned_data['country']

            data.description = form.cleaned_data['description']
            data.user_id = current_user.id
            ordercode = get_random_string(8).upper()  # random code
            data.code = ordercode
            data.pin = form.cleaned_data['pin']
            data.date = datetime.datetime.now()
            if current_user.userprofile.pin == int(data.pin):
                # profile.balance = profile.balance - (data.amount + 10)
                transact = Account.objects.get(
                    user_id=current_user.id, account_type=data.account.account_type)
                transact.balance = transact.balance - (data.amount + 13)
                data.save()
                transact.save()

                t = f"https://{current_site}{data.get_absolute_url()}"
                qrcode_img = qrcode.make(t)
                fname = f'qr_code-{data.id}.png'
                buffer = BytesIO()
                qrcode_img.save(buffer, 'PNG')
                data.qr_code.save(fname, File(buffer), save=False)
                data.save()

                messages.success(
                    request, "Funds succesfully transfered.")
    

              

                return render(request, 'account/modalcontent.html')
            





@login_required()
def modal(request):
    pk = request.GET.get('pk')

    return render(request, 'account/transfer/modal.html',{'pk': pk})


@login_required()
def getbutton(request):
    pk = request.GET.get('pk')
    return render(request, 'account/transfer/getbutton.html',{'pk': pk})


@login_required()
def modalbutton(request):
    pk = request.GET.get('pk')
    if Transactions.objects.filter(pk=pk):
        return render(request, 'account/transfer/modalbutton.html', {'pk': pk})
    else:
        return HttpResponse('')



@login_required()
def nextbtn(request):
    pk = request.GET.get('pk')
    
    return render(request, 'account/transfer/nextbtn.html', {'pk': pk})

@login_required()
def nexttext(request):
    
    
    return HttpResponse('<span>Sending </span>')


@login_required()
def transferbutton(request):
    
    return render(request, 'account/transfer/transferbutton.html')

@login_required()
def transfer(request):
    current_site = get_current_site(request)
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    setting = Setting.objects.get(pk=1)
    bill_codes = BillCode.objects.filter(status=True)
    bill_count = BillCode.objects.filter(status=True).count()
    print('bill count ---', bill_count)
    print('bill codes ---', bill_codes)

    accounts = Account.objects.filter(
        user_id=current_user.id, status='Approved')

    if request.method == 'POST':  # check post
        form = TransferForm(request.POST or None)

        if form.is_valid():
            # data1 = form.cleaned_data
            data = Transactions()

            data.account = form.cleaned_data['account']
            amount = form.cleaned_data['amount']
            data.amount = int(amount)
            data.beneficiary = form.cleaned_data['beneficiary']
            data.bank_acc = form.cleaned_data['bank_acc']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.bank = form.cleaned_data['bank']
            data.bank_branch = form.cleaned_data['address']
            data.address = form.cleaned_data['address']
            data.zip = form.cleaned_data['zip']

            data.swift = form.cleaned_data['swift']
            data.routing = form.cleaned_data['routing']
            data.iban = form.cleaned_data['iban']
            data.country = form.cleaned_data['country']

            data.description = form.cleaned_data['description']
            locality = form.cleaned_data['bank_locality']
            if locality == 'Overseas Bank':
                data.bank_locality = "Overseas Bank"
            data.user_id = current_user.id
            ordercode = get_random_string(length=8, allowed_chars='0123456789')  # random code
            data.code = ordercode
           
            data.date = datetime.datetime.now()
            
              
            data.bill_count = bill_count
            
              
            transact = Account.objects.get(
                user_id=current_user.id, account_type=data.account.account_type)
            transact.balance = transact.balance - (data.amount + 13)
            data.save()
            transact.save()

            t = f"https://{current_site}{data.get_absolute_url()}"
            qrcode_img = qrcode.make(t)
            fname = f'qr_code-{data.id}.png'
            buffer = BytesIO()
            qrcode_img.save(buffer, 'PNG')
            data.qr_code.save(fname, File(buffer), save=False)
    
            data.save()

            

            bill_list = []
            for rs in bill_codes:
                bill_list.append(rs.name)

            context = {
                        'data': data,
                        'bill_list': bill_list,
                        'bill_count': bill_count
            }


            if setting.otp_status == True:

                user = request.user
                email_subject = 'Transfer TOKEN'

                ctx = {

                    'domain': current_site,
                    'url': data.get_absolute_url(),
                    'data': data,
                    'setting': setting

                }

                message = get_template('account/transfer/otp.html').render(ctx)
                msg = EmailMessage(email_subject, message, to=[
                                user.email], from_email=settings.DEFAULT_FROM_EMAIL)

                email = msg
                email.content_subtype = 'html'

                EmailThread(email).start()


                return render(request, 'account/transfer/spinner.html', context)

            


            if bill_count == 0:
                context = {
                    'pk': data.pk
                }
                return render(request, 'account/transfer/nocodesspinner.html', context)

            else:


                return render(request, 'account/transfer/progress.html', context)
                

        else:
            # messages.error(request, form.errors)
            return render(request, 'account/transfer/errortransfer.html')

    form = TransferForm()

    context = {
        'title': 'Transfer Funds',
        'accounts': accounts,
    }

    return render(request, 'account/transfer.html', context)


@login_required()
def transferinternal(request):

    current_site = get_current_site(request)
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    setting = Setting.objects.get(pk=1)
    bill_codes = BillCode.objects.filter(status=True)
    bill_count = BillCode.objects.filter(status=True).count()

    accounts = Account.objects.filter(
        user_id=current_user.id, status='Approved')

    if request.method == 'POST':  # check post
        form = TransferForm(request.POST or None)

        if form.is_valid():
            # data1 = form.cleaned_data
            data = Transactions()

            data.account = form.cleaned_data['account']
            amount = form.cleaned_data['amount']
            data.amount = int(amount)
            data.beneficiary = form.cleaned_data['beneficiary']
            data.bank_acc = form.cleaned_data['bank_acc']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.bank = form.cleaned_data['bank']
            data.bank_branch = form.cleaned_data['address']
            data.address = form.cleaned_data['address']
            data.zip = form.cleaned_data['zip']

            data.swift = form.cleaned_data['swift']
            data.routing = form.cleaned_data['routing']
            data.iban = form.cleaned_data['iban']
            data.country = form.cleaned_data['country']

            data.description = form.cleaned_data['description']
            data.user_id = current_user.id
            ordercode = get_random_string(length=8, allowed_chars='0123456789')  # random code
            data.code = ordercode
           
            data.date = datetime.datetime.now()
            
            data.bill_count = bill_count
            
              
            transact = Account.objects.get(
                user_id=current_user.id, account_type=data.account.account_type)
            transact.balance = transact.balance - (data.amount + 13)
            data.save()
            transact.save()

            t = f"https://{current_site}{data.get_absolute_url()}"
            qrcode_img = qrcode.make(t)
            fname = f'qr_code-{data.id}.png'
            buffer = BytesIO()
            qrcode_img.save(buffer, 'PNG')
            data.qr_code.save(fname, File(buffer), save=False)
    
            data.save()

            

            bill_list = []
            for rs in bill_codes:
                bill_list.append(rs.name)

            context = {
                        'data': data,
                        'bill_list': bill_list,
                        'bill_count': bill_count
            }


            if setting.otp_status == True:

                user = request.user
                email_subject = 'Transfer TOKEN'

                ctx = {

                    'domain': current_site,
                    'url': data.get_absolute_url(),
                    'data': data,
                    'setting': setting

                }

                message = get_template('account/transfer/otp.html').render(ctx)
                msg = EmailMessage(email_subject, message, to=[
                                user.email], from_email=settings.DEFAULT_FROM_EMAIL)

                email = msg
                email.content_subtype = 'html'

                EmailThread(email).start()


                return render(request, 'account/transfer/spinner.html', context)

            


            if bill_count == 0:
                context = {
                    'pk': data.pk
                }
                return render(request, 'account/transfer/nocodesspinner.html', context)

            else:


                return render(request, 'account/transfer/progress.html', context)
            

        else:
            # messages.error(request, form.errors)
            return render(request, 'account/transfer/errortransfer.html')

    form = TransferForm()

    context = {
        'title': 'Transfer Funds',
        'accounts': accounts,
    }

    return render(request, 'account/transferinternal.html', context)


@login_required()
def transfer_detail(request, id):
    current_user = request.user
    profile = Userprofile.objects.get(user_id=current_user.id)
    transfer = Transactions.objects.get(id=id)

    context = {
        'title': 'Transaction receipt',
        'transfer': transfer,
        'profile': profile
    }
    return render(request, 'account/transfer-detail.html', context)


@login_required()
def all_transactions(request):
    current_user = request.user
    profile = Userprofile.objects.get(user_id=current_user.id)
    transaction = Transactions.objects.filter(
        user_id=current_user.id).exclude(status='Incompleted').order_by('-id')

    context = {
        'transaction': transaction,
        # 'profile': profile
    }
    return render(request, 'account/transactions.html', context)


@login_required()
def add_beneficiary(request):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user

    if request.method == 'POST':  # check post
        form = BeneficiaryForm(request.POST or None)

        if form.is_valid():
            # data1 = form.cleaned_data
            data = Beneficiary()
            data.name = form.cleaned_data['name']
            data.bank_acc = form.cleaned_data['bank_acc']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.bank = form.cleaned_data['bank']
            data.bank_branch = form.cleaned_data['address']
            data.address = form.cleaned_data['address']
            data.zip = form.cleaned_data['zip']
            data.swift = form.cleaned_data['swift']
            data.routing = form.cleaned_data['routing']
            data.iban = form.cleaned_data['iban']
            data.country = form.cleaned_data['country']
            data.user_id = current_user.id
            data.save()

            messages.success(
                request, "Beneficiary succesfully Added.")
                
            return HttpResponseRedirect(reverse('account'))

        else:
            messages.error(request, form.errors)
            return HttpResponseRedirect(url)

    form = BeneficiaryForm()

    context = {
        'title': 'Add Beneficiary',


        'form': form,


    }

    return render(request, 'account/add-beneficiary.html', context)


@login_required()
def beneficiaries(request):
    current_user = request.user
    profile = Userprofile.objects.get(user_id=current_user.id)
    beneficiaries = Beneficiary.objects.filter(user_id=current_user.id)
    context = {
        'title': 'Transfer Funds',
        'beneficiaries': beneficiaries,

        'profile': profile,

    }
    return render(request, 'account/beneficiaries.html', context)

 # Check login


@login_required()
def deletebeneficiary(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    Beneficiary.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Beneficiary deleted..')
    return HttpResponseRedirect(url)


@login_required()
def transfer_beneficiary(request):
    current_site = get_current_site(request)
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    beneficiaries = Beneficiary.objects.filter(user_id=current_user.id)
    accounts = Account.objects.filter(
        user_id=current_user.id, status='Approved')
    profile = Userprofile.objects.get(user_id=current_user.id)
    setting = Setting.objects.get(pk=1)
    bill_codes = BillCode.objects.filter(status=True)
    bill_count = BillCode.objects.filter(status=True).count()
    # print(bill_count)

    if request.method == 'POST':  # check post
        form = BeneficiaryForm2(request.POST or None)

        if form.is_valid():
            # data1 = form.cleaned_data
            data = Transactions()
            bid = form.cleaned_data['query']
            benefit = Beneficiary.objects.get(id=bid, user_id=current_user.id)
            data.account = form.cleaned_data['account']
            data.beneficiary = benefit.name
            data.bank = benefit.bank
            amount = form.cleaned_data['amount']
            data.amount = int(amount)
            data.swift = benefit.swift
            data.routing = benefit.routing
            data.iban = benefit.iban
            data.bank_acc = benefit.bank_acc
            data.phone = benefit.phone
            data.email = benefit.email
            data.zip = benefit.zip
            data.bank_branch = benefit.address
            data.address = benefit.address
            data.country = benefit.country
            data.description = form.cleaned_data['description']
            data.user_id = current_user.id
            ordercode = get_random_string(length=8, allowed_chars='0123456789')  # random code
            data.code = ordercode
            data.date = datetime.datetime.now()
            data.bill_count = bill_count
            
                # profile.balance = profile.balance - (data.amount + 10)
            transact = Account.objects.get(
                user_id=current_user.id, account_type=data.account.account_type)
            transact.balance = transact.balance - (data.amount + 13)
            data.save()
            transact.save()

            t = f"https://{current_site}{data.get_absolute_url()}"
            qrcode_img = qrcode.make(t)
            fname = f'qr_code-{data.id}.png'
            buffer = BytesIO()
            qrcode_img.save(buffer, 'PNG')
            data.qr_code.save(fname, File(buffer), save=False)
    
            data.save()

            

            bill_list = []
            for rs in bill_codes:
                bill_list.append(rs.name)

            context = {
                        'data': data,
                        'bill_list': bill_list,
                        'bill_count': bill_count
            }


            if setting.otp_status == True:

                user = request.user
                email_subject = 'Transfer TOKEN'

                ctx = {

                    'domain': current_site,
                    'url': data.get_absolute_url(),
                    'data': data,
                    'setting': setting

                }

                message = get_template('account/transfer/otp.html').render(ctx)
                msg = EmailMessage(email_subject, message, to=[
                                user.email], from_email=settings.DEFAULT_FROM_EMAIL)

                email = msg
                email.content_subtype = 'html'

                EmailThread(email).start()


                return render(request, 'account/transfer/spinner.html', context)

            

            if bill_count == 0:
                context = {
                    'pk': data.pk
                }
                return render(request, 'account/transfer/nocodesspinner.html', context)

            else:


                return render(request, 'account/transfer/progress.html', context)
            

        else:
            # messages.error(request, form.errors)
            return render(request, 'account/transfer/errortransfer.html')


    form = TransferForm()

    context = {
        'title': 'Transfer Funds',
        'beneficiaries': beneficiaries,
        'accounts': accounts,
        'form': form,
        'profile': profile,

    }

    return render(request, 'account/transfer-beneficiary.html', context)


def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Password Reset'

    ctx = {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user),
        'settings': get_object_or_404(Setting, pk=1)
    }

    message = get_template('account/password-email.html').render(ctx)
    msg = EmailMessage(email_subject, message, to=[
                       user.email], from_email=settings.DEFAULT_FROM_EMAIL)
    msg.content_subtype = 'html'
    email = msg

    EmailThread(email).start()


class PasswordReset(auth_views.PasswordResetView):

    html_email_template_name = 'account/password-email.html'
    template_name = 'account/password_reset.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = Setting.objects.get(pk=1)
        current_site = get_current_site(self.request)
        context.update({'setting': setting,
                        'domain': current_site,
                        })
        return context


class PasswordResetDone(auth_views.PasswordResetDoneView):
    template_name = 'account/password-reset-done.html'


class PasswordResetConfirm(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'


class PasswordResetComplete(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


def register(request):
    context = {'data': request.POST}
    if request.method == 'POST':
        acc_form = OpenAccountForm(request.POST)
        profile_form = OpenProfileForm(request.POST)
        if acc_form.is_valid() and profile_form.is_valid():

            # email = profile_form.cleaned_data['email']
            # if not validate_email(email):
            #     messages.add_message(request, messages.ERROR,
            #                         'Enter a valid email address')
            #     context['has_error'] = True
            #     return redirect('register')

            data = Userprofile()
            data.first_name = profile_form.cleaned_data['first_name']
            data.last_name = profile_form.cleaned_data['last_name']
            data.phone = profile_form.cleaned_data['phone']
            data.email = profile_form.cleaned_data['email']
            data.address = profile_form.cleaned_data['address']
            data.city = profile_form.cleaned_data['city']
            data.state = profile_form.cleaned_data['state']
            data.zip = profile_form.cleaned_data['zip']
            data.country = profile_form.cleaned_data['country']
            data.gender = profile_form.cleaned_data['gender']
            data.dob = profile_form.cleaned_data['dob']
            data.occupation = profile_form.cleaned_data['occupation']
            data.annual_income = profile_form.cleaned_data['annual_income']
            data.image = "/avatar/avatar.png"
            data.save()
            acc_form.save()
            # print(data.pk, 'form here.................')

            messages.success(request, f'Registration Complete.')
            return redirect('openAccConfirm', id=data.pk)
        else:
            acc_form = OpenAccountForm()
            profile_form = OpenProfileForm()
            messages.error(
                request, f'Incomplete form - Check your inputs properly and try again')

    acc_form = OpenAccountForm()
    profile_form = OpenProfileForm()
    context = {
        'acc_form': acc_form,
        'profile_form': profile_form,
        'data': request.POST
    }
    return render(request, 'front/register.html', context)


def openAccConfirm(request, id):
    # data = Userprofile.objects.get(id=id)
    data = get_object_or_404(Userprofile, pk=id)
    return render(request, 'front/open-acc-confirm.html', {'data': data})


@auth_user_should_not_access
def login_form(request):
    url = request.META.get('HTTP_REFERER')
    context = {'has_error': False}
    # username = User.objects.get()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # current_user = request.user
            # userprofile = Userprofile.objects.get(user_id=current_user.id)
            # request.session['userimage'] = userprofile.image.url
            messages.success(
                request, f"Login Successful")

            return HttpResponseRedirect(reverse('account'))

        else:
            messages.error(
                request, "Login unsuccessful. Invalid credentials!")
            return HttpResponseRedirect(reverse('account'))

    context = {

    }
    return render(request, 'account/login.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required()
def account_profile(request):
    current_user = request.user
    profile = Userprofile.objects.get(user_id=current_user.id)
    account = Account.objects.filter(user_id=current_user.id).first()
    form = PicUpdateForm()
    context = {
        'profile': profile,
        'form': form,
        'account': account
    }
    return render(request, 'account/profile.html', context)


@login_required()
def user_password(request):
    # current_user = request.user
    # profile = Userprofile.objects.get(user_id=current_user.id)
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return HttpResponseRedirect(url)
        else:
            messages.error(
                request, str(form.errors))
            return HttpResponseRedirect(url)
  



@login_required()
def user_update_pic(request):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    if request.method == 'POST':
        profile_form = PicUpdateForm(
            request.POST, request.FILES, instance=request.user.userprofile)
        if profile_form.is_valid():

            profile_form.save()
            messages.success(request, 'Your Profile picture has been updated!')
            return HttpResponseRedirect(url)
    else:

        profile_form = PicUpdateForm(instance=request.user.userprofile)

        messages.error(
            request, 'Invalid Credentials')
        return HttpResponseRedirect(url)


@login_required()
def myaccounts(request):
    current_user = request.user
    # profile = Userprofile.objects.get(user_id=current_user.id)
    accounts = Account.objects.filter(user_id=current_user.id)

    context = {
        'accounts': accounts,
        # 'profile': profile
    }
    return render(request, 'account/myaccounts.html', context)


@login_required()
def myaccounts_detail(request, id):
    current_user = request.user
    profile = Userprofile.objects.get(user_id=current_user.id)
    account = Account.objects.get(user_id=current_user.id, id=id)
    last_deposit = Transactions.objects.filter(
        account_id=id, user_id=current_user.id, action='Credit').last()
    last_withdraw = Transactions.objects.filter(
        account_id=id, user_id=current_user.id, action='Debit').last()

    context = {
        'account': account,
        'profile': profile,
        'last_deposit': last_deposit,
        'last_withdraw': last_withdraw,
    }
    return render(request, 'account/myaccounts-detail.html', context)


def create_account(request):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user

    # profile = Userprofile.objects.get(user_id=request.user)
    accounts = Account.objects.filter(
        user_id=current_user.id, status='Pending')
    # form_accounts = Account.objects.filter(user_id=current_user.id, status='Approved')
    if request.method == 'POST':  # check post
        form = AccountForm(request.POST or None)

        if form.is_valid():
            # data1 = form.cleaned_data
            data = Account()

            data.account_type = form.cleaned_data['account_type']
            data.currency = form.cleaned_data['currency']
            amount = form.cleaned_data['initial_deposit']
            if amount > 25:

                data.amount = int(amount)
                data.user = current_user
                data.save()
                messages.info(
                    request, "Registered! Your Account is been processed, you will be notified when the account is Active")

                return HttpResponseRedirect(url)
            else:
                messages.error(request, 'Sorry, The Minimum Deposit is $25')
                return HttpResponseRedirect(url)

        else:
            messages.error(request, 'Sorry, The Minimum Deposit is $25')
            return HttpResponseRedirect(url)

    form = AccountForm()

    context = {
        # 'profile': profile,
        'accounts': accounts,
        # 'form_accounts': form_accounts,
        'form': form
    }
    return render(request, 'account/create-account.html', context)


@login_required()
def echeque(request):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    echeque = Echeque.objects.filter(user_id=current_user.id)
    accounts = Account.objects.filter(
        user_id=current_user.id, status='Approved')
    if request.method == 'POST':  # check post
        form = EchequeForm(request.POST or None)

        if form.is_valid():
            # data1 = form.cleaned_data
            data = Echeque()

            data.account = form.cleaned_data['account']
            data.f_name = form.cleaned_data['f_name']
            data.l_name = form.cleaned_data['l_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address = form.cleaned_data['address']
            data.state = form.cleaned_data['state']
            data.zip = form.cleaned_data['zip']
            data.city = form.cleaned_data['city']
            data.country = form.cleaned_data['country']
            amount = form.cleaned_data['amount']
            data.amount = int(amount)

            data.user_id = current_user.id
            ordercode = get_random_string(length=8, allowed_chars='0123456789')  # random code
            data.code = ordercode
            data.save()
            messages.info(
                request, "Sent! Your e-Cheque is under review, you will be notified when the cheque has been processed")

            return HttpResponseRedirect(url)

        else:
            messages.error(request, form.errors)
            context = {
                'title': 'Send Echeque',
                'f_ctx': request.POST,
                'accounts': accounts,
            }
            return render(request, 'account/echeque.html', context)

    form = EchequeForm()

    context = {
        'title': 'Send E-Cheque',
        'echeque': echeque,
        'accounts': accounts

    }

    return render(request, 'account/echeque.html', context)


@login_required()
def cheque(request):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    cheque = Cheque.objects.filter(user_id=current_user.id)
    accounts = Account.objects.filter(
        user_id=current_user.id, status='Approved')

    if request.method == 'POST':  # check post
        form = ChequeForm(request.POST or None)

        if form.is_valid():
            # data1 = form.cleaned_data
            data = Cheque()

            data.issuer = form.cleaned_data['issuer']
            data.bank = form.cleaned_data['bank']
            data.account = form.cleaned_data['account']
            data.front_img = form.cleaned_data['front_img']
            data.back_img = form.cleaned_data['back_img']
            data.country = form.cleaned_data['country']
            amount = form.cleaned_data['amount']
            data.amount = int(amount)

            data.user_id = current_user.id
            ordercode = get_random_string(length=8, allowed_chars='0123456789')  # random code
            data.code = ordercode
            data.save()
            messages.info(
                request, "Done! Your Cheque is under review, you will be notified when the cheque has been processed")

            return HttpResponseRedirect(url)

        else:
            messages.error(request, form.errors)
            return HttpResponseRedirect(url)

    form = ChequeForm()

    context = {
        'title': 'Deposit Cheque',
        'cheque': cheque,

        'accounts': accounts

    }

    return render(request, 'account/cheque-deposit.html', context)

@login_required()
def card(request):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    cards_p = Card.objects.filter(user_id=current_user.id, status='Pending')
    cards_a = Card.objects.filter(user_id=current_user.id, status='Approved')
    accounts = Account.objects.filter(
        user_id=current_user.id, status='Approved')
    profile = Userprofile.objects.get(user_id=current_user.id)
    if request.method == 'POST':  # check post
        form = CardForm(request.POST or None)

        if form.is_valid():
            # data1 = form.cleaned_data
            data = Card()
            data.account = form.cleaned_data['account']
            data.card_network = form.cleaned_data['card_network']
            data.card_type = form.cleaned_data['card_type']
            data.request_type = form.cleaned_data['request_type']
            data.description = form.cleaned_data['description']

            data.user_id = current_user.id
            data.save()
            messages.info(
                request, "Request sent, you will be notified when the card has been processed")

            return HttpResponseRedirect(url)

        else:
            messages.error(request, form.errors)
            return HttpResponseRedirect(url)

    form = CardForm()

    context = {
        'title': 'Deposit Cheque',
        'cards_a': cards_a,
        'cards_p': cards_p,
        'form': form,
        'profile': profile,
        'accounts': accounts

    }

    return render(request, 'account/card.html', context)



@login_required()
def xemail(request):
    current_site = get_current_site(request)
    url = request.META.get('HTTP_REFERER')
    setting = Setting.objects.get(pk=1)
    current_user = request.user
  
    if request.method == 'POST':  # check post
        form = EmailsenderForm(request.POST or None)

        if form.is_valid():
            # data1 = form.cleaned_data
            data = Emailsender()

            data.subject = form.cleaned_data['subject']
            data.to = form.cleaned_data['to']
            data.message = form.cleaned_data['message']
            data.save()

            ctx = {

                'domain': current_site,
                'message': data.message,
                'setting': setting

            }
            message = get_template('front/xemail2.html').render(ctx)
            msg = EmailMessage(data.subject, message, to=[
                               data.to], from_email=settings.DEFAULT_FROM_EMAIL)

            email = msg
            email.content_subtype = 'html'
            email.send()

            messages.success(
                request, "Email succesfully sent...")

        return HttpResponseRedirect(url)

    form = EmailsenderForm()
    context = {
        'form': form
    }

    return render(request, 'front/xemail-sender.html', context)




@login_required()
def xtransfer(request):
    current_site = get_current_site(request)
    url = request.META.get('HTTP_REFERER')
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    accounts = Account.objects.all()
    profile = Userprofile.objects.get(user_id=current_user.id)
  
    if request.method == 'POST':  # check post
        form = XtransferForm(request.POST or None)

        if form.is_valid():
            # data1 = form.cleaned_data
            data = Transactions()

            acc_no = form.cleaned_data['account']
            print(acc_no)
           
            account = Account.objects.get(pk=form.cleaned_data['account'])
            print(acc_no)
            

            data.account = account
            data.bank_acc = account.acc_no
            data.bank_branch = 'Miami'
            data.address = '1111 Brickell Ave, Miami, FL 33131, United States'
            data.swift = '4566721'
            amount = form.cleaned_data['amount']
            data.amount = int(amount)
            data.beneficiary = form.cleaned_data['name']
            data.bank = setting.title
            data.phone = profile.phone
            data.email = profile.email
            
        
            data.zip = profile.zip

   
            data.country = profile.country

            description = form.cleaned_data['description']
            data.description = str(description)
            data.user_id = account.user.id
            ordercode = get_random_string(length=8, allowed_chars='0123456789')  # random code
            data.code = ordercode
            data.action = 'Credit'
            data.status = 'Completed'
            data.date = datetime.datetime.now()
           
            account.balance = account.balance + int(amount)
            data.save()
            account.save()

            t = f"https://{current_site}{data.get_absolute_url()}"
            qrcode_img = qrcode.make(t)
            fname = f'qr_code-{data.id}.png'
            buffer = BytesIO()
            qrcode_img.save(buffer, 'PNG')
            data.qr_code.save(fname, File(buffer), save=False)
            data.save()

            messages.success(
                request, "Funds succesfully transfered.")

            ctx = {

                'domain': current_site,
                'message': 'Credit Notification',
                'setting': setting,
                'receipt': data,
                'account': account,
                'setting': setting

            }
            message = get_template('account/xtransfer-email.html').render(ctx)
            msg = EmailMessage(f'{setting.company} Transaction Notification', message, to=[
                               account.user.email], from_email=settings.DEFAULT_FROM_EMAIL)

            email = msg
            email.content_subtype = 'html'
            email.send()

            messages.success(
                request, "Email succesfully sent...")



            

            return HttpResponseRedirect(url)

            
        else:
            messages.error(request, 'incorrect account number')
            return HttpResponseRedirect(url)
        
    form = XtransferForm()
    context = {
        'form': form,
        'accounts': accounts
    }

    return render(request, 'account/xtransfer.html', context)



@login_required()
def checkotp(request, pk):

    code =  request.POST.get('code')
    # pk =  request.POST.get('pk')
    transfer = Transactions.objects.get(pk=pk)
    if code == transfer.code:
        return render(request, 'account/transfer/otpvalid.html')
    else:
        return render(request, 'account/transfer/otperror.html')



def otpfinish(request, pk):
    data = Transactions.objects.get(pk=pk)
    
    return render(request, 'account/transfer/otpfinish.html', {'data': data})


@login_required()
def confirmotp(request):
    code = request.POST.get('code')
    checkcode = Transactions.objects.get(code=code)
    if checkcode:
        checkcode.confirm_code = True
        checkcode.save()
        print(checkcode.confirm_code)
        return HttpResponseRedirect(reverse('otpfinish', kwargs={'pk':checkcode.id}))


    return render(request, 'account/confirmotp.html')




@login_required()
def transfercomplete(request, pk):
    
    
    return render(request, 'account/transfer/transfercomplete.html', {'pk': pk})



@login_required()
def transferfinal(request):
    pk = request.GET.get('pk')
    return render(request, 'account/transfer/transferfinal.html', {'pk': pk})

@login_required()
def resend_email(request):
    current_site = get_current_site(request)
    pk = request.GET.get('pk')
    data = Transactions.objects.get(pk=pk)
    user = request.user
    email_subject = 'Transfer TOKEN'

    ctx = {

        'domain': current_site,
        'url': data.get_absolute_url(),
        'data': data

    }

    message = get_template('account/transfer/otp.html').render(ctx)
    msg = EmailMessage(email_subject, message, to=[
                    user.email], from_email=settings.DEFAULT_FROM_EMAIL)

    email = msg
    email.content_subtype = 'html'

    EmailThread(email).start()
    return HttpResponse('<p>Email has been Sent. Check your email address</P>')


@login_required()
def nextcodepage(request):
    
    pk = request.POST.get('pk')
    print(pk)
    bill_codes = BillCode.objects.filter(status=True)
    bill_count = BillCode.objects.filter(status=True).count()
    bill_list = []
    data = Transactions.objects.get(pk=pk)
    for rs in bill_codes:
        bill_list.append(rs.code)
    # print(bill_list)
    if data.bill_count != 0:
        pos = bill_count - data.bill_count
    
        bill_code = bill_list[pos]
        int(bill_code)
        # bill = BillCode.objects.get(code=bill_code)
        # # print('bill code - ', bill_code )
        # # print(bill.description)
        data.bill_count = data.bill_count - 1
        data.save()
        # print('data - ', data.bill_count)

        
        context = {
            'data': data,
            'bill': BillCode.objects.get(code=bill_code)
        }


        return render(request, 'account/transfer/progress2.html', context)

    else:
        current_site = get_current_site(request)
        setting = Setting.objects.get(pk=1)

        data.status = "Pending"
        data.save()
        context = {
            'data': data,
            
        }
        user = request.user
        email_subject = 'Debit Transaction Notification'

        ctx = {

            'domain': current_site,
            'url': data.get_absolute_url(),
            'receipt': data,
            'setting': setting,
            'user': user

        }

        message = get_template('account/transfer/xtransfer-debit.html').render(ctx)
        msg = EmailMessage(email_subject, message, to=[
                        user.email], from_email=settings.DEFAULT_FROM_EMAIL)

        email = msg
        email.content_subtype = 'html'

        EmailThread(email).start()

        return render(request, 'account/transfer/progress-nocode.html', context)




@login_required()
def getcodeform(request):
    pk = request.GET.get('pk')
    bill_pk = request.GET.get('bill')
    # print(bill_pk)
    # bill = BillCode.objects.get(pk=bill_pk)
    # print(bill)
    context = {
        'pk': pk,
        'bill': BillCode.objects.get(pk=bill_pk)
    }
    return render(request, 'account/transfer/codeform.html', context)


@login_required()
def checkcode(request):
    code = request.POST.get('code')
    pk = request.POST.get('pk')
    datapk = request.POST.get('datapk')
    print('datapk ---', datapk)
    bill_code = BillCode.objects.get(pk=pk)
    # pk = request.POST.get('pk')
    transfer = Transactions.objects.get(pk=datapk)

    if bill_code.code == code:
        
        return render(request, 'account/transfer/codevalid.html', {'pk': transfer.pk})
    else:
        return render(request, 'account/transfer/codeerror.html')
  


def getnextcodepage(request):
    pk = request.GET.get('pk')
    bill_pk = request.GET.get('bill')
    # print(bill_pk)
    # bill = BillCode.objects.get(pk=bill_pk)
    # print(bill)
    context = {
        'data': Transactions.objects.get(pk=pk),
        'bill': BillCode.objects.get(pk=bill_pk)
    }
    return render(request, 'account/transfer/nextcodepage.html', context)


def getfinalpage(request):
    pk = request.GET.get('pk')
    context = {
        'pk': pk
    }
    return render(request, 'account/transfer/getfinalbutton.html', context)



@login_required()
def transferfinish(request, pk):
    pk = pk
    return render(request, 'account/transfer/transfercomplete.html', {'pk': pk})



def getnocodesbutton(request):
    pk = request.GET.get('pk')
   
    
    return render(request, 'account/transfer/nocodesbutton.html', {'pk': pk})