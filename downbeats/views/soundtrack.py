from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from downbeats.models.category import Category
from downbeats.models.subcategory import Subcategory
from downbeats.models.soundtrack import Soundtrack


class SoundtrackDetailView(APIView):
    """
    View to retrieve a single soundtrack by ID.
    """

    def put(self, request, pk, *args, **kwargs):
        try:
            soundtrack = Soundtrack.objects.get(pk=pk)
            data = request.data.copy()
            soundtrack.title = data.get('title', soundtrack.title)
            soundtrack.description = data.get('description', soundtrack.description)
            soundtrack.thumbnail = data.get('thumbnail', soundtrack.thumbnail)
            soundtrack.url = data.get('url', soundtrack.url)

            soundtrack.save()
            return Response({"id": soundtrack.id, "title": soundtrack.title}, status=status.HTTP_200_OK)
        except Soundtrack.DoesNotExist:
            return Response({"error": "Soundtrack not found"}, status=status.HTTP_404_NOT_FOUND)


class SoundtrackCreateView(APIView):
    """
    View to handle the creation of soundtracks.
    """

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        # Get all required fields from the request data
        request_title = data.get('title', None)
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

        if request_url and not (request_title and request_thumbnail):
            # Download the title and thumbnail from the URL using yt-dlp
            try:
                import yt_dlp
                import requests
                from django.core.files.base import ContentFile
                
                # Configure yt-dlp options
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'extract_flat': False,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Extract video info
                    info = ydl.extract_info(request_url, download=False)
                    
                    # Get title if not provided
                    if not request_title:
                        request_title = info.get('title', 'Unknown Title')
                    
                    # Get thumbnail if not provided
                    if not request_thumbnail:
                        thumbnail_url = info.get('thumbnail')
                        if thumbnail_url:
                            response = requests.get(thumbnail_url, timeout=10)
                            if response.status_code == 200:
                                # Clean the filename
                                safe_title = "".join(c for c in request_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                                request_thumbnail = ContentFile(response.content, name=f"{safe_title[:50]}.jpg")
                            else:
                                return Response({"error": "Failed to download thumbnail from video"}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({"error": "No thumbnail URL found for this video"}, status=status.HTTP_400_BAD_REQUEST)
                        
            except ImportError:
                return Response({"error": "yt-dlp is not installed. Please install it with: pip install yt-dlp"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                return Response({"error": f"Failed to fetch video data: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate required fields
        if not request_title:
            return Response({"error": "Title is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not request_url:
            return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Try to create the soundtrack
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
        

class SoundtrackDeleteView(APIView):
    """
    View to handle the deletion of soundtracks.
    """

    def delete(self, request, pk, *args, **kwargs):
        try:
            soundtrack = Soundtrack.objects.get(pk=pk)
            soundtrack.delete()
            return Response({"message": "Soundtrack deleted successfully"}, status=status.HTTP_200_OK)
        except Soundtrack.DoesNotExist:
            return Response({"error": "Soundtrack not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        