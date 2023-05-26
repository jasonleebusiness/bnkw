# Create your views here.
from audioop import reverse
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request

from django.views.generic import View, ListView, DetailView
from .models import Setting, ContactForm, ContactMessage

def home(request):
    return HttpResponseRedirect('/in')

def index(request):
    
    return render(request, 'front/index.html')


def aboutus(request):
    
    return render(request, 'front/about-us.html')


def contactus(request):

    url = request.META.get('HTTP_REFERER')
    
    if request.method == 'POST':  # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data1 = form.cleaned_data
            data = ContactMessage()  # create relation with model
            
            data.name = form.cleaned_data['name']  # get form input data
            data.phone = form.cleaned_data['phone']  # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.info(
                request, "Thank you for contacting us - Our Team will get back to you shortly. ")
            

            return HttpResponseRedirect(url)
    
    form = ContactForm()
   
    context = {
               
        'form': form,
       
    }

    return render(request, 'front/contact-us.html', context)


def mission(request):
    
    return render(request, 'front/mission.html')


def expectation(request):
    
    return render(request, 'front/expectations.html')


def career(request):
    
    return render(request, 'front/sustainability.html')


def p_checking(request):
    
    return render(request, 'front/p-checking.html')

def p_savings(request):
    
    return render(request, 'front/p-savings.html')

def p_cards(request):
    
    return render(request, 'front/p-cards.html')

def p_invest(request):
    
    return render(request, 'front/p-invest.html')

def p_retire(request):
    
    return render(request, 'front/p-retire.html')

def p_mortgage(request):
    
    return render(request, 'front/p-mortgage.html')

def p_auto(request):
    
    return render(request, 'front/p-auto.html')

def b_checking(request):
    
    return render(request, 'front/b-checking.html')

def b_cash(request):
    
    return render(request, 'front/b-cash.html')

def b_credit(request):
    
    return render(request, 'front/b-credit.html')

def b_wire(request):
    
    return render(request, 'front/b-wire.html')

def b_foreign(request):
    
    return render(request, 'front/b-foreign.html')

def c_solutions(request):
    
    return render(request, 'front/c-solutions.html')

def c_expertise(request):
    
    return render(request, 'front/c-expertise.html')


def c_deals(request):
    
    return render(request, 'front/c-deals.html')

def i_phil(request):
    
    return render(request, 'front/i-phil.html')

def i_outlook(request):
    
    return render(request, 'front/i-outlook.html')

def i_solutions(request):
    
    return render(request, 'front/i-solutions.html')


























def handler400(request, exception):
    return render(request, 'front/page-error-400.html', status=400)


def handler403(request, exception):
    return render(request, 'front/page-error-403.html', status=403)


def handler404(request, exception):
    return render(request, 'front/page-error-404.html', status=404)

    
def handler500(request):
    return render(request, 'front/page-error-500.html', status=500)