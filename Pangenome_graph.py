#!/usr/bin/env python3 
#Creates CSV-files from 2 input FASTA-files for a panGenome graph data structure to be stored in the graph database Neo4j. 

import sys
import numpy as np
import pandas as pd


#Transforms input FASTA-file into list of strings (1 list element for each sequence) and stores the FASTA headers for documentation.
def read_input(i):
	Seq_str = ""
	Sequence = []
	Descriptions = []
	with open(sys.argv[i], "r") as f:
		Species = str(f.name).split(".", 1)[0]
		for line in f.readlines():
			#checks if the line is a FASTA header or sequence
			if line[0] == ">":
				Descriptions.append(line.strip())
				Sequence.append(Seq_str)
				Seq_str = ""
			else: 
				Seq_str += line.strip().upper()
		Sequence.append(Seq_str)
	f.close()
	
	return Sequence[1:],Descriptions, Species



#determines the optimal alignment of the next 1000 nucleotides (test_range) for every shift between the 2 sequences up to 100 (shift_range). 
def shift(pos1, pos2, Sequence1, Sequence2, shift_range, test_range):
	max_shift = 0
	max_match = 0
	lst = [i for i in range(-shift_range, shift_range+1)]
	lst = sorted(lst, key=abs)

	#for each shift s, the next 1000 nucleotides are compared for matches
	for s in lst:
		match = 0
		for m in range(test_range):
			
			if s <= 0 and len(Sequence1[0]) > m+pos1 and len(Sequence2[0]) > m-s+pos2:
				if Sequence1[0][m+pos1] == Sequence2[0][m-s+pos2]:
					match += 1
			
			elif s > 0 and len(Sequence1[0]) > m+s+pos1 and len(Sequence2[0]) > m+pos2:
				if Sequence1[0][m+s+pos1] == Sequence2[0][m+pos2]:
					match += 1
		#updates the max_match score
		if match > max_match:
			max_match = match
			max_shift = s
			
			#ends the loop prematurely, if an overlap of 75% is reached to improve the performance
			if match > test_range * 0.75:
				return max_shift
	return max_shift
	


#aligns the 2 sequences using the shift-function and determines whether a matches, mutation or gap occurred
def Alignment(Sequence1, Sequence2, n):
	i = 0
	seq1 = []
	seq2 = []
	values = []
	shift1 = 0
	shift2 = 0

	#adds the nucleotides and the match-values (T...true(match), F..false(mismatch), G1...gap sequence1, G2...gap sequence2) until the end of the sequencens
	while i+shift1 < len(Sequence1[n]) and i+shift2 < len(Sequence2[n]):
		if (Sequence1[n][i+shift1]) == (Sequence2[n][i+shift2]):
			seq1.append(Sequence1[n][i+shift1])
			seq2.append(Sequence2[n][i+shift2])
			values.append('T')
			i += 1	
		
		#if the nucleotdies are not matching, the shift function is called to determine wether a Gap or a mismatch happend
		else:
			new_shift = shift(i+shift1, i+shift2, Sequence1, Sequence2, 100, 1000)
			if new_shift > n:
				seq1.append(Sequence1[n][i+shift1])
				seq2.append("-")
				values.append('G2')
				shift1 += 1	
			elif new_shift < 0:
				seq2.append(Sequence2[n][i+shift2])
				seq1.append("-")
				values.append('G1')
				shift2 += 1
			else:
				seq1.append(Sequence1[n][i+shift1])
				seq2.append(Sequence2[n][i+shift2])
				values.append('F')
				i += 1

	#adds the last nucleotides of one sequecne, if they protrude in the alignment
	while i+shift2 < len(Sequence2[n]):
		seq1.append("-")
		seq2.append(Sequence2[n][i+shift2])
		values.append('G1')
		i += 1
		
	while i+shift1 < len(Sequence1[n]):
		seq1.append(Sequence1[n][i+shift1])
		seq2.append("-")
		values.append('G2')
		i += 1
	
	return values, seq1, seq2, shift1, shift2



