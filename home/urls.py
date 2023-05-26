from django.urls import path, include
from django.views.decorators.cache import cache_page
from .views import (
    index,
    aboutus,
    mission,
    career,
    expectation,
    contactus,
    p_checking,
    p_savings,
    p_cards,
    p_invest,
    p_retire,
    p_mortgage,
    p_auto,
    b_checking,
    b_cash,
    b_credit,
    b_foreign,
    b_wire,
    c_solutions,
    c_deals,
    c_expertise,
    i_outlook,
    i_phil,
    i_solutions,
    home

    )



urlpatterns = [
    path('', home, name='home'),
    path('in/', index, name='index'),
    path('in/Who-We-Are/', aboutus, name='aboutus'),
    path('in/Our-Mission-and-Vision/', mission, name='mission'),
    path('in/Careers-At-Barclays/', career, name='career'),
    path('in/Service-Expectation/', expectation, name='expectation'),
    path('in/contact-us/', contactus, name='contactus'),
    path('in/personal-banking/checking/', p_checking, name='p_checking'),
    path('in/personal-banking/savings/', p_savings, name='p_savings'),
    path('in/personal-banking/credit-cards/', p_cards, name='p_cards'),
    path('in/personal-banking/investments/', p_invest, name='p_invest'),
    path('in/personal-banking/retirement/', p_retire, name='p_retire'),
    path('in/personal-banking/mortgages/', p_mortgage, name='p_mortgage'),
    path('in/personal-banking/auto-loans/', p_auto, name='p_auto'),


    # business
    path('in/business/checking/', b_checking, name='b_checking'),
    path('in/business/cash-management/', b_cash, name='b_cash'),
    path('in/business/credit-&-financing/', b_credit, name='b_credit'),
    path('in/business/international-wire-transfer/', b_wire, name='b_wire'),
    path('in/business/foreign-currency-exchange/', b_foreign, name='b_foreign'),

    # commercial
    path('in/commercial/solutions/', c_solutions, name='c_solutions'),
    path('in/commercial/deals/', c_deals, name='c_deals'),
    path('in/commercial/expertise/', c_expertise, name='c_expertise'),

    # investment
    path('in/investment/market-outlook/', i_outlook, name='i_outlook'),
    path('in/investment/philosophy/', i_phil, name='i_phil'),
    path('in/investment/solutions/', i_solutions, name='i_solutions'),
    
   
]