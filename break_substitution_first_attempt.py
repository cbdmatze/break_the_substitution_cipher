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
    # Only consider alphabetic characters in the encrypted text
    encrypted_letters_only = [char.lower() for char in encrypted_text if char.isalpha()]

    # Count frequency of letters in both texts
    encrypted_freq = Counter(encrypted_letters_only)
    typical_freq = Counter(typical_text)

    # Sort letters by their frequency
    sorted_encrypted_letters = [item[0] for item in encrypted_freq.most_common()]
    sorted_typical_letters = [item[0] for item in typical_freq.most_common()]

    # Map letters from encrypted to typical based on frequency
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


def main():
    # Load the encrypted book
    encrypted_text = load_encrypted_text(BOOK_FILE_NAME)

    # Frequency analysis of the encrypted text
    encrypted_freq = analyze_frequency(encrypted_text)  # Fixed variable name

    # Typical letter frequency in English
    typical_english_freq = Counter("etaoinshrdlcumwfgypbvkjxqz")  # Fixed typo in variable name

    # Create a mapping based on frequency analysis
    mapping = create_mapping_by_frequency(encrypted_text, typical_english_freq)

    # Apply the mapping to the encrypted text
    decrypted_text = apply_mapping(encrypted_text, mapping)

    # Output the partially decrypted text
    print(decrypted_text[:500])  # Print the first 500 characters for review


if __name__ == "__main__":
    main()
