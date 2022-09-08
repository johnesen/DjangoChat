from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import User

# admin.site.register(User)
# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'photo', 'is_superuser', 'is_staff', 'is_active', 'last_active')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)