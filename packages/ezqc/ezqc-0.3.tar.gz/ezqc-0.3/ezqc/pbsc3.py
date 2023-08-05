import matplotlib.pyplot as plt
from .color_print import print_color


def per_base_sequence_content(seqs):
    greater_20 = 0
    greater_10 = 0

    # Initialize a dictionary to hold our counts
    base_content = {'A': [], 'T': [], 'C': [], 'G': []}

    # Determine the length of the longest sequence
    max_length = max(len(seq) for seq in seqs)

    # Loop over each position up to the maximum length
    for i in range(max_length):
        # Initialize a dictionary to hold the counts for this position
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
    # Create the x-values for our plot (the position in the read)
    x_values = list(range(1, len(base_content['A'])+1))

    plt.figure()

    # Plot the base content for each base 
    for base, y_values in base_content.items():
        plt.plot(x_values, y_values, label=base)

    # Add labels and a legend
    plt.xlabel('Position in read (bp)')
    plt.ylabel('Base content (%)')
    plt.ylim(0, 100)
    plt.legend()

    # Save and/or display the plot
    plt.savefig(f"{sub_directory_path}/per_base_sequence_content_plot.png")
    #plt.show()

def run_pbsc3(seqs,sub_directory_path):
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
