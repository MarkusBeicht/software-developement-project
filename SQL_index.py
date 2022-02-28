#!/usr/bin/env python3
import pandas as pd
import numpy as np

#Reads the four CSV files in (as pandas dataframes)
df_chr = pd.read_csv('dory_eup_orth_chrs.csv')
df_gene = pd.read_csv('dory_eup_orth_genes.csv')
df_EUP = pd.read_csv('EUPgeneCHR.csv')
df_DORY = pd.read_csv('DORYgeneCHR.csv')


#Adds an indexed IdentCode column to each table. 
df_chr['IdentCode']=df_chr.index
df_gene['IdentCode']=df_gene.index
df_DORY['IdentCode']=df_DORY.index
df_EUP['IdentCode']=df_EUP.index

#Adds ChrId and GeneID columns, which will be used as foreign keys in the SQL database model. 
df_DORY['ChrID']=-1
df_DORY['GeneID']=-1
df_EUP['ChrID']=-1
df_EUP['GeneID']=-1

df_DORY_c = pd.DataFrame(columns=('Species', 'Chromosome', 'Gene', 'CoordinateStart', 'CoordinateEnd', 'IdentCode', 'ChrID', 'GeneID'))
df_EUP_c = pd.DataFrame(columns=('Species', 'Chromosome', 'Gene', 'CoordinateStart', 'CoordinateEnd', 'IdentCode', 'ChrID', 'GeneID'))


#The following nested loops compare all gene names and chromosome names in the data with each other. 

#DORY Chromosomes
for i in range(len(df_chr)):
	for j in range(len(df_DORY)):
		#If the chromosome name of the DORY table corresponds to the chromosome name in the HomologousChromosomes table, then the ChrID of the DORY table is set to the corresponding Index (IdentCode) of the HomologousChromosomes table. 
		if df_chr.iloc[i, 0]==df_DORY.iloc[j, 1]:
			if df_DORY.iloc[j, 6]==-1:
				df_DORY.at[j, 'ChrID'] = df_chr.iat[i, 2]
			#If the ChrID was already set, a new row is added which contains the same values and the new HomologousChromosomes Index. 
			else:
				row = pd.DataFrame([[df_DORY.at[j, 'Species'],df_DORY.at[j, 'Chromosome'],df_DORY.at[j, 'Gene'],df_DORY.at[j, 'CoordinateStart'],df_DORY.at[j, 'CoordinateEnd'],len(df_DORY)+len(df_DORY_c),df_DORY.at[j, 'ChrID'],-1]], columns=('Species', 'Chromosome', 'Gene', 'CoordinateStart', 'CoordinateEnd', 'IdentCode', 'ChrID', 'GeneID'))
				df_DORY_c = df_DORY_c.append(row, ignore_index=True)
df_DORY = df_DORY.append(df_DORY_c, ignore_index=True)


#DORY Genes
for i in range(len(df_gene)):
	for j in range(len(df_DORY)):
		if df_gene.iloc[i, 0]==df_DORY.iloc[j, 2]:
			df_DORY.at[j, 'GeneID'] = df_gene.iat[i, 2]


#EUP Chromosomes
for i in range(len(df_chr)):
	for j in range(len(df_EUP)):
		if df_chr.iloc[i, 1]==df_EUP.iloc[j, 1]:
			if df_EUP.iloc[j, 6]==-1:
				df_EUP.at[j, 'ChrID'] = df_chr.iat[i, 2]
			else:
				row = pd.DataFrame([[df_EUP.at[j, 'Species'],df_EUP.at[j, 'Chromosome'],df_EUP.at[j, 'Gene'],df_EUP.at[j, 'CoordinateStart'],df_EUP.at[j, 'CoordinateEnd'],len(df_EUP)+len(df_EUP_c),df_EUP.at[j, 'ChrID'],-1]], columns=('Species', 'Chromosome', 'Gene', 'CoordinateStart', 'CoordinateEnd', 'IdentCode', 'ChrID', 'GeneID'))
				df_EUP_c = df_EUP_c.append(row, ignore_index=True)
df_EUP = df_EUP.append(df_EUP_c, ignore_index=True)


#EUP Genes
for i in range(len(df_gene)):
	for j in range(len(df_EUP)):
		if df_gene.iloc[i, 1]==df_EUP.iloc[j, 2]:
			df_EUP.at[j, 'GeneID'] = df_gene.iat[i, 2]


#Saves the updated dataframes as CSV files. 
df_DORY.to_csv('DORY.csv', index=False)
df_EUP.to_csv('EUP.csv', index=False)
df_chr.to_csv('CHR_ID.csv', index=False)
df_gene.to_csv('GENE_ID.csv', index=False)
