import random
import string
import math
from collections import Counter


# File I/O functions
def load_encrypted_book(filename):
    """
    Load the encrypted book from a text file.

    Parameters:
    - filename: str, the name of the file to load.

    Returns:
    - str: the content of the file as a string.
    """
    with open(filename, "r") as file:
        return file.read()


def save_results(filename, decrypted_text, best_hyperparameters):
    """
    Save the best decrypted text and corresponding hyperparameters to a file.

    Parameters:
    - filename: str, the name of the file to save the results.
    - decrypted_text: str, the best-decrypted text.
    - best_hyperparameters: dict, the best hyperparameters found during grid search.

    Returns:
    - None
    """
    with open(filename, "w") as file:
        file.write("Best Decrypted Text:\n")
        file.write(decrypted_text + "\n\n")
        file.write("Best Hyperparameters:\n")
        for param, value in best_hyperparameters.items():
            file.write(f"{param}: {value}\n")


# Frequency and N-gram analysis functions
def frequency_analysis(text):
    """
    Perform frequency analysis on the given text, returning the frequency count of letters.

    Parameters:
    - text: str, the text to analyze.

    Returns:
    - Counter: a Counter object with the frequency of each letter.
    """
    letters_only = [char.lower() for char in text if char.isalpha()]
    return Counter(letters_only)


def ngram_analysis(text, n=2):
    """
    Perform N-gram analysis on the text (bigrams, trigrams, etc.).

    Parameters:
    - text: str, the text to analyze.
    - n: int, the number of characters in the n-gram.

    Returns:
    - Counter: a Counter object with the frequency of each n-gram.
    """
    ngrams = [text[i:i+n] for i in range(len(text) - n + 1) if all(char.isalpha() for char in text[i:i+n])]
    return Counter(ngrams)


# Substitution and scoring functions
def substitute_text(text, substitution_dict):
    """
    Substitute characters in the text based on the provided substitution dictionary.

    Parameters:
    - text: str, the original text.
    - substitution_dict: dict, a dictionary mapping encrypted characters to decrypted ones.

    Returns:
    - str: the substituted text.
    """
    table = str.maketrans(substitution_dict)
    return text.translate(table)


def calculate_score(decrypted_text, bigrams, trigrams, quadgrams, weights):
    """
    Calculate the score of the decrypted text based on n-gram frequencies.

    Parameters:
    - decrypted_text: str, the text to evaluate.
    - bigrams: Counter, frequency counts of bigrams.
    - trigrams: Counter, frequency counts of trigrams.
    - quadgrams: Counter, frequency counts of quadgrams.
    - weights: dict, weights for bigrams, trigrams, and quadgrams.

    Returns:
    - float: the calculated score of the decrypted text.
    """
    bi_score = sum(bigrams[decrypted_text[i:i+2]] for i in range(len(decrypted_text) - 1))
    tri_score = sum(trigrams[decrypted_text[i:i+3]] for i in range(len(decrypted_text) - 2))
    quad_score = sum(quadgrams[decrypted_text[i:i+4]] for i in range(len(decrypted_text) - 3))

    score = (weights['bigram'] * bi_score +
             weights['trigram'] * tri_score +
             weights['quadgram'] * quad_score)
    
    return score


# Hill-climbing and Simulated Annealing functions
def hill_climbing(text, bigrams, trigrams, quadgrams, weights, iterations):
    """
    Perform hill-climbing to decrypt the text.

    Parameters:
    - text: str, the encrypted text.
    - bigrams: Counter, frequency counts of bigrams.
    - trigrams: Counter, frequency counts of trigrams.
    - quadgrams: Counter, frequency counts of quadgrams.
    - weights: dict, weights for bigrams, trigrams, and quadgrams.
    - iterations: int, number of iterations for the hill-climbing process.

    Returns:
    - tuple: (best_decrypted_text, best_score, best_substitution_dict)
    """
    alphabet = list(string.ascii_lowercase)
    current_substitution = {letter: letter for letter in alphabet}
    current_decrypted = substitute_text(text, current_substitution)
    current_score = calculate_score(current_decrypted, bigrams, trigrams, quadgrams, weights)

    best_substitution = current_substitution
    best_decrypted = current_decrypted
    best_score = current_score

    for _ in range(iterations):
        new_substitution = best_substitution.copy()
        a, b = random.sample(alphabet, 2)
        new_substitution[a], new_substitution[b] = new_substitution[b], new_substitution[a]

        new_decrypted = substitute_text(text, new_substitution)
        new_score = calculate_score(new_decrypted, bigrams, trigrams, quadgrams, weights)

        if new_score > best_score:
            best_substitution = new_substitution
            best_decrypted = new_decrypted
            best_score = new_score

    return best_decrypted, best_score, best_substitution


