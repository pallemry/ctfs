from pathlib import Path
from collections import Counter
import matplotlib.pyplot as plt
import numpy
import urllib.parse

def plot_number_frequencies(numbers, color='skyblue', title='Frequency of Numbers'):
    """
    Counts duplicates in a list of numbers and plots their frequencies.
    
    Parameters:
    numbers (list): A list of integers or floats with duplicate values.
    color (str): The color of the bars (default is 'skyblue').
    title (str): The main title of the plot.
    """
    if not numbers:
        print("The list is empty. Nothing to plot.")
        return

    # 1. Count the frequencies of each unique number
    counts = Counter(numbers)
    
    # 2. Extract and sort by the unique numbers (X-axis) so the plot reads left-to-right
    sorted_unique_numbers = sorted(counts.keys())
    frequencies = [counts[num] for num in sorted_unique_numbers]
    
    # 3. Initialize the plot layout
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # 4. Generate the bar chart
    ax.bar(sorted_unique_numbers, frequencies, color=color, edgecolor='black', zorder=2)
    
    # 5. Customize titles and axis labels
    ax.set_title(title, fontsize=14, pad=15)
    ax.set_xlabel("Unique Values", fontsize=12)
    ax.set_ylabel("Frequency (Count)", fontsize=12)
    
    # Ensure every single unique number gets an X-axis label
    ax.set_xticks(sorted_unique_numbers)
    
    # Add a clean grid behind the bars for easier reading
    ax.grid(axis='y', linestyle='--', alpha=0.7, zorder=1)
    
    # 6. Display the plot
    plt.show()

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def main() -> None:
    cipher = Path("cipher").read_text()
    parts = [int(part) for part in cipher.split('.') if len(part) > 0]
    assert len(parts) % 3 == 0

    sums = [sum(chunk) for chunk in chunks(parts, 3)]

    for password_guess in range(717, 845):
        decrypted_letters = [encrypted_sum - password_guess for encrypted_sum in sums]
        if not all(x > 0 and x < 255 for x in decrypted_letters):
            continue
        decrypted = bytes(decrypted_letters)
        print(decrypted)
    
    plot_number_frequencies(parts)

    print(len(parts), len(parts) / 3)


if __name__ == "__main__":
    main()