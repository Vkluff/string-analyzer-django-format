from django.contrib import admin
from .models import AnalyzedString

# Register your models here.
@admin.register(AnalyzedString)
class AnalyzedStringAdmin(admin.ModelAdmin):
    list_display = ('id', 'value', 'length', 'is_palindrome', 'word_count', 'sha_256_hash')
    search_fields = ('value', 'id', 'sha_256_hash')
    list_filter = ('id', 'sha_256_hash', 'created_at', 'updated_at')

    def value_preview(self, obj):
        return obj.value[:50] + '...' if len(obj.value) > 50 else obj.value

