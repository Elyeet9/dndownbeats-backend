from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from downbeats.models.category import Category
from downbeats.serializers.category import CategorySerializer


class CategoryListView(APIView):
    """
    View to list all categories.
    """

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CategoryDetailView(APIView):
    """
    View to retrieve a single category by ID.
    """

    def get(self, request, pk, *args, **kwargs):
        try:
            category = Category.objects.get(pk=pk)
            # Get related top-level subcategories
            subcategories = category.subcategories.filter(subcategory__isnull=True)
            # Get all top-level soundtracks in the category
            soundtracks = category.soundtracks.filter(subcategory__isnull=True)
            response = {
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'thumbnail': category.thumbnail.url if category.thumbnail else None,
                'subcategories': [
                    {
                        'id': subcategory.id,
                        'name': subcategory.name,
                        'description': subcategory.description,
                        'thumbnail': subcategory.thumbnail.url if subcategory.thumbnail else None
                    } for subcategory in subcategories
                ],
                'soundtracks': [
                    {
                        'id': soundtrack.id,
                        'title': soundtrack.title,
                        'description': soundtrack.description,
                        'url': soundtrack.url,
                        'thumbnail': soundtrack.thumbnail.url if soundtrack.thumbnail else None
                    } for soundtrack in soundtracks
                ]
            }
            return Response(response, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)