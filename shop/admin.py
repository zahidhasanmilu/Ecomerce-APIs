from django.contrib import admin
from .models import Shop
from django import forms
from django.core.exceptions import ValidationError


# Register your models here.
class ShopAdminForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = [
            "owner",
            "name",
            "tagline",
            "description",
            "logo",
            "cover_image",
            "contact_email",
            "contact_phone",
            "address",
            "policies",
            "settings",
            "status",
            "is_verified",
        ]

    def clean_owner(self):
        owner = self.cleaned_data.get('owner')

        ALLOWED_ROLES = ['shop_owner']

        if owner and owner.role not in ALLOWED_ROLES:
            error_message = (
                f"The owner's email ({owner.email}) has the role '{owner.role}'. "
                f"The owner must have the role '{ALLOWED_ROLES[0]}' "
                f"for shop creation/update."
            )
            raise ValidationError(error_message)

        return owner


class ShopAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'get_owner_role',
        'get_owner_email',
        'is_verified',
    )
    list_filter = ('is_verified',)
    search_fields = ('name', 'owner__username')

    form = ShopAdminForm

    def get_owner_role(self, obj):
        return obj.owner.role

    get_owner_role.short_description = 'Owner Role'

    def get_owner_email(self, obj):
        return obj.owner.email

    get_owner_email.short_description = 'Owner Email'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


# register admin
admin.site.register(Shop, ShopAdmin)
