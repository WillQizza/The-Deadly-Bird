from rest_framework import serializers
from .models import Ad

class AdSerializer(serializers.ModelSerializer):
  type = serializers.CharField(read_only=True, default="ad")
  contentType = serializers.CharField(source="content_type")
  company = serializers.CharField()
    
  class Meta:
    model = Ad
    fields = ['type', 'title', 'id', 'description', 'contentType', 'content', 'company']