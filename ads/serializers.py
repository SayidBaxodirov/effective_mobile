from rest_framework import serializers
from .models import Ads, ExchangeProposal


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = '__all__'

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError('Title shoud be at least 3 characters long')
        return value

    def validate_description(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError('Description should be at least 10 characters long')
        return value


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeProposal
        fields = '__all__'
