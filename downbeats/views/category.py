from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from downbeats.models.category import Category
from downbeats.serializers.category import CategorySerializer, CategoryCreateSerializer


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
        
    def put(self, request, pk, *args, **kwargs):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategoryCreateSerializer(category, data=request.data)
            if serializer.is_valid():
                updated_category = serializer.save()
                return Response({"id": updated_category.id, "name": updated_category.name}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        

class CategoryCreateView(APIView):
    """
    View to create a new category.
    """

    def post(self, request, *args, **kwargs):
        serializer = CategoryCreateSerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()
            return Response({"id": category.id, "name": category.name}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class CategoryDeleteView(APIView):
    """
    View to delete a category by ID.
    """

    def get(self, request, pk, *args, **kwargs):
        try:
            category = Category.objects.get(pk=pk)
            subcategories_count = category.subcategories.count()
            soundtracks_count = category.soundtracks.count()
            return Response({
                'subcategories_count': subcategories_count,
                'soundtracks_count': soundtracks_count,
            }, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, *args, **kwargs):
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response({"message": "Category deleted successfully"}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)