from rest_framework import serializers

class GenericErrorSerializer(serializers.Serializer):
  error = serializers.BooleanField(default=True)
  message = serializers.CharField()

class GenericSuccessSerializer(serializers.Serializer):
  error = serializers.BooleanField(default=False)
  message = serializers.CharField()
