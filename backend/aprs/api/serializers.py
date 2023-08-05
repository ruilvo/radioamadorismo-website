"""
Serializers for the APRS API.

They seem useless but they help with schema generation.
"""

from rest_framework import serializers


class CallsignSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Serializer for the callsign.
    """

    callsign = serializers.CharField(max_length=200)


class PasscodeSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Serializer for the passcode.
    """

    passcode = serializers.CharField(max_length=200)
