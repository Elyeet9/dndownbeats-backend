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
            # Download the title and thumbnail from the URL using BeautifulSoup
            try:
                import requests
                from bs4 import BeautifulSoup
                from django.core.files.base import ContentFile
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
                }
                resp = requests.get(request_url, headers=headers, timeout=10)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    # Get title
                    if not request_title:
                        title_tag = soup.find('meta', property='og:title')
                        request_title = title_tag['content'] if title_tag else 'Unknown Title'
                    # Get thumbnail
                    if not request_thumbnail:
                        thumb_tag = soup.find('meta', property='og:image')
                        thumbnail_url = thumb_tag['content'] if thumb_tag else None
                        if thumbnail_url:
                            thumb_resp = requests.get(thumbnail_url, headers=headers, timeout=10)
                            if thumb_resp.status_code == 200:
                                safe_title = "".join(c for c in request_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                                request_thumbnail = ContentFile(thumb_resp.content, name=f"{safe_title[:50]}.jpg")
                            else:
                                return Response({"error": "Failed to download thumbnail from video (fallback)"}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({"error": "No thumbnail URL found for this video (fallback)"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"error": "Failed to fetch YouTube page (fallback)"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": f"yt-dlp and fallback both failed: {str(e)} | {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

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
