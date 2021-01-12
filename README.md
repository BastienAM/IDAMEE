# Integration of Health Insurance Data to facilitate Epidemiological Studies

## required library :
you need to install the following libraries with the command `pip install xxx` :
* rdflib
* sqlalchemy
* sqlite3
* bsddb3 ([help for windows user](https://stackoverflow.com/questions/33714698/installing-bsddb3-6-1-1-in-windows-filenotfounderror-db-include-db-h))

## Run generateIrNat
For run the script, you must enter the name of the database file.  
Example : `python generateIrNat.py -db "snds_2235.db"`

## Run main
`python main.py`

## Convert .ttl file to TDB for Fuseki

### Required : 
* [apache-jena](https://jena.apache.org/download/index.cgi) (works with apache-jena-3.16.0)

### For windows user
You need to set Jena home and path.
* `SET JENA_HOME=`*the directory you downloaded Jena to*
* `SET PATH=%PATH%;%JENA_HOME%\bat`

Then, run :  
`tdbloader.bat --loc=database output.ttl`

The tdbloader script creates a database in the given location `databaseTDB` from the input file `output.ttl`.

### For Linux/Mac user
You need to set Jena home and path.
* `export JENA_HOME=`*the directory you downloaded Jena to*
* `export PATH=$PATH:$JENA_HOME/bin`

Then, run :  
`tdbloader --loc=database output.ttl`

## Run Apache Jena Fuseki

### Required : 
* [apache-jena-fuseki](https://jena.apache.org/download/index.cgi) (works with apache-jena-fuseki-3.16.0)

Run the command in the next repertory `apache-jena-fuseki-3.16.0/` :

`fuseki-server --loc=databaseTDB /data`

You must give the right path to access `databaseTDB` folder create before.
