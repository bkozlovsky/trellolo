from rest_framework import serializers
from mainapp.models import Card

class CardSerializer(serializers.ModelSerializer):

    class Meta:

        model = Card
        fields = ['id', 'name', 'description', 'creator', 'assignee', 'date', 'status']

class CardStatusSerializer(serializers.ModelSerializer):

    class Meta:

        model = Card
        fields = ['id', 'creator', 'assignee', 'date_edited']