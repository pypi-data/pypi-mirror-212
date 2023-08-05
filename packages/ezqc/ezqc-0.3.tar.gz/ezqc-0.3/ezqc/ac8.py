import matplotlib.pyplot as plt
from .color_print import print_color

adapters = {
    'Illumina Universal Adapter': 'AGATCGGAAGAG',
    'Illumina Small RNA 3\' Adapter': 'TGGAATTCTCGG',
    'Illumina Small RNA 5\' Adapter': 'GATCGTCGGACT',
    'SOLiD Small RNA Adapter': 'CTGCTGTACGGCCAAGGCG'
}

def calculate_adapter_content(sequences, adapters):

    counts = {name: [0]*len(sequences) for name, seq in adapters.items()}

    curr = 0
    for seq in sequences:
        for name, adapter in adapters.items():
            if len(seq) >= len(adapter):
                for i in range(len(seq) - len(adapter) + 1):
                    if seq[i:i+len(adapter)] == adapter:
                        counts[name][curr] += 1
        curr += 1

    percentages = {name: [count/len(sequences)*100 for count in count_list] for name, count_list in counts.items()}

    all_pass = True
    for name, percentage in percentages.items():
        if max(percentage) > 10:
            print_color(f'X | {name} is present in more than 10% of all reads','red')
            all_pass = False
        elif (max(percentage) > 5):
            print_color(f'- | {name} is present in more than 5% of all reads','yellow')
            all_pass = False
    if (all_pass):
        print_color(f'O | No adaptor is present in more than 5% of all reads','green')

    return percentages, all_pass

def plot_adapter_content(adapter_percentages,sub_directory_path):
    plt.figure()
    positions = list(range(1, max(map(len, adapter_percentages.values())) + 1))

    for name, percentages in adapter_percentages.items():
        plt.plot(positions[:len(percentages)], percentages, label=name)

    plt.xlabel('Position in read (bp)')
    plt.ylabel('% Adapter')
    plt.ylim(0, 100)
    plt.title('Adapter Content')
    plt.legend()

    # Save and/or display the plot
    plt.savefig(f"{sub_directory_path}/adaptor_content_plot.png")
    #plt.show()

def run_ac8(seqs,sub_directory_path):
    adapter_percentages, all_pass = calculate_adapter_content(seqs, adapters)
    plot_adapter_content(adapter_percentages,sub_directory_path)
    return all_pass