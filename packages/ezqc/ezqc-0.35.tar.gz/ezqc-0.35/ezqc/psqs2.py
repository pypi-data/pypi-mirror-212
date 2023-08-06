import numpy as np
import matplotlib.pyplot as plt
from .color_print import print_color

def phred33_to_q(qual_string):
    """
    This function converts a Phred+33 ASCII-encoded quality string to a list of quality scores.

    :param qual_string: The Phred+33 encoded quality string
    :type qual_string: str
    :return: The quality scores
    :rtype: list
    """
    return [ord(ch) - 33 for ch in qual_string]

def mean_qual_score(qual_string):
    """
    This function calculates the mean quality score from a Phred+33 encoded quality string.

    :param qual_string: The Phred+33 encoded quality string
    :type qual_string: str
    :return: The mean quality score
    :rtype: float
    """
    qual_scores = phred33_to_q(qual_string)
    return np.mean(qual_scores)

def run_psqs2(quality_strings,sub_directory_path):
    """
    This function calculates the mean quality scores from a list of quality strings, and then plots the distribution of 
    these mean scores. The plot is saved to a specified path. It also checks whether the proportion of sequences with 
    low quality is greater than 5%.

    :param quality_strings: A list of Phred+33 encoded quality strings
    :type quality_strings: list
    :param sub_directory_path: The path where the plot will be saved
    :type sub_directory_path: str
    :return: True if the proportion of sequences with low quality is less than 5%, False otherwise
    :rtype: bool
    """
    mean_qual_scores = [mean_qual_score(qual_string) for qual_string in quality_strings]

    # Set up bins for the x-axis (mean sequence quality)
    bin_edges = np.arange(0, np.ceil(max(mean_qual_scores)) + 1, 1)

    counts, _ = np.histogram(mean_qual_scores, bins=bin_edges)

    proportion_low_quality = sum(mqs < 20 for mqs in mean_qual_scores) / len(mean_qual_scores)

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.bar(bin_edges[:-1], counts, width=1, edgecolor="k", alpha=0.7)
    plt.xlabel("Mean Sequence Quality(Phred scores)")
    plt.ylabel("Number of Sequences")
    plt.title("Quality Scores distribution over all sequences")
    plt.xticks(bin_edges)
    plt.grid(True, linestyle='--', alpha=0.5)

    plt.savefig(f"{sub_directory_path}/per_sequence_quality_scores.png")
    # plt.show()


    # print(proportion_low_quality)
    if (proportion_low_quality >= 0.05):
        print_color(f"X | Per sequence quality score NOT pass. Because proportion of low quality is {100*proportion_low_quality:.2f} %, which is more than 5%","red")
        return False
    else:
        print_color(f"O | Per sequence quality pass. Proportion of low quality is {100*proportion_low_quality:.2f} %, which is less than 5%","green")
        return True