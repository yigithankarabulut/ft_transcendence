from rest_framework import serializers
from .models import ImageModel


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ['image']

    def bind(self, data):
        return ImageModel(user_id=data['user_id'], image=data['image'])