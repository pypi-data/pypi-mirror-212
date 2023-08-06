import matplotlib.pyplot as plt
from .color_print import print_color
from collections import Counter

def detect_warnings_failures(sequences):
    """
    Detect warnings and failures based on the lengths of the sequences.

    :param sequences: list of sequences
    :type sequences: list of str
    :return: True if no warnings or failures detected, False otherwise
    :rtype: bool
    """
    sequence_lengths = [len(seq) for seq in sequences]
    # Detect warning and failure situations
    if 0 in sequence_lengths:
        print_color("X | Some sequences have zero length.","red")
        return False
    if len(set(sequence_lengths)) > 1:
        print_color("- | Not all sequences are of the same length.","yellow")
        return False
    else:
        print_color("O | Lengths of Sequences are good","green")
        return True

# version 2
def run_sld6(sequences,sub_directory_path):
    """
    Execute the sequence analysis for sequence length distribution. This includes plotting the distribution and 
    checking for warnings/failures.

    :param sequences: list of sequences
    :type sequences: list of str
    :param sub_directory_path: The directory path where the plot will be saved
    :type sub_directory_path: str
    :return: True if the analysis passes, False otherwise
    :rtype: bool
    """
    sequence_lengths = [len(seq) for seq in sequences]
    length_freq = Counter(sequence_lengths)
    
    # separate keys and values for plotting, but sort them by sequence length
    if len(length_freq) == 1:
        unique_length = list(length_freq.keys())[0]
        
        # Add the adjacent lengths with frequency 0
        length_freq[unique_length - 1] = 0
        length_freq[unique_length + 1] = 0

    # separate keys and values for plotting, but sort them by sequence length
    lengths, freqs = zip(*sorted(length_freq.items()))
    # lengths = list(length_freq.keys())
    # freqs = list(length_freq.values())
    plt.figure(figsize=(10,6))
    plt.plot(lengths, freqs, marker='o')
    plt.title('Distribution of sequence lengths over all sequences')
    plt.xlabel('Sequence length(bp)')
    plt.ylabel('Count of sequences')
    plt.grid(True)
    plt.savefig(f"{sub_directory_path}/Sequence_Length_Distribution.png")
    # plt.show()

    return detect_warnings_failures(sequences)