#Consecutive matches and mismatches are grouped together. Structures the sequences into the eventual nodes. 
def group_mismatch_gap(values, seq1, seq2, shift1, shift2):
	i = 0
	join_nodes = []
	AB = []
	joins = []
	
	while i+shift1 < len(seq1) and i+shift2 < len(seq2):
		
		#groups consecutive matches together
		if values[i] == 'T' and i < len(seq1)-1:
			S = ''
			while values[i] == 'T' and i < len(seq1)-1:
				S+=seq1[i]
				i += 1
				if i == len(values)-1:
					S+=seq1[i]
			join_nodes.append(S)
			joins.append('T')

		#Groups consecutive mismatches together and evaluates whether they are mismatches or gaps (join-value)
		if values[i] != 'T' and i < len(seq1):
			A = ''
			B = ''
			AB = []
			while values[i] != 'T' and i < len(seq1)-1: 
				if values[i] == 'G1':
					B += seq2[i]
					i += 1
				elif values[i] == 'G2':
					A += seq1[i]
					i += 1
				elif values[i] == 'F':
					A += seq1[i]
					B += seq2[i]
					i += 1
				if i == len(values)-1:
					if values[i] == 'G1':
						B += seq2[i]
					elif values[i] == 'G2':
						A += seq1[i]
					elif values[i] == 'F':
						A += seq1[i]
						B += seq2[i]
			
			AB.append(A)
			AB.append(B)
			join_nodes.append(AB)
		
		#Adds the join-value of the last nucleotides.
		if A == '':
			joins.append('G1')
		elif B == '':
			joins.append('G2')
		else: 
			joins.append('F')
	return joins, join_nodes


#Created nodes and relationships in the structure they will have in the graph database.
#Stores nodes (node sequence), NodeID, NodeSequence and relationship startID (prev), endID (next), and rel (correspondance to input file).
def nodes_rel(joins, join_nodes, n, l):
	i = 0
	j = 0
	prev = []
	next = []
	rel = []
	NodeID = []
	nodes = []
	NodeSequence = []
	
	#Checks if first node is shared by both sequcenes (str) or not (list) and adds the first node. 
	if isinstance(join_nodes[i], str):
		nodes.append(join_nodes[i])
		i += 1
		NodeID.append(i+j+l)
		NodeSequence.append(n)
	else:		
		if join_nodes[i][0] == '-':
			nodes.append(join_nodes[i][1])
			i += 1
			NodeID.append(i+j+l)
			NodeSequence.append(n)
		elif join_nodes[i][1] == '-':
			nodes.append(join_nodes[i][0])
			i += 1
			NodeID.append(i+j+l)
			NodeSequence.append(n)
		else:
			nodes.append(join_nodes[i][0])
			nodes.append(join_nodes[i][1])
			i += 1
			NodeID.append(i+j+l)
			NodeSequence.append(n)
			j += 1
			NodeID.append(i+j+l)
			NodeSequence.append(n)

	#Adds the nodes and relationships depending on the join-value (F, T, G1, G2).
	#If the node is shared by both sequences the previous nodes are looked at to define the relationships correctly.
	while i < len(join_nodes):
		if joins[i] == 'T':
			if joins[i-1] == 'F':
				nodes.append(join_nodes[i])
				i += 1
				NodeID.append(i+j+l)
				NodeSequence.append(n)
				
				prev.append(i+j-2+l)
				next.append(i+j+l)
				rel.append(1)
				prev.append(i+j-1+l)
				next.append(i+j+l)
				rel.append(2)
		
			elif joins[i-1] == 'G1':
				nodes.append(join_nodes[i])
				i+=1
				NodeID.append(i+j+l)
				NodeSequence.append(n)
				
				prev.append(i+j-1+l)
				next.append(i+j+l)
				rel.append(2)
				if i >= 2:
					prev.append(i+j-2+l)
					next.append(i+j+l)
					rel.append(1)
				
			elif joins[i-1] == 'G2':
				nodes.append(join_nodes[i])
				i+=1
				NodeID.append(i+j+l)
				NodeSequence.append(n)
				
				prev.append(i+j-1+l)
				next.append(i+j+l)
				rel.append(1)
				if i >= 2:
					prev.append(i+j-2+l)
					next.append(i+j+l)
					rel.append(2)
		
		#If the node is not shared by both sequences the nodes and relationships are added according to the join-values. The previous node is always a shared node. 
		elif joins[i] == 'F':
			nodes.append(join_nodes[i][0])
			nodes.append(join_nodes[i][1])
			i+=1
			NodeID.append(i+j+l)
			NodeSequence.append(n)
			j += 1
			NodeID.append(i+j+l)
			NodeSequence.append(n)
			
			prev.append(i+j-2+l)
			next.append(i+j-1+l)
			rel.append(1)
			prev.append(i+j-2+l) 
			next.append(i+j+l)
			rel.append(2)
		
		elif joins[i] == 'G1':
			nodes.append(join_nodes[i][1])
			i+=1
			NodeID.append(i+j+l)
			NodeSequence.append(n)
			
			prev.append(i+j-1+l)
			next.append(i+j+l)
			rel.append(2)
	
		elif joins[i] == 'G2':
			nodes.append(join_nodes[i][0])
			i+=1
			NodeID.append(i+j+l)
			NodeSequence.append(n)
			
			prev.append(i+j-1+l)
			next.append(i+j+l)
			rel.append(1)
	
	
	#Removes empty nodes and their corresponding relationships.
	m = 0
	n = 0
	for i in range(len(nodes)-m):
		if nodes[i-m] == '':
			m += 1
			nodes.pop(i)
			remove_rel = NodeID.pop(i)
			for i in range(len(prev)-n):
				if remove_rel == prev[i-n] or remove_rel == next[i-n]:
					prev.pop(i-n)
					next.pop(i-n)
					rel.pop(i-n)
					n += 1
	
	return(prev, next, rel, NodeID, nodes, NodeSequence)
	

