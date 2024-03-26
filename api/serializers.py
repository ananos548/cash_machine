from rest_framework.serializers import ModelSerializer
from api.models import Item


class ItemSerializer(ModelSerializer):

    class Meta:
        model = Item
        fields = ('id', 'title', 'price')
