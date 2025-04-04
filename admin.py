from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Customer
from .models import *


class CustomerInline(admin.StackedInline):
    model = Customer
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (CustomerInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Customer)

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)