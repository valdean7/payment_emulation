from django.contrib import admin
from .models import Account, Card


class AccountAdmin(admin.ModelAdmin):
    model = Account
    readonly_fields = ['account_number', 'balance']


class CardAdmin(admin.ModelAdmin):
    model = Card
    readonly_fields = ['cvv', 'card_number', 'validity']


    def get_readonly_fields(self, request, obj=None):
        readonly =  list(super().get_readonly_fields(request, obj))

        if obj:
            readonly.append('pin')

        return readonly


admin.site.register(Account, AccountAdmin)
admin.site.register(Card, CardAdmin)
