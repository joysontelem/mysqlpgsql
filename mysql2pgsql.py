import re
import sys

filepath = sys.argv[1]
f = open(filepath,'r')

# a dictionary mapping MySQL datatypes to corresponding PostgreSQL datatypes
type_dict = {
'INT(':'INTEGER',
'TINYINT':'SMALLINT',
'MEDIUMINT':'INTEGER',
'FLOAT':'REAL',
'DOUBLE':'DOUBLE PRECISION',
'TINYTEXT':'TEXT',
'MEDIUMTEXT':'TEXT',
'LONGTEXT':'TEXT',
'TINYBLOB':'BYTEA',
'BLOB':'BYTEA',
'MEDIUMBLOB':'BYTEA',
'LONGBLOB':'BYTEA',
'DATETIME':'TIMESTAMP'
}

# method to replace MySQL datatype with PostgreSQL datatype
def replaceDatatype(datatype):
	for key,value in type_dict.items():
		if(datatype.upper().startswith(key)):
			if(datatype.endswith(",")):
				return value + ","
			else:
				return value
		if(datatype.upper().startswith("ENUM")): #enums need to be created in metadata
			global enums
			global metadata
			metadata = "CREATE TYPE enum"+str(enums)+" AS " + datatype.rstrip(",") + ";\n"
			enums = enums + 1
			if(datatype.endswith(",")):
				return "enum"+str(enums) + ","
			else:
				return "enum"+str(enums)
		
	return datatype
		

flagtable=False; #inside create table
flaginsert=False; #inside insert into

# going line by line
pg=""
metadata=""
enums=1
for line in f:
	metaconstraint=""
	if(line.startswith("--") or line.startswith("/*") or line.startswith("DROP TABLE") or line.startswith("LOCK") or line.startswith("UNLOCK")): #these lines are useless
		continue
	
	line = re.sub(r'//*.*/*/',"",line)
	line = line.strip()
	line = line.replace("`" ,"")
	line = line.replace('"',"'")
	if(line.startswith("USE DATABASE")):
		line = line.replace("USE DATABASE","\c")
		pg = pg + "\n" + line

	if(line.startswith("CREATE TABLE")):
		flagtable = True
		tablename = line.split()[2]
		pg = pg + "\n" + line
		continue
		
	if(line.startswith("PRIMARY KEY")):
		pg = pg + "\n" + line
		continue
		
	if(line.startswith("UNIQUE KEY")):
		line = re.sub(r'KEY.*\(',"(",s)
		pg = pg + "\n" + line
		continue
	if(line.startswith("KEY")):
		continue
	if(line.startswith("CONSTRAINT")):
		metaconstraint=""
		line = "ALTER TABLE " + tablename + " ADD " + line + ";\n"
		metaconstraint = metaconstraint + line 
		continue			
	if(line.startswith(")") and flagtable):
		flagtable = False;
		pg = pg + "\n"+ ");"
		pg = pg + "\n" + metaconstraint
		continue
		
	if(flagtable):
		tokens = line.split(" ",2)
		columnname = tokens[0]
		datatype = tokens[1]
		
		try:
			constraint = tokens[2]
			constraint = constraint.replace("auto_increment","")
		except IndexError:
			constraint = '' 
			
		datatype = str(replaceDatatype(datatype))
		line = columnname + " " + datatype + " " + constraint
		pg = pg + "\n" + line
		continue
		
	
	if(line.startswith("INSERT INTO") or line.startswith("insert into")):
		pg = pg + "\n" + line;
		flaginsert = True
		continue
	
	if(flaginsert and line.endswith(");")):
		flaginsert = False;
		pg = pg + "\n" + line;
		continue

pg = metadata + "\n" + pg
print(pg)
