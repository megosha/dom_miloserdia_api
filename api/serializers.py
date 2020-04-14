from rest_framework.serializers import ModelSerializer

from api import models


class PartnerSerializer(ModelSerializer):
    class Meta:
        model = models.Partner
        fields = "__all__"
