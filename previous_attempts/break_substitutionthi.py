import string
from collections import Counter

BOOK_FILE_NAME = "encrypted_book.txt"

def load_encrypted_text(filename):
    """Loads the encrypted text from a file."""
    with open(filename, 'r') as f:
        return f.read()

def analyze_frequency(text):
    """Analyzes the letter frequency of the encrypted text."""
    # Only analyze alphabetic characters (ignoring punctuation and spaces)
    letters_only = [char.lower() for char in text if char.isalpha()]
    return Counter(letters_only)

def create_mapping_by_frequency(encrypted_text, typical_text):
    """Create a potential mapping by comparing frequency counts."""
    # Count frequency of letters in the encrypted text
    encrypted_freq = Counter(char.lower() for char in encrypted_text if char.isalpha())
    typical_freq = Counter(typical_text)

    # Sort letters by their frequency
    sorted_encrypted_letters = [item[0] for item in encrypted_freq.most_common()]
    sorted_typical_letters = [item[0] for item in typical_freq.most_common()]

    # Create mapping based on frequency
    mapping = {}
    for enc_letter, typ_letter in zip(sorted_encrypted_letters, sorted_typical_letters):
        mapping[enc_letter] = typ_letter
        mapping[enc_letter.upper()] = typ_letter.upper()
    
    return mapping

def apply_mapping(text, mapping):
    """Applies the letter mapping to the encrypted text."""
    decrypted_text = []
    for char in text:
        if char in mapping:
            decrypted_text.append(mapping[char])
        else:
            decrypted_text.append(char)  # Leave non-alphabetic characters unchanged
    return ''.join(decrypted_text)

def update_mapping(existing_mapping, manual_updates):
    """Update the existing mapping with manual corrections."""
    for enc_letter, typ_letter in manual_updates.items():
        existing_mapping[enc_letter] = typ_letter
        existing_mapping[enc_letter.upper()] = typ_letter.upper()
    return existing_mapping

def main():
    # Load the encrypted book
    encrypted_text = load_encrypted_text(BOOK_FILE_NAME)

    # Frequency analysis of the encrypted text
    encrypted_freq = analyze_frequency(encrypted_text)

    # Typical letter frequency in English
    typical_english_freq = "etaoinshrdlcumwfgypbvkjxqz"

    # Create a mapping based on frequency analysis
    mapping = create_mapping_by_frequency(encrypted_text, typical_english_freq)

    # Update the mapping with new manual adjustments based on the latest output
    manual_updates = {
        'W': 'F',
        'h': 'r',
        'n': 'a',
        'k': 'n',
        'e': 'k',
        't': 't',
        's': 's',
        'i': 'i',
        'c': 'c',
        'o': 'o',
        'Y': 'M',
        'b': 'h',
        'f': 'w',
        'g': 'y',
        'A': 'C',  # Adjust based on recognizable patterns
        'R': 'S',
        'a': 'e',
        'i': 'o',
        'W': 'F',
        'h': 'r',
        'n': 'a',
        'k': 'n',
        'o': 'k',  # If you're seeing a pattern
        't': 't',
        'e': 'e'  # Revisit based on frequency
    }
    
    mapping = update_mapping(mapping, manual_updates)

    # Apply the mapping to the encrypted text
    decrypted_text = apply_mapping(encrypted_text, mapping)

    # Output the partially decrypted text
    print("Decrypted Text (First 500 Characters):\n", decrypted_text[:500])

if __name__ == "__main__":
    main()
