from django.contrib import admin # type: ignore

# Register your models here.
from django.contrib.auth.admin import UserAdmin # type: ignore

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('name', 'email', 'is_staff', 'is_active', 'date_joined', 'sent_verification_email', 'verified_email')
    list_filter = ('name', 'email', 'is_staff', 'is_active', 'date_joined', 'sent_verification_email', 'verified_email')

    fieldsets = (
        (None, {'fields': ('name', 'email', 'password', 'date_joined', 'sent_verification_email', 'verified_email')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)