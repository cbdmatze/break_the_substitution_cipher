import random
import string
from collections import Counter
import math

# Load the encrypted book
def load_encrypted_book(filename):
    with open(filename, "r") as file:
        return file.read()

# Substitute text using a given dictionary
def substitute_text(text, substitution_dict):
    table = str.maketrans(substitution_dict)
    return text.translate(table)

# Evaluate the current decryption based on n-grams
def evaluate_decryption(decrypted_text, digraph_weight=2, trigram_weight=3, quadgram_weight=4, pentagram_weight=5, penalty_weight=1):
    # Load n-gram models
    common_digraphs = ['th', 'he', 'in', 'er', 'an', 're', 'on', 'at', 'en', 'nd', 'ti', 'es', 'or', 'te', 'of']
    common_trigrams = ['the', 'and', 'ing', 'her', 'hat', 'his', 'tha', 'ere', 'for', 'ent', 'ion', 'ter']
    common_quadgrams = ['tion', 'ment', 'that', 'with', 'this', 'ther', 'here', 'ions', 'ated', 'able']
    common_pentagrams = ['ation', 'ation', 'there', 'other', 'their', 'which', 'would', 'could', 'about', 'after']
    
    # Compute scores based on n-grams
    score = 0
    
    # Bigrams
    digraph_score = sum([decrypted_text.count(d) for d in common_digraphs]) * digraph_weight
    score += digraph_score
    
    # Trigrams
    trigram_score = sum([decrypted_text.count(t) for t in common_trigrams]) * trigram_weight
    score += trigram_score
    
    # Quadgrams (4-grams)
    quadgram_score = sum([decrypted_text.count(q) for q in common_quadgrams]) * quadgram_weight
    score += quadgram_score
    
    # Pentagrams (5-grams)
    pentagram_score = sum([decrypted_text.count(p) for p in common_pentagrams]) * pentagram_weight
    score += pentagram_score
    
    # Penalize unlikely sequences
    unlikely_sequences = ['zx', 'qq', 'jf', 'zz', 'vx']  
    for seq in unlikely_sequences:
        score -= decrypted_text.count(seq) * penalty_weight
    
    return score

# Simulated Annealing with higher n-grams
def simulated_annealing_with_ngrams(encrypted_text, initial_mapping, digraph_weight=2, trigram_weight=3, quadgram_weight=4, pentagram_weight=5, temperature=1000, cooling_rate=0.995, max_iterations=1000):
    current_mapping = initial_mapping.copy()
    best_mapping = current_mapping.copy()
    best_decrypted_text = substitute_text(encrypted_text, best_mapping)
    best_score = evaluate_decryption(best_decrypted_text, digraph_weight, trigram_weight, quadgram_weight, pentagram_weight)
    
    current_decrypted_text = best_decrypted_text
    current_score = best_score
    
    for iteration in range(max_iterations):
        # Generate a neighboring solution by swapping two random letters in the mapping
        new_mapping = current_mapping.copy()
        letter1, letter2 = random.sample(string.ascii_lowercase, 2)
        new_mapping[letter1], new_mapping[letter2] = new_mapping[letter2], new_mapping[letter1]
        
        # Apply the new mapping and evaluate
        new_decrypted_text = substitute_text(encrypted_text, new_mapping)
        new_score = evaluate_decryption(new_decrypted_text, digraph_weight, trigram_weight, quadgram_weight, pentagram_weight)
        
        # Calculate probability of accepting the new solution
        delta_score = new_score - current_score
        if delta_score > 0 or random.uniform(0, 1) < math.exp(delta_score / temperature):
            current_mapping = new_mapping
            current_decrypted_text = new_decrypted_text
            current_score = new_score
        
        # Update the best solution found so far
        if current_score > best_score:
            best_mapping = current_mapping
            best_decrypted_text = current_decrypted_text
            best_score = current_score
        
        # Cool down the temperature
        temperature *= cooling_rate
        
        # Stop early if temperature gets too low
        if temperature < 0.1:
            break
        
    return best_decrypted_text, best_score

# Initialize random substitution mapping
def initialize_random_mapping():
    letters = list(string.ascii_lowercase)
    shuffled_letters = random.sample(letters, len(letters))
    mapping = {letters[i]: shuffled_letters[i] for i in range(26)}
    mapping.update({letter.upper(): shuffled_letters[i].upper() for i, letter in enumerate(letters)})
    return mapping

# Grid search over hyperparameters
def grid_search(encrypted_text, filename, digraph_weights, trigram_weights, quadgram_weights, pentagram_weights, temperatures, cooling_rates, max_iterations=1000):
    best_combination = None
    best_score = -float('inf')
    best_decrypted_text = None
    
    # Try every combination of hyperparameters
    for digraph_weight in digraph_weights:
        for trigram_weight in trigram_weights:
            for quadgram_weight in quadgram_weights:
                for pentagram_weight in pentagram_weights:
                    for temperature in temperatures:
                        for cooling_rate in cooling_rates:
                            print(f"Testing: Digraph Weight={digraph_weight}, Trigram Weight={trigram_weight}, Quadgram Weight={quadgram_weight}, Pentagram Weight={pentagram_weight}, Temp={temperature}, Cooling Rate={cooling_rate}")
                            
                            # Initialize a random substitution mapping
                            initial_mapping = initialize_random_mapping()
                            
                            # Decrypt using simulated annealing
                            decrypted_text, score = simulated_annealing_with_ngrams(
                                encrypted_text, initial_mapping, digraph_weight, trigram_weight, quadgram_weight, pentagram_weight, temperature, cooling_rate, max_iterations
                            )
                            
                            # Update best score if this is better
                            if score > best_score:
                                best_score = score
                                best_combination = (digraph_weight, trigram_weight, quadgram_weight, pentagram_weight, temperature, cooling_rate)
                                best_decrypted_text = decrypted_text
                                print(f"New Best Score: {best_score} with {best_combination}")
    
    # Output the final decrypted text
    print("\nBest Decrypted Text (First 500 Characters):\n")
    print(best_decrypted_text[:500])
    
    print(f"\nBest Hyperparameters: Digraph Weight={best_combination[0]}, Trigram Weight={best_combination[1]}, Quadgram Weight={best_combination[2]}, Pentagram Weight={best_combination[3]}, Temp={best_combination[4]}, Cooling Rate={best_combination[5]}")
    
    return best_decrypted_text

# Main function to run grid search and break the cipher
def break_cipher_with_grid_search(filename):
    # Load the encrypted text
    encrypted_text = load_encrypted_book(filename)
    
    # Define parameter ranges for grid search
    digraph_weights = [1, 2, 3]
    trigram_weights = [1, 2, 3]
    quadgram_weights = [3, 4, 5]
    pentagram_weights = [4, 5, 6]
    temperatures = [500, 1000, 1500]
    cooling_rates = [0.99, 0.995, 0.999]
    
    # Run grid search
    best_decrypted_text = grid_search(encrypted_text, filename, digraph_weights, trigram_weights, quadgram_weights, pentagram_weights, temperatures, cooling_rates)
    
    return best_decrypted_text

# Run the cipher breaker with grid search
break_cipher_with_grid_search("encrypted_book.txt")
