from rest_framework import serializers


class BaseSerializer(serializers.Serializer):
    sender_id = serializers.CharField(required=True)
    receiver_id = serializers.CharField(required=True)


class ReceiverSerializer(serializers.Serializer):
    receiver_id = serializers.CharField(required=True)


class GetByIdSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)


class PaginationSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False, default=1, min_value=1, max_value=500)
    limit = serializers.IntegerField(required=False, default=10, min_value=1, max_value=500)


class FriendsSerializer(serializers.Serializer):
    @staticmethod
    def single_representation(instance):
        return {
            "id": instance['receiver_id'],
        }

    @classmethod
    def response(self, instance):
        return [self.single_representation(i) for i in instance]
