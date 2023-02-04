from rest_framework import serializers

from tournament.models import Participant, Tournament

class TournamentSerializer(serializers.ModelSerializer):

    class Meta :
        model = Tournament

        fields = '__all__'

class ParticipantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participant

        fields = '__all__'