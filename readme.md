# Break the Substitution Cipher

An experimental Python project for attacking a monoalphabetic substitution cipher. It began with straightforward letter-frequency guesses and grew into a collection of hill-climbing, simulated-annealing, n-gram-scoring, and hyperparameter-search experiments.

> **In short:** the current higher-n-gram experiment can produce readable passages, but it does not reliably recover every letter in the book. Its search is stochastic, its score is a lightweight heuristic, and the full parameter sweep can take a long time.

## What is in this repository?

| File or folder | Purpose |
| --- | --- |
| [`encrypted_book.txt`](encrypted_book.txt) | Ciphertext used by the experiments. |
| [`break_substitution_simulated_annealing_higher_ngrams_integrated.py`](break_substitution_simulated_annealing_higher_ngrams_integrated.py) | The current higher-n-gram simulated-annealing and grid-search experiment. |
| [`final_attempt_best_results.py`](final_attempt_best_results.py) | Another saved, runnable experiment from the development process. |
| [`results.txt`](results.txt) | Sample output excerpts from several attempts; useful for comparing their characteristic errors. |
| [`previous_attempts/`](previous_attempts/) | The broader experiment archive, including unsuccessful approaches and their output. |
| [`previous_worthy_steps/`](previous_worthy_steps/) | Approaches and intermediate versions worth keeping for future cipher-solving work. |

The archives are part of the project, not clutter to discard: even a failed run can be a useful starting point for a different ciphertext or scoring model.

## How the approach developed

The saved scripts and repository history show a gradual move from simple statistical guesses toward a more expensive search:

1. **Start with letter frequencies.** The first versions compare ciphertext letter frequencies with typical English frequencies and build an initial substitution guess. This is fast, but individual-letter statistics do not capture word context; several letters can have similar frequencies, leaving ambiguous or incorrect mappings.
2. **Refine mappings with hill climbing.** Later attempts swap letters in the guessed mapping and keep changes that improve a text score. This gives the search a way to improve beyond a one-shot frequency guess, but it can get stuck in a local optimum.
3. **Add simulated annealing.** The search was extended to sometimes accept a worse-scoring swap, with the chance controlled by a temperature that cools over time. Early exploration can escape some local optima; later iterations become more selective.
4. **Use letter sequences, not just individual letters.** Scoring evolved from digraphs (2-letter sequences) to trigrams, then quadgrams and pentagrams. Experiments also adjusted the relative weights and tried penalties for unlikely sequences.
5. **Combine methods and tune parameters.** The archive includes combined hill-climbing/simulated-annealing approaches and grid searches over n-gram weights, starting temperature, and cooling rate. The search became more systematic, but also much more computationally expensive.
6. **Keep the trail.** Both [`previous_attempts/`](previous_attempts/) and [`previous_worthy_steps/`](previous_worthy_steps/) preserve the intermediate scripts. The [`results.txt`](results.txt) excerpts illustrate the progression: some outputs contain recognizable English while still making widespread substitution errors.

This is an experimental path rather than a claim that every added technique improved every result. In particular, a higher score under one of these heuristic functions does not necessarily mean a more accurate decryption.

<details>
<summary>Browse the preserved attempts and worthy steps</summary>

The attempt archive contains:

- [`break_substitution_first_attempt.py`](previous_attempts/break_substitution_first_attempt.py)
- [`break_substitution_second_attempt.py`](previous_attempts/break_substitution_second_attempt.py)
- [`new_start.py`](previous_attempts/new_start.py) and [`new_start_2.py`](previous_attempts/new_start_2.py)
- [`hill_climbing_algorithm.py`](previous_attempts/hill_climbing_algorithm.py)
- [`hill_climbing_with_simulated_annealing.py`](previous_attempts/hill_climbing_with_simulated_annealing.py)
- [`break_substitution_trigram_simulated_annealing.py`](previous_attempts/break_substitution_trigram_simulated_annealing.py)
- [`break_substitution_trigram_adjust_weight_digraph_trigram.py`](previous_attempts/break_substitution_trigram_adjust_weight_digraph_trigram.py)
- [`break_substitution_penalty_grid_search_bi-trigram-weight.py`](previous_attempts/break_substitution_penalty_grid_search_bi-trigram-weight.py)
- [`break_substitution_grid_search_all_hyperparameters_bigraphs_trigrams_hill_climbing_simulated_annealing_combined.py`](previous_attempts/break_substitution_grid_search_all_hyperparameters_bigraphs_trigrams_hill_climbing_simulated_annealing_combined.py)
- [`brek_substitution_digraph_trigram_hill_climbing_simulated_annealing_grid_search.py`](previous_attempts/brek_substitution_digraph_trigram_hill_climbing_simulated_annealing_grid_search.py)
- [`break_substitution_simulated_annealing_higher_ngrams_integrated.py`](previous_attempts/break_substitution_simulated_annealing_higher_ngrams_integrated.py)
- [`break_substitution_finally.py`](previous_attempts/break_substitution_finally.py) and [`break_substitution_finally_2.py`](previous_attempts/break_substitution_finally_2.py)
- [`break_substitutionthi.py`](previous_attempts/break_substitutionthi.py)
- [`results.txt`](previous_attempts/results.txt) and [`decrypted_results.txt`](previous_attempts/decrypted_results.txt)

The separate worthy-steps archive keeps:

