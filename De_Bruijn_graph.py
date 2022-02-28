#!/usr/bin/env python3 
#Creates CSV-files from one or more input FASTA-files for a De Bruijn graph data structure to be stored in the graph database Neo4j. 

import sys
import numpy as np
import pandas as pd
import argparse 


#Parses keyboard arguments for input FASTA files, k-mer length
def add_args(parser):
	parser.add_argument("-i", type=argparse.FileType('r'), nargs='+', help="Input Fasta file")
	parser.add_argument("-k", type=int, default=3, help="Enter k-mer size")


#Creates CSV-file containing relationships.
def Relationship(ID, prev, next, Species, Sequence):
	filename_r = "./Relationships_%s.csv" % Species
	df = pd.DataFrame(data={"Position:int": ID, ":START_ID": prev, ":END_ID": next, "Species:TYPE": Species, "Sequence:int": Sequence})
	df.to_csv(filename_r, sep=',',index=False)


#Creates CSV-file containing nodes.
def Nodes(kmers, k):
	filename_n = "./Nodes.csv"
	df = pd.DataFrame(data={"Kmer:ID": kmers, "Kmers(" + str(k) + "):LABEL": k})
	df.to_csv(filename_n, sep=',',index=False)


#Creates Log file documenting which sequences correspond to which nodes
def Log(Descriptions1, Descriptions2):
	desc = "Pangenome graph Log\nDocumentation of the structure of the data for Neo4j for the seperate FASTA file sequences.\n\n"


#Transforms input FASTA-file into list of strings (1 list element for each sequence) and stores the FASTA headers for documentation.
def read_input(f):
	Sequence = ""
	Sequences = []
	Descriptions = []
	Species = str(f.name).split(".", 1)[0]

	for line in f.readlines():
		if line[0] == ">":
			Descriptions.append(line.strip())
			Sequences.append(Sequence)
			Sequence = ""
		else: 
			Sequence += line.strip().upper()
	Sequences.append(Sequence) 
	f.close()
	return Sequences[1:],Descriptions, Species


#Performs De Bruijn algorithm using overlapping kmers and stores the start and end kmer of each relationship. 
def De_Bruijn(Sequences, k, kmers):
	prev = []
	next = []
	ID = []
	Sequence = []

	#Overlapping kmers are determined for each sequence in the FASTA file. 
	for s in range(len(Sequences)):
			for i in range(len(Sequences[s])-k):
				if Sequences[s][i:i+k] not in kmers:
					kmers.append(Sequences[s][i:i+k])
				prev.append(Sequences[s][i:i+k])
				next.append(Sequences[s][i+1:i+k+1])
				ID.append(i)
				Sequence.append(str(s+1))
			if Sequences[s][len(Sequences[s])-k:len(Sequences[s])+1] not in kmers:
				kmers.append(Sequences[s][len(Sequences[s])-k:len(Sequences[s])+1])
	return ID, prev, next, Sequence, kmers


#Uses keyboard arguments to perform input, De Bruijn, Relationship and Nodes functions. 
def main(args):
	k = args.k
	kmers = []
	
	#Performs functions for each input FASTA file. 
	for f in args.i:
		Sequences, Descriptions, Species = read_input(f)
		ID, prev, next, Sequence, kmers = De_Bruijn(Sequences, k, kmers)
		Relationship(ID, prev, next, Species, Sequence)
	
	#Nodes file is created only once, after all distinct kmers are added up. 
	Nodes(kmers, k)		

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Creates .csv-Files for Neo4j")
    add_args(parser)
    main(parser.parse_args())
    sys.exit(0)
