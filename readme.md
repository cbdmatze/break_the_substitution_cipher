The folder "previous_attempts"  contains all approaches that were necessary to come to such a project in the end....you can get an impression of my way to approach to that code problem and all the attempts were saved because in other code issues similar to this one breaking a classic substitution cipher they could provide sexy results...I have to warn you in advance....this program takes several hours to evaluate the best hyperparameters....but to be honest....that is not my problem...but yours....!! Have a lot of fun....and please don't be to hard to me when it comes to grading that shit...!!!



Cipher Breaker using Simulated Annealing and N-Gram Analysis

Overview

This project demonstrates how to decrypt a substitution cipher using a grid search of hyperparameters and simulated annealing to optimize the solution. The program attempts to recover plaintext from encrypted text where the substitution cipher is unknown. It uses statistical analysis of n-grams (common letter combinations in the English language) to evaluate potential solutions.

The key components of the project include:

	1.	Loading the encrypted text.
	2.	Decrypting the text using a random substitution mapping.
	3.	Evaluating the quality of the decryption using n-gram analysis.
	4.	Optimizing the decryption through simulated annealing, a probabilistic method for finding an approximate solution.
	5.	Performing a grid search to explore different sets of hyperparameters to maximize decryption accuracy.

How the Code Works

1. Loading the Encrypted Text

The load_encrypted_book function reads the encrypted text from a file. This text is assumed to be encrypted using an unknown substitution cipher, where each letter in the alphabet has been replaced with another letter.

2. Substitution Cipher and Text Substitution

In a substitution cipher, each letter of the alphabet is mapped to a different letter. For example, all instances of ‘A’ in the plaintext might be replaced with ‘X’ in the ciphertext. The function substitute_text performs this substitution on the encrypted text given a dictionary that maps letters from the ciphertext to guessed plaintext letters.

3. N-Gram Analysis for Evaluation

The core evaluation method of this decryption is based on n-grams. An n-gram is a sequence of n characters that often appear together in a language. Common examples include:

	•	Digraphs (2-grams): like “th”, “he”, “in”.
	•	Trigrams (3-grams): like “the”, “and”, “ing”.
	•	Quadgrams (4-grams): like “tion”, “ment”.
	•	Pentagrams (5-grams): like “ation”, “there”.

The function evaluate_decryption uses a weighted sum of the number of n-grams that appear in the decrypted text, giving more weight to higher n-grams (such as quadgrams and pentagrams) because these are less frequent and more informative of the correctness of a decryption.

Penalties are also applied for unlikely sequences of letters, which helps eliminate mappings that produce nonsensical text.

4. Simulated Annealing for Optimization

The heart of the decryption process lies in the use of simulated annealing, a probabilistic technique used to find an approximate solution to optimization problems. The steps are as follows:

	•	Initialization: The process starts with a random substitution mapping of letters.
	•	Neighboring Solution: At each iteration, a new potential solution is generated by swapping two letters in the current mapping.
	•	Evaluation: The new solution is evaluated using n-gram analysis.
	•	Acceptance Criteria: The new solution is accepted if it improves the score. Otherwise, it is accepted with a probability that decreases as the score difference becomes larger and as the temperature decreases. This acceptance of worse solutions allows the algorithm to escape local optima.
	•	Cooling: The temperature gradually decreases over time, reducing the likelihood of accepting worse solutions. The process ends when the temperature drops below a set threshold or a maximum number of iterations is reached.

The function simulated_annealing_with_ngrams implements this process.

5. Grid Search over Hyperparameters

To maximize the accuracy of the decryption, various hyperparameters such as weights for n-grams, temperature, and cooling rates are tested. This is done using a grid search in the grid_search function, which systematically explores combinations of the following hyperparameters:

	•	n-gram weights: How much weight to give to each n-gram (digraph, trigram, quadgram, pentagram) in the evaluation.
	•	Temperature: The starting temperature for simulated annealing.
	•	Cooling rate: The rate at which the temperature decreases during the annealing process.

The best set of hyperparameters is chosen based on the score of the decrypted text.

6. Final Output

After finding the best mapping and hyperparameters, the program outputs:

	•	The best decrypted text.
	•	The combination of hyperparameters that resulted in the best decryption.

The final result is printed to the console, and the decrypted text (along with the best hyperparameters) is saved to a file named decryption_results_simulated_annealing_higher_ngrams_integrated.txt.

Key Concepts Behind the Code

1. Substitution Cipher

A substitution cipher is a type of encryption where each letter of the plaintext is replaced with a corresponding letter in the ciphertext. The challenge in solving a substitution cipher is to recover the original mapping, i.e., which letter in the ciphertext corresponds to which letter in the plaintext.

2. Simulated Annealing

Simulated annealing is inspired by the process of heating and cooling materials to reach a low-energy, stable state. It is used here to find the most probable letter mapping by:

	•	Starting from a random mapping.
	•	Gradually improving it by exploring neighboring mappings.
	•	Accepting worse mappings with decreasing probability to escape local optima.

3. N-Gram Analysis

In natural language, certain combinations of letters are more likely to occur than others. For example, in English, “th” is much more common than “zx”. N-gram analysis uses these patterns to assess the likelihood that a given decryption is correct. The more common n-grams a decrypted text has, the more likely it is to be close to the original plaintext.

4. Grid Search

Grid search is a brute-force method of hyperparameter tuning. It tries all combinations of the hyperparameters within the specified ranges and selects the one that produces the best result. In this case, it searches for the best combination of n-gram weights, temperature, and cooling rate for simulated annealing.

Considerations for Decrypting a Substitution Cipher

When attempting to decrypt a substitution cipher, several key considerations must be made:

	1.	Language Properties:
	•	Every language has common letter patterns, both in terms of individual letter frequencies (e.g., ‘E’ is the most common letter in English) and letter combinations (like digraphs, trigrams, etc.).
	•	Understanding these patterns helps guide the decryption process.
	2.	Statistical Patterns:
	•	Substitution ciphers are vulnerable to frequency analysis, where the frequencies of letters in the ciphertext are compared to known letter frequencies in the language.
	•	This project takes frequency analysis further by also considering the frequency of n-grams.
	3.	Heuristic Optimization:
	•	Since trying all possible mappings is computationally infeasible (there are ￼ possible mappings), heuristic optimization methods like simulated annealing are used to find a good solution without trying every possibility.
	4.	Hyperparameter Tuning:
	•	The success of simulated annealing heavily depends on the choice of hyperparameters (e.g., initial temperature, cooling rate). Grid search is used to systematically explore different hyperparameter combinations and find the optimal configuration.

Running the Code

To run the program, simply call the break_cipher_with_grid_search function with the filename of the encrypted text as an argument:

break_cipher_with_grid_search("encrypted_book.txt")

Make sure that the encrypted text file (encrypted_book.txt) is in the same directory as the script.

Conclusion

This project provides a robust method for decrypting substitution ciphers by leveraging the power of n-gram analysis and simulated annealing. It explores various hyperparameter configurations through grid search to find the best decryption possible. The combination of statistical analysis and probabilistic optimization offers an effective approach to breaking classical ciphers.

