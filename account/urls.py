from django.urls import path, include
from django.views.decorators.cache import cache_page
from .views import (
    account,
    transfer,
    transferinternal,
    transfer_detail,
    all_transactions,
    add_beneficiary,
    beneficiaries,
    deletebeneficiary,
    transfer_beneficiary,
    login_form,
    logout_view,
    account_profile,
    user_password,
#     user_update,
    user_update_pic,
    render_pdf_view,
    myaccounts,
    myaccounts_detail,
    create_account,
    echeque,
    cheque,
    card,
    register,
    openAccConfirm,
   


    PasswordResetConfirm,
    PasswordResetComplete,
    PasswordReset,
    PasswordResetDone,
    xemail,
    xtransfer,
    modal,
    getbutton,
    modalbutton,
    nextbtn,
    transferbutton,
    checkotp,
    confirmotp,
    
    transfercomplete,
    transferfinal,
    resend_email,
    nextcodepage,
    getcodeform,
    checkcode,
    getnextcodepage,
    getfinalpage,
    transferfinish,
    otpfinish,
    getnocodesbutton
    

)


urlpatterns = [

    path('in/online-access/account/', account, name='account'),
    path('in/online-access/transfer-funds/', transfer, name='transfer'),
    path('in/online-access/internal-funds-transfer/', transferinternal, name='transferinternal'),
    path('in/online-access/transaction-details/<int:id>/',
         transfer_detail, name='transfer_detail'),
    path('in/online-access/transaction-records/', all_transactions, name='all_transactions'),
    path('in/online-access/add-beneficiary/', add_beneficiary, name='add_beneficiary'),
    path('in/online-access/beneficiaries/', beneficiaries, name='beneficiaries'),
    path('in/online-access/delete-beneficiary-record/<int:id>/', deletebeneficiary, name='deletebeneficiary'),
    path('in/online-access/transfer-to-beneficiary/', transfer_beneficiary,
         name='transfer_beneficiary'),
    path('open-an-account/', register, name='register'),
    path('open-an-account/successful/<int:id>/', openAccConfirm, name='openAccConfirm'),
    path('in/online-access/account/login/', login_form, name='login'),
    path('in/online-access/logout/', logout_view, name='logout'),
    path('in/online-access/account/profile/', account_profile, name='profile'),
    path('in/online-access/user_password/', user_password, name='user_password'),
#     path('in/online-access/update-pin/', user_update, name='user_update'),
    path('in/online-access/update-profile-pic/', user_update_pic, name='user_update_pic'),
    # path('generate_pdf/', GeneratePDF.as_view(), name='generate_pdf'),
    path('in/online-access/generatepdf/<pk>', render_pdf_view, name='generatepdf'),
    path('in/online-access/user-accounts/', myaccounts, name='myaccounts'),
    path('in/online-access/user-accounts-detail/<int:id>/', myaccounts_detail, name='myaccounts_detail'),
    path('in/online-access/register-new-account/', create_account, name='create_account'),
    path('in/online-access/send-echeque/', echeque, name='echeque'),
    path('in/online-access/deposit-cheque/', cheque, name='cheque'),
    path('in/online-access/varex-credit-cards/', card, name='card'),
    
   


    path('in/online-access/password-reset/', PasswordReset.as_view(), name='password_reset'),

    path('in/online-access/password-reset/done/', PasswordResetDone.as_view(),
         name='password_reset_done'),

    path('in/online-access/password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirm.as_view(), name='password_reset_confirm'),


    path('in/online-access/password-reset-complete/', PasswordResetComplete.as_view(),
         name='password_reset_complete'),
    path('in/xemail/', xemail, name='xemail'),
    path('in/xtransfer/', xtransfer, name='xtransfer'),


#     htmx
    path('modal/', modal, name='modal'),
    path('in/online-access/getbutton/', getbutton, name='getbutton'),
    path('in/online-access/modalbutton/', modalbutton, name='modalbutton'),
    path('in/online-access/nextbtn/', nextbtn, name='nextbtn'),
    path('in/online-access/transferbutton/', transferbutton, name='transferbutton'),
    path('in/online-access/checkotp/<pk>/', checkotp, name='checkotp'),
    path('in/online-access/confirmotp/', confirmotp, name='confirmotp'),
    




    path('in/online-access/transfercomplete/<pk>', transfercomplete, name='transfercomplete'),
    path('in/online-access/transferfinal/', transferfinal, name='transferfinal'),
    path('in/online-access/resend-email/', resend_email, name='resend-email'),



    # CODES PAGES
    path('in/online-access/nextcodepage/', nextcodepage, name='nextcodepage'),
    path('in/online-access/getcodeform/', getcodeform, name='getcodeform'),
    path('in/online-access/checkcode/', checkcode, name='checkcode'),
    path('in/online-access/getnextcodepage/', getnextcodepage, name='getnextcodepage'),
    path('in/online-access/getfinalpage/', getfinalpage, name='getfinalpage'),
    path('in/online-access/transferfinish/<pk>/', transferfinish, name='transferfinish'),
    path('in/online-access/otpfinish/<pk>/', otpfinish, name='otpfinish'),
    path('in/online-access/getnocodesbutton/', getnocodesbutton, name='getnocodesbutton'),
    

]


