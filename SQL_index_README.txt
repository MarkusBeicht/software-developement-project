This python3 script was used to preprocess the input CSV files for the MSSQL server instance. This was necessary to enable unique connections between the data records. Otherwise, a single gene data record might correspond to several genes which are orthologous to it. 

The user simply executes the command "python3 SQL_index.py", given that the required CSV files are in the current path. 
The python packages pandas and numpy are requried.

Four new CSV files are created, which contain a more optimal data structure for a relational database like MSSQL. 
