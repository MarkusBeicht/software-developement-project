This python3 script takes two FASTA files as input and outputs two CSV files (Nodes, Relationships), which can be imported in a Neo4j database instance using the neo4j admin-import tool. 
It requries the numpy, pandas and sys modules. 
The user has to enter the FASTA files per keyboard input. An example command would look like this: "python3 Pangenome_graph.py Seq1.fna Seq2.fna". 

The two FASTA files are read in sequence per sequence. The first sequences of each of the two FASTA files are aligned, as well as the second, third and so on with each other. 
The the nucleotudes are grouped into consecutive matches and mismatches. 
Based on this, the necessary nodes and relationships are created. 
The node data is stored in the file "Nodes.csv". 
The relationship data is stored in the file "Relationships.csv". 
A Log file "Log.txt", which contains the information which sequences correspond to which Neo4j nodes and relationships, is also created. 
The name of the input FASTA file up to the first dot becomes the Species name of all Sequences corrseponding to that file. ("Seq1.fna" -> Species: Seq1)

The output files can the be imported into Neo4j using the neo4j admin-import tool after the CSV files are put into the import folder of the database instance. 
"bin/neo4j-admin import --nodes=import/Nodes.csv --relationships=import/Relationships.csv". 
