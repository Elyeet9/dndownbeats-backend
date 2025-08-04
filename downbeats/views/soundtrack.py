from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class SoundtrackCreateView(APIView):
    """
    View to handle the creation of soundtracks.
    """

    def post(self, request):
        serializer = SoundtrackCreateSerializer(data=request.data)
        if serializer.is_valid():
            soundtrack = serializer.save()
            return Response({"message": "Soundtrack created successfully", "id": soundtrack.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)