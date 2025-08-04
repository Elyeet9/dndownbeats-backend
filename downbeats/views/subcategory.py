from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from downbeats.models.subcategory import Subcategory
from downbeats.serializers.subcategory import SubcategoryCreateSerializer


class SubcategoryDetailView(APIView):
    """
    View to retrieve a single subcategory by ID.
    """

    def get(self, request, pk, *args, **kwargs):
        try:
            subcategory = Subcategory.objects.get(pk=pk)
            parent_name = ""
            parent = subcategory.subcategory
            while parent:
                parent_name = f'{parent.name} / {parent_name}' 
                parent = parent.subcategory
            parent_name = parent_name.rstrip(" / ")

            response = {
                'id': subcategory.id,
                'name': subcategory.name,
                'description': subcategory.description,
                'category': subcategory.category.id,
                'category_name': subcategory.category.name,
                'thumbnail': subcategory.thumbnail.url if subcategory.thumbnail else None,
                'subcategory': subcategory.subcategory.id if subcategory.subcategory else None,
                'subcategories': [
                    {
                        'id': child.id,
                        'name': child.name,
                        'description': child.description,
                        'thumbnail': child.thumbnail.url if child.thumbnail else None
                    } for child in subcategory.child_subcategories.all()
                ],
                'soundtracks': [
                    {
                        'id': soundtrack.id,
                        'title': soundtrack.title,
                        'description': soundtrack.description,
                        'url': soundtrack.url,
                        'thumbnail': soundtrack.thumbnail.url if soundtrack.thumbnail else None
                    } for soundtrack in subcategory.soundtracks.all()
                ],
                'parent_name': parent_name
            }

            return Response(response, status=status.HTTP_200_OK)
        except Subcategory.DoesNotExist:
            return Response({"error": "Subcategory not found"}, status=status.HTTP_404_NOT_FOUND)
        

class SubcategoryCreateView(APIView):
    """
    View to create a new subcategory.
    """

    def post(self, request, *args, **kwargs):
        serializer = SubcategoryCreateSerializer(data=request.data)
        if serializer.is_valid():
            subcategory = serializer.save()
            return Response({"id": subcategory.id, "name": subcategory.name}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)