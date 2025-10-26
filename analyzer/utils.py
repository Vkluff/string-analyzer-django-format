import hashlib
from typing import Dict

def compute_sha256_hash(input_string: str) -> str:
    """Compute the SHA-256 hash of the given input string."""
    return hashlib.sha256(input_string.encode()).hexdigest()

def is_palindrome(value: str) -> bool:
    """Check if the given string is a palindrome."""
    cleaned_value = value.replace(" ", "").lower()
    return cleaned_value == cleaned_value[::-1]

def count_unique_characters(value: str) -> int:
    """Count the number of unique characters in the string."""
    return len(set(value.lower()))

def count_words(value: str) -> int:
    """Count words seperated by whitespace"""
    trimmed_value = value.strip()
    if not trimmed_value:
        return 0
    return len(trimmed_value.split())

def character_frequency_map(value: str) -> Dict[str, int]: 
    """Create a frequency map of characters (case insensitive, excluding spaces)."""
    frequency = {}
    for char in value.lower():
        if char != ' ':
            frequency[char] = frequency.get(char, 0) + 1
    return frequency

def analyze_string(value: str) -> Dict:
    """Analyze the given string and return various properties."""
    analysis = {
        'length': len(value),
        'is_palindrome': is_palindrome(value),
        'unique_characters': count_unique_characters(value),
        'word_count': count_words(value),
        'sha_256_hash': compute_sha256_hash(value),
        'character_frequency_map': character_frequency_map(value)
    }
    return analysis

def parse_natural_language_query(query: str) -> Dict[str, str]:
    """Parse a simple natural language query into filter parameters.
    
     Examples:
    - "all single word palindromic strings" → {word_count: 1, is_palindrome: true}
    - "strings longer than 10 characters" → {min_length: 11}
    - "strings containing the letter z" → {contains_character: 'z'}
    """
    import re

    filters = {}
    query_lower = query.lower()

    if "palindrom" in query_lower:
        filters['is_palindrome'] = True

    if "single word" in query_lower or "single_word" in query_lower:
        filters['word_count'] = 1

    # Check for length constraints
    longer_match = re.search(r"longer than (\d+)", query_lower)
    if longer_match:
        filters["min_length"] = int(longer_match.group(1)) + 1
    
    shorter_match = re.search(r"shorter than (\d+)", query_lower)
    if shorter_match:
        filters["max_length"] = int(shorter_match.group(1)) - 1
    
    # Check for character mentions
    if "first vowel" in query_lower or "vowel" in query_lower:
        filters["contains_character"] = "a"
    
    if "letter z" in query_lower:
        filters["contains_character"] = "z"
    
    char_match = re.search(r"contain.*(?:letter|character)\s+([a-z])", query_lower)
    if char_match:
        filters["contains_character"] = char_match.group(1)
    
    # Check for word count
    word_count_match = re.search(r"(\d+)\s+word", query_lower)
    if word_count_match:
        filters["word_count"] = int(word_count_match.group(1))
    
    return filters