#Creates CSV-file containing relationships.
def Relationship(prev, next, rel):
	filename_r = "./Relationships.csv"
	df = pd.DataFrame(data={":START_ID": prev, ":END_ID": next, ":TYPE": rel})
	df.to_csv(filename_r, sep=',',index=False)


#Creates CSV-file containing nodes.
def Nodes(NodeID, nodes, NodeSequence, Label):
	filename_n = "./Nodes.csv" 
	df = pd.DataFrame(data={"NodeID:ID": NodeID, "Nodes:LABEL": Label, "Sequence": nodes, "Sequence:int": NodeSequence_all})
	df.to_csv(filename_n, sep=',',index=False)

#Creates Log file documenting which sequences correspond to which nodes
def Log(Descriptions1, Descriptions2, Species1, Species2):
	desc = "Pangenome graph Log\nDocumentation of the structure of the data for Neo4j for the seperate FASTA file sequences.\n\n"
	
	#Uses the FASTA headers for the Log file node type descriptions. 
	for i in range(min(len(Descriptions1), len(Descriptions2))):
		desc += f"Aligned Species {Species1} and {Species2} Sequence {i+1}: {Descriptions1[i]} and {Descriptions2[i]}\n"
	if len(Descriptions1) > len(Descriptions2):
		for i in range(len(Descriptions1) - len(Descriptions2)):
			desc += f"Species {Species1} Sequence {i+len(Descriptions2)+1}: {Descriptions1[i+len(Descriptions2)]}\n"	
	
	if len(Descriptions2) > len(Descriptions1):
		for i in range(len(Descriptions2) - len(Descriptions1)):
			desc += f"Species {Species2} Sequence {i+len(Descriptions1)+1}: {Descriptions2[i+len(Descriptions1)]}\n"	
	
	#Writes txt file. 
	filename_n = open("./Log.txt", "w")
	filename_n.write(desc)
	filename_n.close()



if __name__ == "__main__":
	#Reads FASTA input into list of strings
	Sequence1, Descriptions1, Species1 = read_input(1)
	Sequence2, Descriptions2, Species2 = read_input(2)
	
	#Declares variables. 
	prev_all = []
	next_all = []
	rel_all = []
	NodeID_all = []
	nodes_all = []
	NodeSequence_all = []
	Label_all = []
	l = 0


	#Performs alignment, grouping of consecutive matches/mismatches, node/relationship creation for the sequences of the FASTA files.
	for n in range(min(len(Sequence1), len(Sequence2))):
		values, seq1, seq2, shift1, shift2 = Alignment(Sequence1, Sequence2, n)
		joins, join_nodes = group_mismatch_gap(values, seq1, seq2, shift1, shift2)
		prev, next, rel, NodeID, nodes, NodeSequence = nodes_rel(joins, join_nodes, n+1, l)
		for i in range(len(prev)):
			prev_all.append(prev[i])
			next_all.append(next[i])
			rel_all.append(rel[i])
		for i in range(len(NodeID)):
			NodeID_all.append(NodeID[i])
			nodes_all.append(nodes[i])
			NodeSequence_all.append(NodeSequence[i])
			Label_all.append(f"Aligned Species {Species1} and {Species2} Sequence {n+1}")
		l += len(NodeID)


	#If the first FASTA input file has more sequences they are added as a single node containing the sequence.
	if len(Sequence1) > len(Sequence2):
		for i in range(len(Sequence1) - len(Sequence2)):
			NodeID_all.append(len(NodeID_all)+1)
			nodes_all.append(Sequence1[i+len(Sequence2)])
			NodeSequence_all.append(len(Sequence2)+i+1)
			Label_all.append(f"Species {Species1} Sequence {n+i+2}")
	
	#If the second FASTA input file has more sequences they are added as a single node containing the sequence.
	if len(Sequence1) < len(Sequence2):
		for i in range(len(Sequence2) - len(Sequence1)):
			NodeID_all.append(len(NodeID_all)+1)
			nodes_all.append(Sequence2[i+len(Sequence1)])
			NodeSequence_all.append(len(Sequence1)+i+1)
			Label_all.append(f"Species {Species2} Sequence {n+i+2}")


	#Creates output CSV-files
	Relationship(prev_all, next_all, rel_all)
	Nodes(NodeID_all, nodes_all, NodeSequence_all, Label_all)
	Log(Descriptions1, Descriptions2, Species1, Species2)
