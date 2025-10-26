from django.db import models

# Create your models here.
class AnalyzedString(models.Model):
    id = models.CharField(max_length=64, primary_key=True)  # Use SHA hash as ID
    value = models.TextField()
    length = models.IntegerField()
    is_palindrome = models.BooleanField()
    unique_characters = models.IntegerField()
    word_count = models.IntegerField()
    sha_256_hash = models.CharField(max_length=64, unique=True)
    character_frequency_map = models.JSONField()

    # Date/Time field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Analyzed string'
        verbose_name_plural = 'Analyzed strings'

    def __str__(self):
        return f'String: {self.value[:50]}'


    

