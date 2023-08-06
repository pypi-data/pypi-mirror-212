import matplotlib.pyplot as plt
from .color_print import print_color

def per_base_n_content(seqs):
    """
    Calculate the percentage of 'N' at each position in the given sequences.

    :param seqs: list of sequences
    :type seqs: list of str
    :return: List of N content percentages, count of positions with greater than 10% and 20% N content
    :rtype: list of float, int, int
    """
    greater_20 = 0
    greater_10 = 0
    
    n_content = []

    max_length = max(len(seq) for seq in seqs)

    # Loop over each position up to the maximum length
    for i in range(max_length):
        n_count = 0
        
        # Loop over each sequence and count the 'N's at this position
        for seq in seqs:
            if i < len(seq) and seq[i] == 'N':
                n_count += 1
        
        # Calculate the percentage of 'N' at this position and add it to our n_content list
        n_content.append(n_count / len(seqs) * 100)

        if n_content[-1] > 20:
            greater_20 += 1
        if n_content[-1] > 10:
            greater_10 += 1

    return n_content, greater_10, greater_20

def plot_n_content(n_content,sub_directory_path):
    """
    Plot the 'N' content as a function of position in the read.

    :param n_content: list of N content percentages
    :type n_content: list of float
    :param sub_directory_path: The directory path where the plot will be saved
    :type sub_directory_path: str
    """
    # Create the x-values for our plot (the position in the read)
    x_values = list(range(1, len(n_content)+1))

    plt.figure()

    # Plot the 'N' content
    plt.plot(x_values, n_content, label='N')

    plt.xlabel('Position in read (bp)')
    plt.ylabel('N content (%)')
    plt.ylim(0, 100)
    plt.legend()

    plt.savefig(f"{sub_directory_path}/per_base_N_content_plot.png")
    #plt.show()

def run_pbnc5(seqs,sub_directory_path):
    """
    Execute the sequence analysis for 'N' content. This includes calculating 'N' content, plotting and printing 
    warnings/failures based on thresholds.

    :param seqs: list of sequences
    :type seqs: list of str
    :param sub_directory_path: The directory path where the plot will be saved
    :type sub_directory_path: str
    :return: True if the analysis passes, False otherwise
    :rtype: bool
    """
    content, greater_10, greater_20 = per_base_n_content(seqs)
    plot_n_content(content,sub_directory_path)
    if (greater_20>0):
        print_color(f"X | Per base N content NOT pass. {greater_20} positions with greater than 20% N content", "red")
        return False
    elif (greater_10):  
        print_color(f"- | Per base N content warning. {greater_10} positions with greater than 10% N content", "yellow")
        return False
    else:
        print_color(f"O | Per base N content pass. No positions with greater than 10% N content", "green")
        return True
