from rest_framework import serializers
from downbeats.models.category import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ["created_at", "updated_at"]


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "description", "thumbnail"]
        read_only_fields = ["created_at", "updated_at"]

    def create(self, validated_data):
        return Category.objects.create(**validated_data)
    