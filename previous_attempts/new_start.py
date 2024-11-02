import string
from collections import Counter

# Step 1: Load the encrypted book
def load_encrypted_book(filename):
    with open(filename, "r") as file:
        return file.read()

# Step 2: Perform frequency analysis on the text
def frequency_analysis(text):
    # Remove non-letter characters and count frequency of each letter
    letters_only = [char.lower() for char in text if char.isalpha()]
    return Counter(letters_only)

# Step 3: Substitute based on initial mapping
def substitute_text(text, substitution_dict):
    # Create translation table for both lowercase and uppercase letters
    table = str.maketrans(substitution_dict)
    return text.translate(table)

# Step 4: Manual mapping for refinement
def refine_mapping():
    # You can start with an initial guess and refine it
    # This is where you can adjust the mapping based on decrypted content
    # Example: Assume most frequent letter is 'E', and map accordingly
    substitution_dict = {
        'x': 'e',  # Example of mapping 'x' to 'e'
        # Add more mappings as you refine them
    }
    return substitution_dict

# Step 5: Main function to break the cipher
def break_cipher(filename):
    encrypted_text = load_encrypted_book(filename)
    
    # Perform frequency analysis
    freq = frequency_analysis(encrypted_text)
    print("Frequency Analysis:")
    print(freq.most_common())  # Print most frequent letters
    
    # Get an initial substitution dictionary
    substitution_dict = refine_mapping()
    
    # Decrypt text using substitution
    decrypted_text = substitute_text(encrypted_text, substitution_dict)
    
    print("Decrypted Text (so far):")
    print(decrypted_text[:500])  # Print first 500 characters to inspect

# Run the cipher breaker on the file
break_cipher("encrypted_book.txt")