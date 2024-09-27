from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser, Farmer, Consumer, FarmerAndConsumerLink

class UserAdmin(BaseUserAdmin):
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_farmer', 'is_consumer')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_farmer', 'is_consumer','is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'is_farmer', 'is_consumer')
    
    
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('get_email', 'get_first_name', 'get_last_name', 'revenue')

    readonly_fields = ('get_email', 'get_first_name', 'get_last_name', 'get_phone_number', 'get_last_login', 'revenue')
    
    fieldsets = (
        (None, {'fields': ('get_email',)}),
        (_('Personal info'), {'fields': ('get_first_name', 'get_last_name', 'get_phone_number')}),
        (_('Selling'), {'fields': ('revenue',)}),
        (_('Important dates'), {'fields': ('get_last_login',)}),
    )

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Last Name'
    
    def get_phone_number(self, obj):
        return obj.user.phone
    get_last_name.short_description = 'Phone Number'
    
    def get_last_login(self, obj):
        return obj.user.last_login
    get_last_login.short_description = 'Last Login'

admin.site.register(Farmer, FarmerAdmin)  
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Consumer)
admin.site.register(FarmerAndConsumerLink)

