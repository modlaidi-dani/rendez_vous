from rest_framework import serializers
from .models import *
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields="__all__"
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model=Company
        fields="__all__"
class BreakTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Break_time
        fields="__all__"
    def validate(self, data):
        start_time=data.get('start_time_break')
        end_time=data.get('end_time_break')
        if end_time<=start_time:
            raise serializers.ValidationError('Tcheck your time ')
        return super().validate(data)        
class ProgrammeSerializer(serializers.ModelSerializer):
    breaks_time=BreakTimeSerializer(many=True,read_only=True)
    class Meta:
        model=Programme
        fields="__all__"
    def validate(self, data):
        start_time=data.get('start_time')
        end_time=data.get('end_time')
        if end_time<=start_time:
            raise serializers.ValidationError('End time must be after start time.')
        return super().validate(data)        
class ServiceSerializer(serializers.ModelSerializer):
    programmes=ProgrammeSerializer(many=True, read_only=True)
    breaks_time=BreakTimeSerializer(many=True,read_only=True)
    class Meta:
        model=Service
        fields="__all__"
    def validate(self, data):
        treatment_time=data.get('time_treatment')
        waiting_time=data.get('waiting_time')
        if waiting_time>=treatment_time:
            raise serializers.ValidationError('Tcheck your treatment time and waiting time')
        return super().validate(data)