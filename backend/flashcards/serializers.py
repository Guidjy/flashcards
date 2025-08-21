from rest_framework import serializers
from .models import Deck, Card, Activity, AccountabilityPartner


class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deck
        fields = '__all__'


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'
        

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'
        
        
class AccountabilityPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountabilityPartner
        fields = '__all__'