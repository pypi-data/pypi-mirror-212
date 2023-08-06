import numpy as np
import matplotlib.pyplot as plt
from .color_print import print_color

threshold = 24

def find_largest_range(numbers):
    """
    This function finds the largest continuous range in a sorted list of numbers.

    :param numbers: A sorted list of numbers
    :type numbers: list
    :return: The start and end of the largest continuous range in the input list
    :rtype: tuple
    """
    start = end = max_start = max_end = 0
    max_length = 0

    for i in range(1, len(numbers)):
        if numbers[i] == numbers[i-1] + 1:
            end = i
        else:
            length = end - start + 1
            if length > max_length:
                max_length = length
                max_start = start
                max_end = end
            start = end = i

    # Check if the last range is the largest
    length = end - start + 1
    if length > max_length:
        max_length = length
        max_start = start
        max_end = end

    return numbers[max_start], numbers[max_end]


def phred33_to_q(quality_str):
    """
    This function converts a Phred+33 ASCII-encoded quality string to a list of quality scores.

    :param quality_str: The Phred+33 encoded quality string
    :type quality_str: str
    :return: The quality scores
    :rtype: numpy.array
    """
    return np.array([ord(ch) - 33 for ch in quality_str])

def calculate_quality_scores(quality_strings):
    """
    This function calculates quality scores from a list of quality strings.

    :param quality_strings: A list of Phred+33 encoded quality strings
    :type quality_strings: list
    :return: The quality scores and a mask array
    :rtype: tuple of numpy.array
    """
    num_sequences = len(quality_strings)
    max_length = max(len(qstr) for qstr in quality_strings)
    quality_scores = np.zeros((num_sequences, max_length))
    mask = np.zeros_like(quality_scores, dtype=bool)

    for i, qstr in enumerate(quality_strings):
        scores = phred33_to_q(qstr)
        quality_scores[i, :len(scores)] = scores
        mask[i, :len(scores)] = True
    
    return quality_scores, mask

def run_pbsq1(quality_strings,sub_directory_path):
    """
    This function calculates and plots quality scores from a list of quality strings, and saves the plot to a specified path. 
    It also checks whether the quality scores meet a certain threshold.

    :param quality_strings: A list of Phred+33 encoded quality strings
    :type quality_strings: list
    :param sub_directory_path: The path where the plot will be saved
    :type sub_directory_path: str
    :return: True if the quality scores meet the threshold, False otherwise
    :rtype: bool
    """
    quality_scores, mask = calculate_quality_scores(quality_strings)

    max_read_length = quality_scores.shape[1]

    # Calculate average, lower quartile, and upper quartile quality scores for each base position
    masked_quality_scores = np.ma.masked_array(quality_scores, ~mask)
    average_quality_scores = masked_quality_scores.mean(axis=0).data
    lower_quartile_scores = np.ma.apply_along_axis(lambda x: np.percentile(x.compressed(), 25), 0, masked_quality_scores)
    upper_quartile_scores = np.ma.apply_along_axis(lambda x: np.percentile(x.compressed(), 75), 0, masked_quality_scores)

    # Create the plot
    positions = np.arange(1, max_read_length+1)
    plt.figure()
    plt.plot(positions, average_quality_scores, label='Mean')
    plt.plot(positions, lower_quartile_scores, label='Lower quartile', linestyle='--')
    plt.plot(positions, upper_quartile_scores, label='Upper quartile', linestyle='--')

    plt.xlabel('Position in read (bp)')
    plt.ylabel('Quality score')
    plt.title('Per base sequence quality plot')
    plt.xticks(np.arange(1, max_read_length+1, max(1, max_read_length//15)))  # Adjust x-axis tick spacing
    plt.yticks(np.arange(0, np.max(average_quality_scores)+1, 2))
    plt.grid(True)
    plt.legend()
    plt.savefig(f"{sub_directory_path}/per_base_sequence_quality_plot.png")
    # plt.show()

    avg_score = np.average(average_quality_scores)

    if avg_score < threshold*0.75:
        print_color(f"X | Per base sequence quality NOT pass. Low average quality score of {avg_score:.2f}", "red")
        return False
    elif np.all(average_quality_scores >= threshold):
        print_color(f"O | Per base sequence quality pass. With high average quality score of {avg_score:.2f}", "green")
        return True
    else:
        indices_above_threshold = np.where(average_quality_scores >= threshold)[0]
        start, end = find_largest_range(indices_above_threshold)
        print_color(f"- | Per base sequence quality can be improved. With high quality reads from position {start} to {end}", "yellow")
        return False
