from rest_framework import serializers

# from account.serializers import current_site
from .models import Shop

from account.models import User

from django.contrib.sites.models import Site

# current_site = Site.objects.get_current()

#--------------- Shop list Serializers ---------------#
class ShopsListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Shop
        fields = [
            "id",
            "username",
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
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields

#--------------- Shop Create Serializers ---------------#
class ShopCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='owner.username', read_only=True)
    email = serializers.CharField(source='owner.email', read_only=True)

    class Meta:
        model = Shop
        fields = [
            "id",
            "username",
            "email",
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
        ]
        read_only_fields = ["id", "username", "email"]

#--------------- Shop Update Serializers ---------------#
class ShopUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = [
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
        ]

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if "logo" in validated_data:
            instance.logo = validated_data["logo"]
            instance.save()
        if "cover_image" in validated_data:
            instance.cover_image = validated_data["cover_image"]
            instance.save()
        return instance

#--------------- Shop Detail Serializers ---------------#
class ShopDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Shop

        fields = [
            "id",
            "username",
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
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
