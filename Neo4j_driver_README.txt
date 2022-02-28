This python3 script was used to do runtime performance tests on a Neo4j database instance. 
It requires the installation of the python package neo4j. (pip install neo4j)

It prompts the user for manual input five times in order to define the connection to the database and declare which query should be performed how often. 
Firstly, the Database connection has to be entered, more accurately the uri. For a local Neo4j database instance the default is “neo4j://localhost:7687”. 
Secondly, the username is asked for. The default in Neo4j is “neo4j”. 
Thirdly, the password of the Neo4j database instance is asked for. The default password Neo4j sets is “neo4j” as well.
These three user inputs are needed to define the connection to the database instance. 
Afterwards, the user is prompted to enter the query which is to be performed. 
Lastly, the user has to enter the number of times the query should be performed as an integer. 
Then, the time measurement will be started and the python3 code will connect to the Neo4j database instance and execute the query as often as was specified in the fifth user input. 
Finally, the runtime, query and number of runs will be printed. 