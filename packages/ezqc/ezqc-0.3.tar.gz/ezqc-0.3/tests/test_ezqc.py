import pytest
import os
import numpy as np
from ezqc.pbsq1 import run_pbsq1
from ezqc.psqs2 import run_psqs2
from ezqc.pbsc3 import run_pbsc3
from ezqc.psgc4 import run_psgc4
from ezqc.pbnc5 import run_pbnc5
from ezqc.sld6 import run_sld6
from ezqc.os7 import run_os7
from ezqc.ac8 import run_ac8

def parse_fastq_file(file_obj):
    while True:
        header = file_obj.readline().strip()
        if not header:
            break
        sequence = file_obj.readline().strip()
        file_obj.readline()
        quality_str = file_obj.readline().strip()
        yield header, sequence, quality_str

headers = []
sequences = []
quality_strings = []

directory_name = "ezqc_output"
# Get the current working directory
current_directory = os.getcwd()
# Create a path for the new directory
new_directory_path = os.path.join(current_directory, directory_name)

# Create the directory if it doesn't already exist
if not os.path.exists(new_directory_path):
    os.makedirs(new_directory_path)
    print(f"Directory '{directory_name}' created successfully!")
else:
    print(f"Directory '{directory_name}' already exists.")


# test 1
with open("tests/SRR020192.fastq", 'r') as fastq_file:
     for header, sequence, quality_str in parse_fastq_file(fastq_file):
        headers.append(header)
        sequences.append(sequence)
        quality_strings.append(quality_str)

def test1_function1_FALSE():
    assert run_pbsq1(quality_strings,directory_name) == False
def test1_function2_TRUE():
    assert run_psqs2(quality_strings,directory_name) == True
def test1_function3_FALSE():
    assert run_pbsc3(sequences,directory_name) == False
def test1_function4_FALSE():
    assert run_psgc4(sequences,directory_name) == False
def test1_function5_TRUE():
    assert run_pbnc5(sequences,directory_name) == True
def test1_function6_FALSE():
    assert run_sld6(sequences,directory_name) == False
def test1_function7_FALSE():
    assert run_os7(sequences,directory_name) == False
def test1_function8_TURE():
    assert run_ac8(sequences,directory_name) == True

#test 2
with open("tests/SRR24755455.fastq", 'r') as fastq_file:
     for header, sequence, quality_str in parse_fastq_file(fastq_file):
        headers.append(header)
        sequences.append(sequence)
        quality_strings.append(quality_str)

def test2_function1_FALSE():
    assert run_pbsq1(quality_strings,directory_name) == False
def test2_function2_TRUE():
    assert run_psqs2(quality_strings,directory_name) == True
def test2_function3_FALSE():
    assert run_pbsc3(sequences,directory_name) == False
def test2_function4_FALSE():
    assert run_psgc4(sequences,directory_name) == False
def test2_function5_TRUE():
    assert run_pbnc5(sequences,directory_name) == True
def test2_function6_FALSE():
    assert run_sld6(sequences,directory_name) == False
def test2_function7_FALSE():
    assert run_os7(sequences,directory_name) == False
def test2_function8_TURE():
    assert run_ac8(sequences,directory_name) == True