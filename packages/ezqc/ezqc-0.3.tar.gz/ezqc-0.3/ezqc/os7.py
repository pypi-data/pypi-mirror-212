import collections
import csv
from .color_print import print_color

def run_os7(dna_sequences,sub_directory_path):
    # Track only the first 100,000 sequences
    dna_sequences = dna_sequences[:100000] if len(dna_sequences)>100000 else dna_sequences

    # Truncate sequences over 75bp to 50bp for analysis
    dna_sequences = [seq[:50] if len(seq) > 75 else seq for seq in dna_sequences]

    total_count = len(dna_sequences)
    
    counter = collections.Counter(dna_sequences)
    
    table = []
    
    sequences_exceeding_1_percent = 0
    sequences_exceeding_0_1_percent = 0

    for sequence, count in counter.items():
        percentage = (count / total_count) * 100

        if percentage > 1:
            sequences_exceeding_1_percent += 1
            table.append([sequence, count, percentage])

        elif percentage > 0.1:
            sequences_exceeding_0_1_percent += 1
            table.append([sequence, count, percentage])

    with open(f"{sub_directory_path}/overrepresented_sequences.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Sequence", "Count", "Percentage"])
        writer.writerows(table)

    if (sequences_exceeding_1_percent > 0):
        print_color(f"X | Overrepresented sequences NOT pass. {sequences_exceeding_1_percent} sequences representing more than 1% of the total", "red")
        return False
    elif (sequences_exceeding_0_1_percent > 0):
        print_color(f"- | Overrepresented sequences warning. {sequences_exceeding_0_1_percent} sequences representing more than 0.1% of the total", "yellow")
        return False
    else:
        print_color(f"O | Overrepresented sequences pass. No sequences representing more than 0.1% of the total", "green")
        return True
