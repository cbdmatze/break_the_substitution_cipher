import string
import random
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


# Identify common trigrams (three-letter sequences)
def trigram_analysis(text):
    trigrams = [text[i:i+3] for i in range(len(text) - 2) if text[i:i+3].isalpha()]
    return Counter(trigrams)


# Substitute text using a given dictionary
def substitute_text(text, substitution_dict):
    table = str.maketrans(substitution_dict)
    return text.translate(table)


# Refine mappings based on common digraphs, trigrams, and words
def refine_mapping(freq, digraphs, trigrams, encrypted_text):
    # Start with a base mapping from frequency analysis
    substitution_dict = {}
    
    # Known letter frequency in English
    english_letter_freq = "etaoinshrdlcumwfgypbvkjxqz"
    
    # Known common digraphs, trigrams, and short words in English
    common_digraphs = ['th', 'he', 'in', 'er', 'an', 're', 'on', 'at', 'en', 'nd', 'ti', 'es', 'or', 'te', 'of']
    common_trigrams = ['the', 'and', 'ing', 'ent', 'ion', 'her', 'for', 'tha', 'nth', 'int', 'ere', 'tio', 'ter']
    common_words = ["the", "and", "is", "in", "to", "of"]
    
    # Analyze the top most common letters and digraphs from the encrypted text
    most_common_letters = [item[0] for item in freq.most_common()]
    most_common_digraphs = [item[0] for item in digraphs.most_common()]
    most_common_trigrams = [item[0] for item in trigrams.most_common()]
    
    # Step 1: Create a frequency-based mapping (most frequent letter to 'e', etc.)
    for enc_letter, eng_letter in zip(most_common_letters, english_letter_freq):
        substitution_dict[enc_letter] = eng_letter
        substitution_dict[enc_letter.upper()] = eng_letter.upper()
    
    # Step 2: Match common digraphs to refine the mapping
    for enc_digraph, common_digraph in zip(most_common_digraphs, common_digraphs):
        substitution_dict[enc_digraph[0]] = common_digraph[0]
        substitution_dict[enc_digraph[1]] = common_digraph[1]
    
    # Step 3: Match common trigrams to refine the mapping further
    for enc_trigram, common_trigram in zip(most_common_trigrams, common_trigrams):
        for i in range(3):
            substitution_dict[enc_trigram[i]] = common_trigram[i]
    
    # Step 4: Look for common words in the decrypted text and refine further
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


# Scoring function based on letter, digraph, and trigram analysis
def evaluate_decryption(decrypted_text):
    score = 0

    # Analyze letter frequency, digraphs, and trigrams
    letter_freq = frequency_analysis(decrypted_text)
    digraphs = digraph_analysis(decrypted_text)
    trigrams = trigram_analysis(decrypted_text)
    
    # Known common English digraphs and trigrams
    common_digraphs = ['th', 'he', 'in', 'er', 'an', 're', 'on', 'at', 'en', 'nd', 'ti', 'es', 'or', 'te', 'of']
    common_trigrams = ['the', 'and', 'ing', 'ent', 'ion', 'her', 'for', 'tha', 'nth', 'int', 'ere', 'tio', 'ter']

    # Reward matches for common digraphs
    for digraph in common_digraphs:
        score += digraphs[digraph] * 2  # Digraph match gives a weight of 2
    
    # Reward matches for common trigrams
    for trigram in common_trigrams:
        score += trigrams[trigram] * 3  # Trigram match gives a weight of 3

    # Other scoring based on common words or letter frequency can stay as is.
    
    return score


# Simulated Annealing with Trigrams for Hill Climbing
def simulated_annealing_with_trigrams(encrypted_text, initial_mapping, temperature=1000, cooling_rate=0.995, max_iterations=1000):
    current_mapping = initial_mapping.copy()
    current_decrypted = substitute_text(encrypted_text, current_mapping)
    current_score = evaluate_decryption(current_decrypted)
    
    best_mapping = current_mapping
    best_decrypted = current_decrypted
    best_score = current_score
    
    for iteration in range(max_iterations):
        # Decrease the temperature
        temperature *= cooling_rate

        # Swap two random letters in the current mapping to generate a neighbor
        neighbor_mapping = current_mapping.copy()
        letter1, letter2 = random.sample(string.ascii_lowercase, 2)
        neighbor_mapping[letter1], neighbor_mapping[letter2] = neighbor_mapping[letter2], neighbor_mapping[letter1]

        # Decrypt with the new neighbor mapping
        neighbor_decrypted = substitute_text(encrypted_text, neighbor_mapping)
        neighbor_score = evaluate_decryption(neighbor_decrypted)
        
        # Check if the neighbor is better or accept it probabilistically
        score_diff = neighbor_score - current_score
        if score_diff > 0 or random.random() < math.exp(score_diff / temperature):
            current_mapping = neighbor_mapping
            current_decrypted = neighbor_decrypted
            current_score = neighbor_score
            
            # Keep track of the best solution
            if current_score > best_score:
                best_mapping = current_mapping
                best_decrypted = current_decrypted
                best_score = current_score
        
        # Optionally, print progress every 100 iterations
        if iteration % 100 == 0:
            print(f"Iteration {iteration}, Best Score: {best_score}")
    
    return best_decrypted, best_mapping


# Main function to break the cipher using simulated annealing with trigrams
def break_cipher_with_trigrams(filename):
    # Load the encrypted text
    encrypted_text = load_encrypted_book(filename)
    
    # Perform frequency analysis on the text
    freq = frequency_analysis(encrypted_text)
    print("Letter Frequency Analysis:")
    print(freq.most_common())
    
    # Analyze digraphs and trigrams (two-letter and three-letter pairs)
    digraphs = digraph_analysis(encrypted_text)
    trigrams = trigram_analysis(encrypted_text)
    print("Digraph and Trigram Frequency Analysis:")
    print(digraphs.most_common(), trigrams.most_common())
    
    # Refine the mapping using frequency analysis, digraphs, trigrams, and common words
    initial_mapping = refine_mapping(freq, digraphs, trigrams, encrypted_text)
    
    # Use simulated annealing to improve the mapping
    decrypted_text, best_mapping = simulated_annealing_with_trigrams(encrypted_text, initial_mapping)
    
    # Output the partially decrypted text
    print("\nDecrypted Text (First 500 Characters):\n")
    print(decrypted_text[:1000])
    
    return decrypted_text

# Run the cipher breaker on the file
break_cipher_with_trigrams("encrypted_book.txt")