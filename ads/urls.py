from django.urls import path, include
from rest_framework import routers
from .views import AdViewSet, logout_view, ExchangeProposalViewSet

router = routers.DefaultRouter()
router.register(r'ads', AdViewSet)
router.register(r'proposals',ExchangeProposalViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('logout/', logout_view, name='logout'),
]
