This python3 script was used to do runtime performance tests on a Microsoft SQL Server (MSSQL). 
It requires the installation of the python package pymssql. (pip install pymssql)
It prompts the user for manual input six times in order to define the connection to the database and declare which query should be performed how often. 
Firstly, the Database connection has to be entered. This can be the IP-address or the name of your device in case of a local database instance. 
Secondly, the username is asked for. The default is “sa”. 
Thirdly, the password of the MSSQL server is asked for. 
Additionally, the user is prompted to enter the name of the database within the MSSQL server which should be accessed. 
These four user inputs are needed to define the connection to the MSSQL server database. 
Afterwards, the user is prompted to enter the query. 
Lastly, the user has to enter the number of times the query should be performed as an integer. 
Then, the time measurement will be started and the python3 code will connect to the MSSQL server database and execute the query as often as was specified in the sixth user input. 
Finally, the runtime, query and number of runs will be printed. 
