import random
import string
from collections import Counter

# Load the encrypted book
def load_encrypted_book(filename):
    with open(filename, "r") as file:
        return file.read()

# Frequency analys
# is of the text
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


# Score the decrypted text based on common words and digraphs
def score_decrypted_text(decrypted_text):
    # Simple scoring method: count common English words
    common_words = ["the", "and", "is", "in", "to", "of", "it", "that"]
    score = 0
    for word in common_words:
        score += decrypted_text.count(word)
    
    # You can add additional scoring mechanisms here (e.g., digraph frequency)
    return score


# Swap two letters in the substitution dictionary
def swap_letters(substitution_dict):
    letters = list(substitution_dict.keys())
    letter1, letter2 = random.sample(letters, 2)  # Randomly choose two letters to swap
    new_dict = substitution_dict.copy()
    
    # Swap their mappings
    new_dict[letter1], new_dict[letter2] = substitution_dict[letter2], substitution_dict[letter1]
    new_dict[letter1.upper()], new_dict[letter2.upper()] = substitution_dict[letter2].upper(), substitution_dict[letter1].upper()
    
    return new_dict


# Refine mappings based on common digraphs and words (initial substitution dictionary)
def refine_mapping(freq, digraphs, encrypted_text):
    substitution_dict = {}
    english_letter_freq = "etaoinshrdlcumwfgypbvkjxqz"
    
    most_common_letters = [item[0] for item in freq.most_common()]
    
    for enc_letter, eng_letter in zip(most_common_letters, english_letter_freq):
        substitution_dict[enc_letter] = eng_letter
        substitution_dict[enc_letter.upper()] = eng_letter.upper()
    
    return substitution_dict


# Hill climbing optimization
def hill_climbing(encrypted_text, initial_substitution_dict, iterations=1000):
    current_substitution = initial_substitution_dict
    current_decrypted = substitute_text(encrypted_text, current_substitution)
    current_score = score_decrypted_text(current_decrypted)
    
    for _ in range(iterations):
        # Swap two letters in the current substitution dictionary
        new_substitution = swap_letters(current_substitution)
        new_decrypted = substitute_text(encrypted_text, new_substitution)
        new_score = score_decrypted_text(new_decrypted)
        
        # If the new mapping improves the score, accept it
        if new_score > current_score:
            current_substitution = new_substitution
            current_score = new_score
            print(f"New better score: {new_score}")
    
    return current_substitution


# Main function to break the cipher using hill climbing
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
    
    # Refine the mapping using frequency analysis (initial substitution)
    initial_substitution_dict = refine_mapping(freq, digraphs, encrypted_text)
    
    # Apply hill climbing to improve the substitution
    best_substitution_dict = hill_climbing(encrypted_text, initial_substitution_dict)
    
    # Decrypt text using the optimized substitution
    decrypted_text = substitute_text(encrypted_text, best_substitution_dict)
    
    # Output the partially decrypted text
    print("\nDecrypted Text (First 500 Characters):\n")
    print(decrypted_text[:1000])
    
    return decrypted_text

# Run the cipher breaker on the file
break_cipher("encrypted_book.txt")