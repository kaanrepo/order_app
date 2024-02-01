from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import  UserAdminCreationForm, UserAdminChangeForm
from .models import User


# Register your models here.


User = get_user_model()

class CustomUserAdmin(UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    model = User
    list_display = ('username',)
    list_filter = ('username',)
    filter_horizontal = ()

    fieldsets = (
        (None, {'fields': ('username',)}),
        ('Permissions', {'fields': ('staff', 'superuser', 'active', 'groups', 'user_permissions')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
        ),
    )

    search_fields = ('username',)



admin.site.register(User, CustomUserAdmin)
