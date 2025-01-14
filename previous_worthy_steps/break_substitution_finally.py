import string
from collections import Counter

def load_encrypted_text(filename):
    """Loads the encrypted text from a file."""
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return ""
    

def analyze_frequency(text):
    """Analyzes the letter frequency of the encrypted text."""
    letters_only = [char.lower() for char in text if char.isalpha()]
    return Counter(letters_only)


def create_mapping_by_frequency(encrypted_freq, typical_freq):
    """Create a potential mapping by comparing frequency counts."""
    sorted_encrypted_letters = [item[0] for item in encrypted_freq.most_common()]
    sorted_typical_letters = [item[0] for item in typical_freq.most_common()]

    mapping = {}
    for enc_letter, typ_letter in zip(sorted_encrypted_letters, sorted_typical_letters):
        mapping[enc_letter] = typ_letter
        mapping[enc_letter.upper()] = typ_letter.upper()
    
    return mapping


def update_mapping(existing_mapping, new_guesses):
    """Update the letter mapping with new guesses."""
    existing_mapping.update(new_guesses)
    return existing_mapping


def apply_mapping(text, mapping):
    """Applies the letter mapping to the encrypted text."""
    decrypted_text = [mapping.get(char, char) for char in text]
    return ''.join(decrypted_text)


def main(book_file_name="encrypted_book.txt"):
    encrypted_text = load_encrypted_text(book_file_name)
    if not encrypted_text:
        return  # Exit if there's an error loading the text.

    # Analyze frequency of letters in the encrypted text
    encrypted_freq = analyze_frequency(encrypted_text)

    # Typical letter frequency in English
    typical_english_freq = Counter("etaoinshrdlcumwfgypbvkjxqz")

    # Create initial mapping based on frequency analysis
    mapping = create_mapping_by_frequency(encrypted_freq, typical_english_freq)

    # Apply the frequency-based mapping
    partially_decrypted_text = apply_mapping(encrypted_text, mapping)
    print("Partially Decrypted Text (Frequency Based):\n", partially_decrypted_text[:1000])

    # Update mapping based on manual guesses
    new_guesses = {
        'W': 'F', 'h': 'r', 'n': 'a', 'k': 'n', 'e': 'k', 't': 't',
        's': 's', 'i': 'i', 'c': 'c', 'o': 'o', 'Y': 'M', 'b': 'h',
        'f': 'w', 'g': 'y', 'A': 'C', 'R': 'S', 'a': 'e', 'o': 't'
    }
    
    mapping = update_mapping(mapping, new_guesses)

    # Apply the updated mapping
    fully_decrypted_text = apply_mapping(partially_decrypted_text, mapping)
    print("\nFully Decrypted Text (With Manual Updates):\n", fully_decrypted_text[:1000])


if __name__ == "__main__":
    main()