- [`break_substitution_first_attempt.py`](previous_worthy_steps/break_substitution_first_attempt.py), [`break_substitution_second_attempt.py`](previous_worthy_steps/break_substitution_second_attempt.py), and [`break_substitution_finally_2.py`](previous_worthy_steps/break_substitution_finally_2.py)
- [`new_start.py`](previous_worthy_steps/new_start.py) and [`new_start_2.py`](previous_worthy_steps/new_start_2.py)
- [`hill_climbing_algorithm.py`](previous_worthy_steps/hill_climbing_algorithm.py) and [`hill_climbing_with_simulated_annealing.py`](previous_worthy_steps/hill_climbing_with_simulated_annealing.py)
- [`break_substitution_trigram_simulated_annealing.py`](previous_worthy_steps/break_substitution_trigram_simulated_annealing.py)
- [`break_substitution_trigram_adjust_weight_digraph_trigram.py`](previous_worthy_steps/break_substitution_trigram_adjust_weight_digraph_trigram.py)
- [`break_substitution_penalty_grid_search_bi-trigram-weight.py`](previous_worthy_steps/break_substitution_penalty_grid_search_bi-trigram-weight.py)
- [`break_substitution_grid_search_all_hyperparameters_bigraphs_trigrams_hill_climbing_simulated_annealing_combined.py`](previous_worthy_steps/break_substitution_grid_search_all_hyperparameters_bigraphs_trigrams_hill_climbing_simulated_annealing_combined.py)
- [`brek_substitution_digraph_trigram_hill_climbing_simulated_annealing_grid_search.py`](previous_worthy_steps/brek_substitution_digraph_trigram_hill_climbing_simulated_annealing_grid_search.py)
- [`break_substitution_finally.py`](previous_worthy_steps/break_substitution_finally.py)

</details>

## How the current experiment works

The main script, [`break_substitution_simulated_annealing_higher_ngrams_integrated.py`](break_substitution_simulated_annealing_higher_ngrams_integrated.py), follows this loop:

1. **Read the ciphertext** from `encrypted_book.txt`.
2. **Create a random one-to-one letter mapping** for the alphabet. The same mapping is applied consistently throughout the text, preserving punctuation, spacing, and line breaks.
3. **Score the candidate plaintext** by counting occurrences of small, hand-written English lists of digraphs, trigrams, quadgrams, and pentagrams, applying a configurable weight to each size, and subtracting a small penalty for a few unlikely pairs.
4. **Try neighboring keys** by swapping two mapped letters. A better score is accepted; a worse one may also be accepted depending on the current simulated-annealing temperature.
5. **Repeat with different settings.** The grid search tries 3 values for each of four n-gram weights, 3 starting temperatures, and 3 cooling rates: **729 parameter combinations**, each with up to 1,000 swap iterations (with an early stop when the temperature gets low).
6. **Keep the best-scoring candidate** seen in the sweep, print its first 500 characters and chosen settings, and write up to the first 100,000 characters of the candidate plus the settings to `decryption_results_simulated_annealing_higher_ngrams_integrated.txt` in the current directory.

The search uses Python's random number generator without a fixed seed, so successive runs may produce different results.

## Run it from the command line

The project uses only Python's standard library; there are no third-party packages to install. Clone the repository and move into its directory:

```bash
git clone https://github.com/cbdmatze/break_the_substitution_cipher.git
cd break_the_substitution_cipher
```

Run the higher-n-gram experiment with Python 3:

```bash
python3 break_substitution_simulated_annealing_higher_ngrams_integrated.py
```

The script expects `encrypted_book.txt` in the current working directory, so run it from the repository root as shown. It currently has no command-line options: the parameter ranges and iteration limit are defined in the script. The full 729-combination sweep can take **hours**, depending on the machine and input length. The result file is written in the directory from which the command is run and is overwritten by a later run.

To try the other saved root-level experiment instead:

```bash
python3 final_attempt_best_results.py
```

That file is a separate experiment, not a command-line wrapper for the main script; inspect its settings and expected input before running it.

## Reading the results

- **The preview in the terminal** is only the first 500 characters of the best candidate found. The generated result file contains at most the first 100,000 characters, plus the selected n-gram weights, temperature, and cooling rate; it may not contain the whole book.
- **A higher score** means that the candidate matched more of the scorer's listed sequences under the selected weights. It is a relative search score—not a probability, a percentage of letters recovered, or proof that the plaintext is correct.
- **Judge the text in context.** Look for coherent words and sentences across multiple passages. A candidate can look plausible in a short excerpt while containing many wrong letters elsewhere.
- **Expect run-to-run variation.** Random initial mappings and swaps mean that separate runs can settle on different candidates. Comparing several runs can be informative, but does not by itself establish correctness.
- **Use the archives as comparisons, not ground truth.** The samples in `results.txt` are excerpts from prior attempts and show both partial progress and remaining errors.

## Current limitation and next step

The present scorer only uses a small, manually selected set of English n-grams, up to 5 letters long. That is a useful prototype, but it misses much of the information in real English and can favor a candidate that happens to contain the chosen patterns.

To make the decryption substantially more reliable—especially across an entire book—the next major improvement would be to integrate a **much richer, corpus-derived n-gram language model**, including more higher-order n-grams (for example, quadgrams and longer sequences), with normalized log-probability scoring rather than just counting a short fixed list. That would give the search more linguistic evidence to distinguish plausible mappings. It would still be a heuristic search, so perfect recovery is not guaranteed; validation against known plaintext or other independent evidence would remain valuable.

## A note on runtime

The expensive runtime is a direct consequence of repeatedly scoring long candidate texts across a broad parameter grid. Reducing the grid or iteration count can make experiments quicker, but may also change the quality of the best candidate. The archived scripts document earlier trade-offs and may be useful when exploring more efficient scoring or search strategies.
