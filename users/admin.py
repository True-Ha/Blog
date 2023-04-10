from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser

#William 456lkj654
#vjlink zxcvAsdf5233461

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['email', 'username', 'age']
    model = CustomUser

admin.site.register(CustomUser, CustomUserAdmin)