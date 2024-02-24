from rest_framework import serializers

class BaseSerializer(serializers.Serializer):
    sender_id = serializers.IntegerField(min_value=1, required=True)
    receiver_id = serializers.IntegerField(min_value=1, required=True)

class GetByIdSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1, required=True)

class PaginationSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False, default=1, min_value=1, max_value=500)
    limit = serializers.IntegerField(required=False, default=10, min_value=1, max_value=500)

class FriendsSerializer(serializers.Serializer):
    def single_representation(self, instance):
        return {
            "id": instance.id,
            "username": instance.username,
        }

    def response(self, instance):
        arr = []
        for i in instance:
            arr.append(self.single_representation(i))
        return arr
