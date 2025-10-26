from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import AnalyzedString
from .serializers import AnalyzedStringSerializer, StringInputSerializer
from .utils import analyze_string

# Create your views here.
class StringViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for analyzing strings and retrieving analyzed strings.
    """
    queryset = AnalyzedString.objects.all() #first have to call your object/database
    serializer_class = AnalyzedStringSerializer #then serialize d data by calling d serializer
    def create(self, request):
        #Post /strings - create and analzye
        serializer = StringInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        value = serializer.validated_data['value']
        analysis = analyze_string(value)
        string_id = analysis['sha_256_hash']

        #Check if string already exists
        if AnalyzedString.objects.filter(sha_256_hash=analysis['sha_256_hash']).exists():
            return Response(
                {"detail": "String already exist in the system."},
                status=status.HTTP_409_CONFLICT
            )

        #Create Record
        db_string = AnalyzedString.objects.create(
            id=analysis['sha_256_hash'],  # Set ID to SHA hash
            value=value,
            length=analysis['length'],
            is_palindrome=analysis['is_palindrome'],
            unique_characters=analysis['unique_characters'],
            word_count=analysis['word_count'],
            sha_256_hash=analysis['sha_256_hash'],
            character_frequency_map=analysis['character_frequency_map']
        )
        serializer = AnalyzedStringSerializer(db_string)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    def retrieve(self, request, pk=None):
        value = pk
        analysis = analyze_string(value)
        string_id = analysis['sha_256_hash']

        db_string = get_object_or_404(AnalyzedString, id=string_id)
        serializer = AnalyzedStringSerializer(db_string)
        return Response(serializer.data)
    
    def list(self, request, pk=None):
        #Get all /strings with filtering
        queryset = AnalyzedString.objects.all()
        filters = {}

        #Get filters parameters
        is_palindrome = request.query_params.get('is_palindrome')
        min_length = request.query_params.get('min_length')
        max_length = request.query_params.get('max_length')
        word_count = request.query_params.get('word_count')
        contains_character = request.query_params.get('contains_character')

        #Apply filters
        if is_palindrome is not None:
            filters['is_palindrome'] = is_palindrome.lower() == 'true'

        if min_length is not None:
            try:
                filters['length__gte'] = int(min_length)
            except ValueError:
                return Response(
                    {"detail": "Invalid minimal Length"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        if max_length is not None:
            try:
                filters['length__lte'] = int(max_length)
            except ValueError:
                return Response(
                    {"detail": "Invalid maximal Length"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        if word_count is not None:
            try:
                filters['word_count'] = int(word_count)
            except ValueError:
                return Response(
                    {"detail": "Invalid Word Count"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        queryset = queryset.filter(**filters)
        results = list(queryset)
        if contains_character is not None:
            results = [
                s for s in results
                if contains_character in s.character_frequency_map
            ]

        serializer = AnalyzedStringSerializer(results, many=True)
        return Response({
            'data': serializer.data, 
            'count': len(results), 
            'filters_applied': {
                'is_palindrome': is_palindrome, 
                'min_length': min_length, 
                'max_length': max_length, 
                'word_count': word_count, 
                'contains_character': contains_character, 
            }

        })
    def destroy(self, request, pk=None):
        #Delete /string Values
        value = pk
        analysis = analyze_string(value)
        string_id = analysis['sha_256_hash']

        db_string = get_object_or_404(AnalyzedString, id=string_id)
        db_string.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def filter_by_natural_language(self, request):
        #Get /strings - Delete a string
        query = request.query_params.get('query')
        filters = {}
        if not query:
            return Response(
                {"detail": "Query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        from .utils import parse_natural_language_query
        try:
            parsed_filters = parse_natural_language_query(query)

            if not parsed_filters:
                return Response(
                    {'detail': 'Unable to parse natural language query'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            #Build filters
            filters = {}
            if 'is_palindrome' in parsed_filters:
                filters['is_palindrome'] = parsed_filters['is_palindrome']
            if 'min_length' in parsed_filters:
                filters['length__gte'] = parsed_filters['min_length']
            if 'max_length' in parsed_filters:
                filters['length__lte'] = parsed_filters['max_length']
            if 'word_count' in parsed_filters:
                filters['word_count'] = parsed_filters['word_count']
            
            print(f"DEBUG: parsed_filters = {parsed_filters}")
            print(f"DEBUG: filters = {filters}")
            
            queryset = AnalyzedString.objects.filter(**filters)
            results = list(queryset)
            print(f"DEBUG: results count = {len(results)}")

            #Filter by character
            if 'contains_character' in parsed_filters:
                char = parsed_filters['contains_character']
                results = [
                    r for r in results
                    if char.lower() in r.character_frequency_map
                ]

            serializer = AnalyzedStringSerializer(results, many=True)
            return Response({
                'data': serializer.data, 
                'count': len(results), 
                'interpreted_query': {
                    'original': query, 
                    'parsed_filters': parsed_filters
                }
            })
        except Exception:
            return Response(
                {'detail': 'Unable to parse natural language query'},
                status=status.HTTP_400_BAD_REQUEST
            )