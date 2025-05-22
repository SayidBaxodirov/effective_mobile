from django.http import Http404
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.exceptions import NotFound

from .models import Ads, ExchangeProposal

from .serializers import AdSerializer, ProposalSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly


# Create your views here.
class AdViewSet(viewsets.ModelViewSet):
    queryset = Ads.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # filter and search logic
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'condition']
    search_fields = ['title', 'description']

    # function that will check if the object exists and display specific message if error
    def get_object(self):
        try:
            obj = super().get_object()
        except Http404:
            raise NotFound(detail="Данное объявление не существует.")
        return obj

    def perform_create(self, serializer):
        print("Authenticated user:", self.request.user)
        serializer.save(user=self.request.user)
