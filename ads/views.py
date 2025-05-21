from django.shortcuts import render
from rest_framework import viewsets
from .models import Ads, ExchangeProposal

from .serializers import AdSerializer, ProposalSerializer


# Create your views here.
class AdViewSet(viewsets.ModelViewSet):
    queryset = Ads.objects.all()
    serializer_class = AdSerializer
    permission_classes = []
    #continue from here
