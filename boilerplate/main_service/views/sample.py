from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response


class SampleView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        data = {'foo': 'bar!'}
        return Response(data)
