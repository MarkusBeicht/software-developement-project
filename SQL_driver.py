from datetime import datetime
import pymssql

if __name__ == "__main__":
	#asks for user input to define the connection to the database
	server = input('Enter MSSQL Server connection: ')
	user = input('Enter MSSQL user name: ')
	pw = input('Enter MSSQL password: ')
	db = input('Enter database name within MSSQL Server: ')
	conn = pymssql.connect(server, user, pw, db)
	cursor = conn.cursor(as_dict=True)
	
	#prompts for user input to enter the query and number of runs
	i = 0
	j = int(input('Enter number of runs: '))
	query = input('Enter the MSSQL query: ')
	
	#starts the time measurement and executes the 
	start_time = datetime.now()
	while i < j:
		#cursor.execute("SELECT distinct genes.EupGENE, dory.Chromosome, dory.CoordinateStart, dory.CoordinateEnd, eup.Gene as EuprymnaOrtholog FROM [TestDB].[dbo].DORYgeneCHR dory left join TestDB.dbo.dory_eup_orth_genes genes on dory.Gene = genes.DoryGENE left join TestDB.dbo.EUPgeneCHR eup   on genes.EupGENE = eup.Gene where dory.Chromosome != 'Dpe11' and eup.Chromosome = 'Lachesis_group5' order by 3;")
		cursor.execute(query)
		i += 1
		#for row in cursor:
	    		#print(row)

	conn.close()
	time_passed = datetime.now() - start_time
	print('Time passed: ' + str(time_passed) + 's for ' + str(j) + ' runs.')

'''
SELECT distinct genes.EupGENE, dory.Chromosome, dory.CoordinateStart, dory.CoordinateEnd, eup.Gene as EuprymnaOrtholog FROM [TestDB].[dbo].DORYgeneCHR dory left join TestDB.dbo.dory_eup_orth_genes genes on dory.Gene = genes.DoryGENE left join TestDB.dbo.EUPgeneCHR eup   on genes.EupGENE = eup.Gene where dory.Chromosome != 'Dpe11' and eup.Chromosome = 'Lachesis_group5' order by 3;
Time passed: 0:00:34.909682s for 1000 runs.
Time passed: 0:00:34.671873s for 1000 runs.
Time passed: 0:00:35.031627s for 1000 runs.
Time passed: 0:00:34.952135s for 1000 runs.
Time passed: 0:00:35.101044s for 1000 runs.
Time passed: 0:00:35.558755s for 1000 runs.
Time passed: 0:00:34.040289s for 1000 runs.
Time passed: 0:00:34.143555s for 1000 runs.
Time passed: 0:00:33.706932s for 1000 runs.
Time passed: 0:00:35.227306s for 1000 runs.
Time passed: 0:00:35.227306s for 1000 runs.



SELECT * from [TestDB].[dbo].DORYgeneCHR dory;
Time passed: 0:00:08.526148s for 10000 runs.
Time passed: 0:00:09.870246s for 10000 runs.
Time passed: 0:00:10.531816s for 10000 runs.
Time passed: 0:00:10.042453s for 10000 runs.
Time passed: 0:00:08.655064s for 10000 runs.
Time passed: 0:00:09.838217s for 10000 runs.
Time passed: 0:00:10.980740s for 10000 runs.
Time passed: 0:00:09.740231s for 10000 runs.
Time passed: 0:00:09.792948s for 10000 runs.
Time passed: 0:00:09.726383s for 10000 runs.
Time passed: 0:00:09.741596s for 10000 runs.

'''
