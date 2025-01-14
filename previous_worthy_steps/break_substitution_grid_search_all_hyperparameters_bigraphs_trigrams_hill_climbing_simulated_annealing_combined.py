import string
from collections import Counter
import random
import math


# Load the encrypted book
def load_encrypted_book(filename):
    """Load encrypted text from a file."""
    with open(filename, "r") as file:
        return file.read()


# Frequency analysis of the text
def frequency_analysis(text):
    """Perform frequency analysis on the text to count letter occurrences."""
    letters_only = [char.lower() for char in text if char.isalpha()]
    return Counter(letters_only)


# Identify common n-grams (letter pairs or triplets)
def ngram_analysis(text, n=2):
    """Perform n-gram analysis (bigrams or trigrams) on the text."""
    ngrams = [text[i:i+n] for i in range(len(text) - n + 1) if text[i:i+n].isalpha()]
    return Counter(ngrams)


# Substitute text using a given dictionary
def substitute_text(text, substitution_dict):
    """Substitute characters in text based on the substitution dictionary."""
    table = str.maketrans(substitution_dict)
    return text.translate(table)


# Score the decrypted text based on n-gram frequencies
def score_decryption(decrypted_text, bigrams, trigrams, weights):
    """Score the decrypted text based on bigram and trigram frequency counts."""
    bigram_score = sum(bigrams.get(decrypted_text[i:i+2], 0) for i in range(len(decrypted_text) - 1))
    trigram_score = sum(trigrams.get(decrypted_text[i:i+3], 0) for i in range(len(decrypted_text) - 2))

    # Weighted sum of bigram and trigram scores
    return weights['bigram'] * bigram_score + weights['trigram'] * trigram_score


# Simulated Annealing algorithm
def simulated_annealing(encrypted_text, bigrams, trigrams, initial_substitution, weights, initial_temp, cooling_rate, iterations):
    """Simulated Annealing to optimize the decryption."""
    current_substitution = initial_substitution.copy()
    current_decrypted = substitute_text(encrypted_text, current_substitution)
    current_score = score_decryption(current_decrypted, bigrams, trigrams, weights)

    best_substitution = current_substitution.copy()
    best_score = current_score
    temperature = initial_temp

    for i in range(iterations):
        # Make a random change in the substitution
        new_substitution = current_substitution.copy()
        a, b = random.sample(string.ascii_lowercase, 2)
        new_substitution[a], new_substitution[b] = new_substitution[b], new_substitution[a]

        # Decrypt with the new substitution
        new_decrypted = substitute_text(encrypted_text, new_substitution)
        new_score = score_decryption(new_decrypted, bigrams, trigrams, weights)

        # Determine whether to accept the new solution
        if new_score > current_score or random.random() < math.exp((new_score - current_score) / temperature):
            current_substitution = new_substitution
            current_score = new_score

            if current_score > best_score:
                best_substitution = current_substitution.copy()
                best_score = current_score

        # Cool down the temperature
        temperature *= cooling_rate

    return substitute_text(encrypted_text, best_substitution), best_score, best_substitution


# Save results to a file
def save_results(filename, decrypted_text, best_hyperparameters):
    """Save the best-decrypted text and hyperparameters to a file."""
    with open(filename, "w") as file:
        file.write(f"Best Hyperparameters: {best_hyperparameters}\n\n")
        file.write("Decrypted Text:\n")
        file.write(decrypted_text)


# Main function
def main():
    """The main execution flow of the decryption program, including grid search and optimization."""
    encrypted_text = load_encrypted_book("encrypted_book.txt")

    # Perform frequency analysis
    bigrams = ngram_analysis(encrypted_text, n=2)
    trigrams = ngram_analysis(encrypted_text, n=3)

    # Define the grid search space
    digraph_weights = [1, 2, 3]
    trigram_weights = [1, 3, 5]
    temperatures = [1000, 2000, 3000]
    cooling_rates = [0.99, 0.995, 0.999]
    iterations_list = [500, 1000, 1500]

    # Perform grid search
    best_decrypted = None
    best_score = float('-inf')
    best_hyperparameters = {}

    for bigram_weight in digraph_weights:
        for trigram_weight in trigram_weights:
            for temp in temperatures:
                for rate in cooling_rates:
                    for iters in iterations_list:
                        weights = {'bigram': bigram_weight, 'trigram': trigram_weight}

                        print(f"Testing parameters: Bigram Weight={bigram_weight}, Trigram Weight={trigram_weight}, "
                              f"Temp={temp}, CoolingRate={rate}, Iterations={iters}")

                        initial_substitution = {char: char for char in string.ascii_lowercase}

                        decrypted_text, score, _ = simulated_annealing(
                            encrypted_text, bigrams, trigrams, initial_substitution, weights, temp, rate, iters)

                        if score > best_score:
                            best_decrypted = decrypted_text
                            best_score = score
                            best_hyperparameters = {
                                'bigram_weight': bigram_weight,
                                'trigram_weight': trigram_weight,
                                'initial_temp': temp,
                                'cooling_rate': rate,
                                'iterations': iters
                            }

    # Save the best-decrypted text and hyperparameters to a file
    save_results("decrypted_results.txt", best_decrypted, best_hyperparameters)


if __name__ == "__main__":
    main()