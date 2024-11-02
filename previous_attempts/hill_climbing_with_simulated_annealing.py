import random
import string
import math
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

# Score the decrypted text based on common words, digraphs, and letter frequencies
def score_decrypted_text(decrypted_text):
    # Common English words
    common_words = ["the", "and", "is", "in", "to", "of", "it", "that"]
    
    # Score based on common words
    score = 0
    for word in common_words:
        score += decrypted_text.count(word) * 10  # Weight common words heavily
    
    # English letter frequencies (ETAOIN SHRDLU)
    english_letter_freq = {'e': 12.7, 't': 9.1, 'a': 8.2, 'o': 7.5, 'i': 7.0, 'n': 6.7, 
                           's': 6.3, 'h': 6.1, 'r': 6.0, 'd': 4.3, 'l': 4.0, 'c': 2.8, 
                           'u': 2.7, 'm': 2.4, 'w': 2.4, 'f': 2.2, 'g': 2.0, 'y': 2.0, 
                           'p': 1.9, 'b': 1.5, 'v': 1.0, 'k': 0.8, 'x': 0.1, 'q': 0.1, 
                           'j': 0.1, 'z': 0.1}
    
    # Frequency analysis of the decrypted text
    decrypted_letter_freq = frequency_analysis(decrypted_text)
    total_letters = sum(decrypted_letter_freq.values())
    
    # Score based on how close letter frequencies are to typical English
    for letter, count in decrypted_letter_freq.items():
        if letter in english_letter_freq:
            expected_freq = english_letter_freq[letter]
            actual_freq = (count / total_letters) * 100
            score -= abs(actual_freq - expected_freq)  # Subtract penalty for deviation
    
    # Digraph frequency
    common_digraphs = ['th', 'he', 'in', 'er', 'an', 're', 'on', 'at', 'en', 'nd', 'ti', 'es', 'or', 'te', 'of']
    decrypted_digraphs = digraph_analysis(decrypted_text)
    
    # Score based on common digraphs
    for digraph in common_digraphs:
        score += decrypted_digraphs[digraph] * 5  # Weight common digraphs
    
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

# Refine mappings based on frequency analysis (initial substitution dictionary)
def refine_mapping(freq, digraphs, encrypted_text):
    substitution_dict = {}
    english_letter_freq = "etaoinshrdlcumwfgypbvkjxqz"
    
    most_common_letters = [item[0] for item in freq.most_common()]
    
    for enc_letter, eng_letter in zip(most_common_letters, english_letter_freq):
        substitution_dict[enc_letter] = eng_letter
        substitution_dict[enc_letter.upper()] = eng_letter.upper()
    
    return substitution_dict

# Simulated annealing optimization
def simulated_annealing(encrypted_text, initial_substitution_dict, iterations=1000, initial_temp=1000, cooling_rate=0.995):
    current_substitution = initial_substitution_dict
    current_decrypted = substitute_text(encrypted_text, current_substitution)
    current_score = score_decrypted_text(current_decrypted)
    
    temperature = initial_temp
    
    for i in range(iterations):
        # Swap two letters in the current substitution dictionary
        new_substitution = swap_letters(current_substitution)
        new_decrypted = substitute_text(encrypted_text, new_substitution)
        new_score = score_decrypted_text(new_decrypted)
        
        # If the new mapping improves the score, or we accept a worse solution probabilistically
        score_diff = new_score - current_score
        acceptance_probability = math.exp(score_diff / temperature) if score_diff < 0 else 1
        
        if score_diff > 0 or random.random() < acceptance_probability:
            current_substitution = new_substitution
            current_score = new_score
            print(f"Iteration {i}: New better score: {new_score}")
        
        # Decrease the temperature
        temperature *= cooling_rate
    
    return current_substitution

# Main function to break the cipher using simulated annealing
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
    
    # Apply simulated annealing to improve the substitution
    best_substitution_dict = simulated_annealing(encrypted_text, initial_substitution_dict)
    
    # Decrypt text using the optimized substitution
    decrypted_text = substitute_text(encrypted_text, best_substitution_dict)
    
    # Output the partially decrypted text
    print("\nDecrypted Text (First 500 Characters):\n")
    print(decrypted_text[:1000])
    
    return decrypted_text

# Run the cipher breaker on the file
break_cipher("encrypted_book.txt")