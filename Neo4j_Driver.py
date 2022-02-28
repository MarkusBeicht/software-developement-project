from neo4j import GraphDatabase
from datetime import datetime

#Defines the the Neo4j_Query class.
class Neo4j_Driver:
    
   	#Establishes the databse connection per driver.
   	def __init__(self, uri, user, password):
		self.driver = GraphDatabase.driver(uri, auth=(user, password))

	#Closes the database connection.
	def close(self):
		self.driver.close()

	#Executes a query per driver and can print the result. 
	def execute_query(self, query):
		with self.driver.session() as session:
			result = session.run(query)
			#print(result.data())


if __name__ == "__main__":
	#Promting user for input about the database connection.
	uri = input('Enter the database connection (uri): ')
	user = input('Enter your Neo4j username: ')
	pw = input('Enter the password of your neo4j databse instance: ')
	connection = Neo4j_Driver(uri, user, pw)
    
	#Asking user for input about the query. 
	query = input('Enter your Cypher-query: ')
	i = 0
	j = int(input('Enter number of runs: '))
    
	#Starting the time measurement and executing the query in a loop. Then it prints the execution time. 
	start_time = datetime.now()
	while i < j:
		connection.execute_query(query)
		i += 1
	connection.close()
	time_passed = datetime.now() - start_time
	print('Time passed: ' + str(time_passed) + 's for ' + str(j) + ' runs of the query: ' + str(query))