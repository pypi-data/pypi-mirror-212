import matplotlib.pyplot as plt
from .color_print import print_color


def per_base_sequence_content(seqs):
    """
    This function calculates the percentage content of each base at each position in the sequences.

    :param seqs: A list of sequences
    :type seqs: list
    :return: A tuple containing a dictionary of base contents, count of positions with greater than 10% differences, 
             and count of positions with greater than 20% differences
    :rtype: tuple
    """
    greater_20 = 0
    greater_10 = 0

    base_content = {'A': [], 'T': [], 'C': [], 'G': []}

    max_length = max(len(seq) for seq in seqs)

    # Loop over each position up to the maximum length
    for i in range(max_length):
        pos_counts = {'A': 0, 'T': 0, 'C': 0, 'G': 0, 'N': 0}
        
        # Loop over each sequence and count the bases at this position
        for seq in seqs:
            if i < len(seq):
                pos_counts[seq[i]] += 1
        
        # Calculate the percentage of each base at this position and add it to our base_content dictionary
        total_count = sum(pos_counts.values())
        for base in base_content.keys():
            base_content[base].append(pos_counts[base] / total_count * 100)
        
        if abs(base_content['A'][-1] - base_content['T'][-1]) > 20 or abs(base_content['G'][-1] - base_content['C'][-1]) > 20:
            greater_20 += 1
        if abs(base_content['A'][-1] - base_content['T'][-1]) > 10 or abs(base_content['G'][-1] - base_content['C'][-1]) > 10:
            greater_10 += 1

    return base_content, greater_10, greater_20



def plot_base_content(base_content,sub_directory_path):
    """
    This function plots the base content for each base at each position in the read and saves the plot to a file.

    :param base_content: A dictionary where the keys are the bases and the values are lists of percentages for each position
    :type base_content: dict
    :param sub_directory_path: The directory path where the plot will be saved
    :type sub_directory_path: str
    """
    # Create the x-values for our plot (the position in the read)
    x_values = list(range(1, len(base_content['A'])+1))

    plt.figure()

    # Plot the base content for each base 
    for base, y_values in base_content.items():
        plt.plot(x_values, y_values, label=base)

    plt.xlabel('Position in read (bp)')
    plt.ylabel('Base content (%)')
    plt.ylim(0, 100)
    plt.legend()

    plt.savefig(f"{sub_directory_path}/per_base_sequence_content_plot.png")
    #plt.show()

def run_pbsc3(seqs,sub_directory_path):
    """
    This function runs the per base sequence content analysis on a set of sequences, plots the results, and checks for significant differences.

    :param seqs: A list of sequences
    :type seqs: list
    :param sub_directory_path: The directory path where the plot will be saved
    :type sub_directory_path: str
    :return: True if the analysis passes, False otherwise
    :rtype: bool
    """
    content, greater_10, greater_20 = per_base_sequence_content(seqs)
    plot_base_content(content,sub_directory_path)
    if (greater_20>0):
        print_color(f"X | Per base sequence content NOT pass. {greater_20} positions with greater than 20% differences", "red")
        return False
    elif (greater_10):  
        print_color(f"- | Per base sequence content warning. {greater_10} positions with greater than 10% differences", "yellow")
        return False
    else:
        print_color(f"O | Per base sequence content pass. No positions with greater than 10% differences", "green")
        return True
