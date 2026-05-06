from django.contrib import admin
from .models import User, Profile


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_verified')
    list_filter = ('role', 'is_active', 'is_verified')
    search_fields = ('username', 'email')
    ordering = ('username',)


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Profile)
