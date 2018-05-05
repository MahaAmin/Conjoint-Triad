from decimal import *
import csv
from Bio import SeqIO


# Generating vector space (7*7*7)
def VS(rang):
    V = []
    for i in range(1,rang):
        for j in range(1,rang):
            for k in range(1,rang):
                tmp = "VS"+str(k) + str(j) + str(i)
                V.append(tmp)
    return V


# calculating conjoint triad for input sequence
def frequency(seq):
    frequency = []
    for i in range(0, (len(seq) - 3)):
        subSeq = seq[i:i+3]
        tmp = "VS"
        for j in range(0,3):
            if((subSeq[j] == 'A') or (subSeq[j] == 'G') or (subSeq[j] == 'V')):
                tmp += "1"
            elif((subSeq[j] == 'I') or (subSeq[j] == 'L') or (subSeq[j] == 'F') or (subSeq[j] == 'P')):
                tmp += "2"
            elif((subSeq[j] == 'Y') or (subSeq[j] == 'M') or (subSeq[j] == 'T') or (subSeq[j] == 'S')):
                tmp += "3"
            elif((subSeq[j] == 'H') or (subSeq[j] == 'N') or (subSeq[j] == 'Q') or (subSeq[j] == 'W')):
                tmp += "4"
            elif((subSeq[j] == 'R') or (subSeq[j] == 'K')):
                tmp += "5"
            elif((subSeq[j] == 'D') or (subSeq[j] == 'E')):
                tmp += "6"
            elif((subSeq[j] == 'C')):
                tmp += "7"
        frequency.append(tmp)
    return frequency


# Creating frequency_dictionary, and calaculate frequency for eaech conjoint triad
def freq_dict(V, freq):
    frequency_dictionary = {}
    for i in range(0, len(V)):
        key = V[i]
        frequency_dictionary[key] = 0

    for i in range(0, len(freq)):
        frequency_dictionary[freq[i]] = frequency_dictionary[freq[i]]+1

    # Normalization

    # Getting fmin & fmax
    fmax = int(0)
    fmin = int(0)
    for i in range(0, len(V)):
        key = V[i]
        if(frequency_dictionary[key] > fmax):
            fmax = frequency_dictionary[key]
        if(frequency_dictionary[key] < fmin):
            fmin = frequency_dictionary[key]

    # di = (fi - fmin) / fmax
    for i in range(0, len(V)):
        key = V[i]
        getcontext().prec = 3
        frequency_dictionary[key] = float("{0:.3f}".format(((frequency_dictionary[key] - fmin) / fmax)))

    return frequency_dictionary


# Export the output to .csv file
def output_to_csv(frequency_dict):
    with open('conjoint_triad.csv', 'a') as csvfile:
        conjointTriad = csv.DictWriter(csvfile, frequency_dict.keys())
        conjointTriad.writeheader()
        conjointTriad.writerow(frequency_dict)


# Reading sequences from fasta file.
def fasta_input():
    print("Enter path of .fasta file : ", end='')
    path = input()
    sequences = []
    for record in SeqIO.parse(path, "fasta"):
        sequences.append(record.seq)
    return sequences

def conjoint_triad():
    # Truncating .csv file
    filename = "conjoint_triad.csv"
    f = open(filename, "w+")
    f.close()
    # reading input file
    sequences = fasta_input()
    # Creating vector space
    v = VS(8)
    # calculating conjoint_triad for each sequence
    for i in range(0, len(sequences)):
        fi = frequency(sequences[i])
        freqDict = freq_dict(v, fi)
        output_to_csv(freqDict)
    print('Data was exported to "conjoint_triad.csv."')


conjoint_triad()
