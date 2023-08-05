from Bio.Blast import NCBIWWW
from Bio import SeqIO

for seq in SeqIO.parse('/Users/sky/Desktop/ezqc/tests/SRR020192.fastq', "fastq"):
  result_handle = NCBIWWW.qblast("blastn", "nt", seq.format("fasta"),
                                format_type="Text")
  print(seq)
  output = result_handle.read()
  print(output)
  break