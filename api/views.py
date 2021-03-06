# from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api import serializers
from front import models


# Create your views here.

class Partners(ReadOnlyModelViewSet):
    #todo фильтровать по important и разбивать по блокам
    queryset = models.Partner.objects.all()
    serializer_class = serializers.PartnerSerializer