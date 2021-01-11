from rest_framework import serializers
from racedata.models import Pilot

class PilotSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Pilot
        fields = ['name', 'total_time', 'total_pts']