from rest_framework import serializers


class CallsignSerializer(serializers.Serializer):
    callsign = serializers.CharField(max_length=200)


class PasscodeSerializer(serializers.Serializer):
    passcode = serializers.CharField(max_length=200)
