from rest_framework import serializers
from downbeats.models.subcategory import Subcategory


class SubcategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ["name", "description", "category", "subcategory", "thumbnail"]
        read_only_fields = ["created_at", "updated_at"]

    def create(self, validated_data):
        return Subcategory.objects.create(**validated_data)