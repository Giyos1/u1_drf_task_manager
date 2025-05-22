from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    compression_ratio_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Image
        fields = [
            'id', 'title', 'original_image', 'compressed_image', 
            'compression_ratio', 'compression_ratio_display', 
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'compressed_image', 'compression_ratio', 'status', 
            'created_at', 'updated_at', 'compression_ratio_display'
        ]
    
    def get_compression_ratio_display(self, obj):
        if obj.compression_ratio is not None:
            return f"{obj.compression_ratio:.2f}%"
        return None


class ImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['title', 'original_image']
