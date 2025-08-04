from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from downbeats.models.category import Category
from downbeats.models.subcategory import Subcategory


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
        data = request.data.copy()
        # Get all required fields from the request data
        request_name = data['name']
        request_description = data.get('description', '')
        request_category = data.get('category')
        category = Category.objects.filter(pk=request_category).first()
        if not category:
            return Response({"error": "Category not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Get the optional fields
        request_subcategory = data.get('subcategory', None)
        subcategory = Subcategory.objects.filter(pk=request_subcategory).first() if request_subcategory else None
        request_thumbnail = data.get('thumbnail', None)

        # Try to create the subcategory
        try:
            subcategory = Subcategory.objects.create(
                name=request_name,
                description=request_description,
                category=category,
                subcategory=subcategory,
                thumbnail=request_thumbnail
            )
            return Response({"id": subcategory.id, "name": subcategory.name}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)