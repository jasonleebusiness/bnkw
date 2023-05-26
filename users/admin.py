from django.contrib import admin

from .models import Userprofile, Transactions, Beneficiary, Echeque, Card

# Register your models here.


class UserprofileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'address', 'city', 'state', 'image_tag']


class TransactionAdmin(admin.ModelAdmin):
    # def get_queryset(self, request):
    #     qs = super(OrderAdmin, self).get_queryset(request)
    #     return qs.filter(ordered=True)

    list_display = ['amount', 'user',
                    'bank_acc', 'beneficiary', 'account', 'status']
    list_filter = ['status', 'user']
    readonly_fields = ('bill_count', 'confirm_code')
    # can_delete = False
    # inlines = [OrderFoodline]

admin.site.register(Userprofile, UserprofileAdmin)
admin.site.register(Transactions, TransactionAdmin)
admin.site.register(Beneficiary)
admin.site.register(Echeque)
admin.site.register(Card)
