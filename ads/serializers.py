from rest_framework import serializers
from .models import Ads, ExchangeProposal


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = '__all__'
        read_only_fields = ['user']

    def validate_title(self, value):
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError('Title shoud be at least 3 characters long')
        return value

    def validate_description(self, value):
        if not value or len(value.strip()) < 10:
            raise serializers.ValidationError('Description should be at least 10 characters long')
        return value


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeProposal
        fields = '__all__'

    def validate_comment(self, value):
        if not value or len(value.strip()) < 5:
            raise serializers.ValidationError('Comment should be at least 5 characters long.')
        return value
