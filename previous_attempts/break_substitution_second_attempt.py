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
    # Count frequency of letters in both texts
    encrypted_freq = Counter(encrypted_text)
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


def update_mapping():
    """Update the letter mapping based on the guessed word 'Introduction'."""
    mapping = {
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
        'A': 'C',
        'R': 'S',
        'a': 'e',
        'o': 't'
    }

    # Handle lowercase equivalents
    for k, v in list(mapping.items()):
        mapping[k.lower()] = v.lower()

    return mapping


def apply_mapping(text, mapping):
    """Applies the updated letter mapping to the encrypted text."""
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
    encrypted_frequ = analyze_frequency(encrypted_text)

    # Typical letter frequency in English
    typical_english_freq= Counter("etaoinshrdlcumwfgypbvkjxqz")

    # Create a mapping based on frequency analysis
    mapping = create_mapping_by_frequency(encrypted_frequ, typical_english_freq)

    # Apply the frequency-based mapping first
    partially_decrypted_text = apply_mapping(encrypted_text, mapping)
    print("Partially Decrypted Text (Frequency Based):\n", partially_decrypted_text[:1000])

    # Now update the mapping manually based on any guesses
    updated_mapping = update_mapping()

    # Apply the updated mapping to the partially decrypted text
    fully_decrypted_text = apply_mapping(partially_decrypted_text, updated_mapping)
    print("\nFully Decrypted Text (With Manual Updates):\n", fully_decrypted_text[:1000])


if __name__ == "__main__":
    main()
