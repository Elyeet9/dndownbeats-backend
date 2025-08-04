from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from downbeats.models.category import Category
from downbeats.models.subcategory import Subcategory
from downbeats.models.soundtrack import Soundtrack


class SoundtrackCreateView(APIView):
    """
    View to handle the creation of soundtracks.
    """

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        # Get all required fields from the request data
        request_title = data['title']
        request_description = data.get('description', '')
        request_category = data.get('category')
        category = Category.objects.filter(pk=request_category).first()
        if not category:
            return Response({"error": "Category not found"}, status=status.HTTP_400_BAD_REQUEST)
        request_url = data.get('url')

        # Get the optional fields
        request_subcategory = data.get('subcategory', None)
        subcategory = Subcategory.objects.filter(pk=request_subcategory).first() if request_subcategory else None
        request_thumbnail = data.get('thumbnail', None)

        # Try to create the subcategory
        try:
            soundtrack = Soundtrack.objects.create(
                title=request_title,
                description=request_description,
                category=category,
                subcategory=subcategory,
                thumbnail=request_thumbnail,
                url=request_url
            )
            return Response({"id": soundtrack.id, "name": soundtrack.title}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)