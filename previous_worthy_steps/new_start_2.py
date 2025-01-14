import string
from collections import Counter

# Load the encrypted book
def load_encrypted_book(filename):
    with open(filename, "r") as file:
        return file.read()

# Frequency analysis of the text
def frequency_analysis(text):
    letters_only = [char.lower() for char in text if char.isalpha()]
    return Counter(letters_only)

# Identify common digraphs (letter pairs)
def digraph_analysis(text):
    digraphs = [text[i:i+2] for i in range(len(text) - 1) if text[i:i+2].isalpha()]
    return Counter(digraphs)

# Substitute text using a given dictionary
def substitute_text(text, substitution_dict):
    table = str.maketrans(substitution_dict)
    return text.translate(table)

# Refine mappings based on common digraphs and words
def refine_mapping(freq, digraphs, encrypted_text):
    # Start with a base mapping from frequency analysis
    substitution_dict = {}
    
    # Known letter frequency in English
    english_letter_freq = "etaoinshrdlcumwfgypbvkjxqz"
    
    # Known common digraphs and short words in English
    common_digraphs = ['th', 'he', 'in', 'er', 'an', 're', 'on', 'at', 'en', 'nd', 'ti', 'es', 'or', 'te', 'of']
    common_words = ["the", "and", "is", "in", "to", "of"]
    
    # Analyze the top most common letters and digraphs from the encrypted text
    most_common_letters = [item[0] for item in freq.most_common()]
    most_common_digraphs = [item[0] for item in digraphs.most_common()]
    
    # Step 1: Create a frequency-based mapping (most frequent letter to 'e', etc.)
    for enc_letter, eng_letter in zip(most_common_letters, english_letter_freq):
        substitution_dict[enc_letter] = eng_letter
        substitution_dict[enc_letter.upper()] = eng_letter.upper()
    
    # Step 2: Match common digraphs to refine the mapping
    for enc_digraph, common_digraph in zip(most_common_digraphs, common_digraphs):
        substitution_dict[enc_digraph[0]] = common_digraph[0]
        substitution_dict[enc_digraph[1]] = common_digraph[1]
    
    # Step 3: Look for common words in the decrypted text and refine further
    # Apply the current substitution and check for common words
    partially_decrypted = substitute_text(encrypted_text, substitution_dict)
    
    for word in common_words:
        if word in partially_decrypted:
            # If we find a match, lock in those letters in the substitution
            for enc_letter, real_letter in zip(partially_decrypted, word):
                if enc_letter.isalpha():
                    substitution_dict[enc_letter.lower()] = real_letter
                    substitution_dict[enc_letter.upper()] = real_letter.upper()
    
    return substitution_dict

# Main function to break the cipher using the refined mapping
def break_cipher(filename):
    # Load the encrypted text
    encrypted_text = load_encrypted_book(filename)
    
    # Perform frequency analysis on the text
    freq = frequency_analysis(encrypted_text)
    print("Letter Frequency Analysis:")
    print(freq.most_common())
    
    # Analyze digraphs (two-letter pairs)
    digraphs = digraph_analysis(encrypted_text)
    print("Digraph Frequency Analysis:")
    print(digraphs.most_common())
    
    # Refine the mapping using frequency analysis, digraphs, and common words
    substitution_dict = refine_mapping(freq, digraphs, encrypted_text)
    
    # Decrypt text using the substitution
    decrypted_text = substitute_text(encrypted_text, substitution_dict)
    
    # Output the partially decrypted text
    print("\nDecrypted Text (First 500 Characters):\n")
    print(decrypted_text[:1000])
    
    return decrypted_text

# Run the cipher breaker on the file
break_cipher("encrypted_book.txt")