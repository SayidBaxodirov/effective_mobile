from django.http import Http404
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.exceptions import NotFound

from .models import Ads, ExchangeProposal

from .serializers import AdSerializer, ProposalSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from .filters import AdsFilter, ProposalFilter


@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect('/')


# Create your views here.
class AdViewSet(viewsets.ModelViewSet):
    queryset = Ads.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # filter and search logic
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = AdsFilter
    search_fields = ['title', 'description']

    # function that will check if the object exists and display specific message if error
    def get_object(self):
        try:
            obj = super().get_object()
        except Http404:
            raise NotFound(detail="Данное объявление не существует.")
        return obj

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExchangeProposalViewSet(viewsets.ModelViewSet):
    queryset = ExchangeProposal.objects.all().select_related('ad_sender', "ad_receiver").order_by('-created_at')
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # filter and search logic
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProposalFilter

    def perform_create(self, serializer):
        serializer.save()  # Don't alter or remove validated data


