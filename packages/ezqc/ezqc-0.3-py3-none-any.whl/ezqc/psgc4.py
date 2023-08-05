import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from .color_print import print_color
# need to pip install scipy

def detect_warnings_failures(gc_contents,sequences):
    mu, std = norm.fit(gc_contents)
    deviations = [abs(content - mu) for content in gc_contents]

    sum_deviation = sum(deviations)

    warning_threshold = 0.15 * len(sequences)
    failure_threshold = 0.30 * len(sequences)

    if sum_deviation > warning_threshold and sum_deviation <= failure_threshold:
        print_color("- | The sum of the deviations from the normal distribution represents more than 15% of the reads.","yellow")
        return False
    elif sum_deviation > failure_threshold:
        print_color("X | The sum of the deviations from the normal distribution represents more than 30% of the reads.","red")
        return False
    else:
        print_color("O | The sum of the deviations from the normal distribution are good","green")
        return True

def run_psgc4(sequences,sub_directory_path):
    gc_contents = []
    # Iterate through each sequence
    for seq in sequences:
        # Compute the GC content for the current sequence
        count_gc = sum(base in "GC" for base in seq)
        gc_percent = 100 * count_gc / len(seq)

        # Append the GC content to the list
        gc_contents.append(gc_percent)
        
    # plot GC distribution over all sequences
    plt.figure(figsize=(10,6))
    plt.hist(gc_contents, bins=100, alpha=0.5, label='Observed GC')

    # calculate and plot theoretical distribution
    mu, sigma = np.mean(gc_contents), np.std(gc_contents)
    s = np.arange(mu - 3.5*sigma, mu + 3.5*sigma, 0.05)
    plt.plot(s, norm.pdf(s, mu, sigma)*len(gc_contents)*(max(gc_contents)-min(gc_contents))/100, label='Theoretical GC')

    plt.title("GC distribution over all sequences")
    plt.xlabel("Mean GC content")
    plt.ylabel("Number of sequences")
    plt.legend(loc='upper right')
    plt.grid(True)
    # Save and/or display the all the plots
    plt.savefig(f"{sub_directory_path}/per_sequence_GC_content.png")
    # plt.show()

    return detect_warnings_failures(gc_contents,sequences)