def simulated_annealing(text, bigrams, trigrams, quadgrams, weights, initial_temp, cooling_rate, iterations):
    """
    Perform simulated annealing to decrypt the text.

    Parameters:
    - text: str, the encrypted text.
    - bigrams: Counter, frequency counts of bigrams.
    - trigrams: Counter, frequency counts of trigrams.
    - quadgrams: Counter, frequency counts of quadgrams.
    - weights: dict, weights for bigrams, trigrams, and quadgrams.
    - initial_temp: float, initial temperature for the annealing process.
    - cooling_rate: float, rate at which the temperature cools.
    - iterations: int, number of iterations for the annealing process.

    Returns:
    - tuple: (best_decrypted_text, best_score, best_substitution_dict)
    """
    alphabet = list(string.ascii_lowercase)
    current_substitution = {letter: letter for letter in alphabet}
    current_decrypted = substitute_text(text, current_substitution)
    current_score = calculate_score(current_decrypted, bigrams, trigrams, quadgrams, weights)

    best_substitution = current_substitution
    best_decrypted = current_decrypted
    best_score = current_score

    temp = initial_temp

    for _ in range(iterations):
        new_substitution = current_substitution.copy()
        a, b = random.sample(alphabet, 2)
        new_substitution[a], new_substitution[b] = new_substitution[b], new_substitution[a]

        new_decrypted = substitute_text(text, new_substitution)
        new_score = calculate_score(new_decrypted, bigrams, trigrams, quadgrams, weights)

        if new_score > current_score or random.random() < math.exp((new_score - current_score) / temp):
            current_substitution = new_substitution
            current_decrypted = new_decrypted
            current_score = new_score

            if new_score > best_score:
                best_substitution = new_substitution
                best_decrypted = new_decrypted
                best_score = new_score

        temp *= cooling_rate

    return best_decrypted, best_score, best_substitution


# Main function
def main():
    """
    The main execution flow of the decryption program, including grid search and optimization.
    """
    encrypted_text = load_encrypted_book("encrypted_book.txt")

    # Perform frequency analysis
    bigrams = ngram_analysis(encrypted_text, n=2)
    trigrams = ngram_analysis(encrypted_text, n=3)
    quadgrams = ngram_analysis(encrypted_text, n=4)

    # Initial hyperparameters
    initial_temp = 1000
    cooling_rate = 0.99
    iterations = 1000
    weights = {'bigram': 0.4, 'trigram': 0.4, 'quadgram': 0.2}

    # Perform grid search (you can adjust the range for grid search)
    best_decrypted = None
    best_score = float('-inf')
    best_hyperparameters = {}

    for temp in [500, 1000, 1500]:
        for rate in [0.98, 0.99, 0.995]:
            for iters in [500, 1000, 1500]:
                print(f"Testing parameters: Temp={temp}, CoolingRate={rate}, Iterations={iters}")

                decrypted_text, score, _ = simulated_annealing(
                    encrypted_text, bigrams, trigrams, quadgrams, weights, temp, rate, iters)

                if score > best_score:
                    best_decrypted = decrypted_text
                    best_score = score
                    best_hyperparameters = {
                        'initial_temp': temp,
                        'cooling_rate': rate,
                        'iterations': iters
                    }

    # Save the best-decrypted text and hyperparameters to a file
    save_results("decrypted_results.txt", best_decrypted, best_hyperparameters)


if __name__ == "__main__":
    main()
