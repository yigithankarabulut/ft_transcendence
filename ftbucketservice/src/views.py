from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
import requests
from ftbucketservice.settings import SERVICE_ROUTES
from django.http import HttpResponse
import os
from .models import ImageModel
from .serializers import ImageSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        access_token = request.headers.get('Authorization')
        if not access_token.split(' ')[0] == 'Bearer':
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        access_token = access_token.split(' ')[1]
        try:
            response = requests.post(f"{SERVICE_ROUTES['/auth']}/auth/token/validate", headers={'Authorization': f'Bearer {access_token}'})
        except requests.exceptions.RequestException as e:
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if response.status_code != 200:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        res = response.json()
        id = res['user_id']
        if not id:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            image = get_object_or_404(ImageModel, user_id=id)
            if image:
                image.delete()
                os.remove(image.image.path)
        except:
            pass
        image = serializer.bind({'user_id': id, 'image': request.data['image']})
        image.save()
        return Response({'message': 'Image uploaded successfully'}, status=status.HTTP_201_CREATED)

    def image_serve(self, request):
        id = request.query_params.get('id')
        if not id:
            return Response({'error': 'Id is required'}, status=status.HTTP_400_BAD_REQUEST)

        image = get_object_or_404(ImageModel, user_id=id)
        with open(image.image.path, 'rb') as img:
            return HttpResponse(img.read(), content_type='image/jpeg')
