from rest_framework import serializers
from .models import AnalyzedString

class AnalyzedStringSerializer(serializers.ModelSerializer):
    properties = serializers.SerializerMethodField()
    
    class Meta:
        model = AnalyzedString
        fields = [
            'id',
            'value',
            'properties',   
            'created_at',
        ]

    def get_properties(self, obj):
        return {
            'length': obj.length,
            'is_palindrome': obj.is_palindrome,
            'unique_characters': obj.unique_characters,
            'word_count': obj.word_count,
            'sha_256_hash': obj.sha_256_hash,
            'character_frequency_map': obj.character_frequency_map,
            'updated_at': obj.updated_at, 
            }
    
class StringInputSerializer(serializers.Serializer):
    value = serializers.CharField(min_length=1, max_length=10000)
    
        

