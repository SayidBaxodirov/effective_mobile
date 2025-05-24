import django_filters
from .models import Ads, ExchangeProposal


class AdsFilter(django_filters.FilterSet):
    class Meta:
        model = Ads
        fields = ['category', 'condition']


class ProposalFilter(django_filters.FilterSet):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'ad_receiver', 'status']
