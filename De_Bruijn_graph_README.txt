This python3 script takes one or more FASTA files as input and outputs CSV files (one node file Nodes and relationship file for each input FASTA file), which can be imported in a Neo4j database instance using the neo4j admin-import tool. 
It requries the numpy, pandas, sys and argparse modules. 

The user has to enter the FASTA files per keyboard input. 
The mandatory input arguments are -k and -i. 
-k defines the kmer-length of the De Bruijn graph nodes and an integer must be added. 
-i defines the input FASTA files. One or more FASTA files can be added. 

An example command would look like this: "python3 De_Bruijn_graph.py -k 3 -i Seq1.fna Seq2.fna". 

The FASTA files are read in sequence per sequence. 
The distinct kmers of all input sequences are determined and stored in the "Nodes.csv" file. 
The relationships defining the sequence through those nodes are stored in a CSV file like "Relationships_X.csv" (X...FASTA file name until the first dot) file, one for each input file. 
The the nucleotudes are grouped into consecutive matches and mismatches. 

The output files can the be imported into Neo4j using the neo4j admin-import tool after the CSV files are put into the import folder of the database instance. 
"bin/neo4j-admin import --nodes=import/Nodes.csv --relationships=import/Relationships_Seq1.csv --relationships=import/Relationships_Seq2.csv". 
