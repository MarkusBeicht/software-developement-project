from datetime import datetime
import pymssql

if __name__ == "__main__":
	#Promts user for input to define the connection to the database.
	server = input('Enter MSSQL Server connection: ')
	user = input('Enter MSSQL user name: ')
	pw = input('Enter MSSQL password: ')
	db = input('Enter database name within MSSQL Server: ')
	conn = pymssql.connect(server, user, pw, db)
	cursor = conn.cursor(as_dict=True)
	
	#Prompts user for input to enter the query and number of runs.
	i = 0
	j = int(input('Enter number of runs: '))
	query = input('Enter the MSSQL query: ')
	
	#Starts the time measurement, executes the query and prints the result. 
	start_time = datetime.now()
	while i < j:
		cursor.execute(query)
		i += 1
		#for row in cursor:
	    		#print(row)

	conn.close()
	time_passed = datetime.now() - start_time
	print('Time passed: ' + str(time_passed) + 's for ' + str(j) + ' runs.')