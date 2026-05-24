import re
from urllib.parse import urlparse, parse_qs

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from downbeats.models.category import Category
from downbeats.models.subcategory import Subcategory
from downbeats.models.soundtrack import Soundtrack


def _extract_youtube_id(url):
    """Return the 11-char YouTube video ID for any common YouTube URL form, or None."""
    try:
        parsed = urlparse(url)
    except Exception:
        return None
    host = (parsed.hostname or "").lower().lstrip("www.")
    if host == "youtu.be":
        vid = parsed.path.lstrip("/").split("/")[0]
        return vid if re.fullmatch(r"[A-Za-z0-9_-]{11}", vid) else None
    if host in ("youtube.com", "m.youtube.com", "music.youtube.com"):
        if parsed.path == "/watch":
            vid = parse_qs(parsed.query).get("v", [None])[0]
            return vid if vid and re.fullmatch(r"[A-Za-z0-9_-]{11}", vid) else None
        m = re.match(r"^/(?:shorts|embed|v)/([A-Za-z0-9_-]{11})", parsed.path)
        if m:
            return m.group(1)
    return None


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
            try:
                import requests
                from django.core.files.base import ContentFile
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                    "Accept-Language": "en-US,en;q=0.9",
                }

                youtube_id = _extract_youtube_id(request_url)
                if youtube_id:
                    # Title via YouTube's public oEmbed endpoint (no auth, no HTML scraping)
                    if not request_title:
                        oembed_resp = requests.get(
                            "https://www.youtube.com/oembed",
                            params={"url": f"https://www.youtube.com/watch?v={youtube_id}", "format": "json"},
                            headers=headers,
                            timeout=10,
                        )
                        if oembed_resp.status_code == 200:
                            request_title = oembed_resp.json().get("title") or "Unknown Title"
                        else:
                            return Response(
                                {"error": f"Failed to fetch YouTube oEmbed: HTTP {oembed_resp.status_code}"},
                                status=status.HTTP_400_BAD_REQUEST,
                            )
                    # Thumbnail directly from the public i.ytimg.com pattern; fall back through qualities.
                    if not request_thumbnail:
                        thumb_content = None
                        for quality in ("maxresdefault", "hqdefault", "mqdefault", "default"):
                            thumb_resp = requests.get(
                                f"https://img.youtube.com/vi/{youtube_id}/{quality}.jpg",
                                headers=headers,
                                timeout=10,
                            )
                            if thumb_resp.status_code == 200 and thumb_resp.content:
                                thumb_content = thumb_resp.content
                                break
                        if thumb_content is None:
                            return Response(
                                {"error": "Failed to download YouTube thumbnail"},
                                status=status.HTTP_400_BAD_REQUEST,
                            )
                        safe_title = "".join(c for c in request_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                        request_thumbnail = ContentFile(thumb_content, name=f"{safe_title[:50] or youtube_id}.jpg")
                else:
                    # Non-YouTube URL: fall back to Open Graph scraping.
                    from bs4 import BeautifulSoup
                    resp = requests.get(request_url, headers=headers, timeout=10)
                    if resp.status_code != 200:
                        return Response(
                            {"error": f"Failed to fetch page: HTTP {resp.status_code}"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    if not request_title:
                        title_tag = soup.find('meta', property='og:title')
                        request_title = title_tag['content'] if title_tag else 'Unknown Title'
                    if not request_thumbnail:
                        thumb_tag = soup.find('meta', property='og:image')
                        thumbnail_url = thumb_tag['content'] if thumb_tag else None
                        if not thumbnail_url:
                            return Response({"error": "No thumbnail URL found for this page"}, status=status.HTTP_400_BAD_REQUEST)
                        thumb_resp = requests.get(thumbnail_url, headers=headers, timeout=10)
                        if thumb_resp.status_code != 200:
                            return Response({"error": "Failed to download thumbnail"}, status=status.HTTP_400_BAD_REQUEST)
                        safe_title = "".join(c for c in request_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                        request_thumbnail = ContentFile(thumb_resp.content, name=f"{safe_title[:50]}.jpg")
            except Exception as e:
                return Response({"error": f"Metadata fetch failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

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
