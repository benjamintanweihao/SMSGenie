#!/usr/bin/env python
import MySQLdb, csv, sys

def read_csv(file_name):
	
	ifile  = open(file_name, "rb")
	try:
		csv_data = csv.reader(ifile, delimiter=";", quotechar='\'')
	except IOError:
		print "No such file or directory"
	
	# construct a list of field names
	field_names_unprocessed = csv_data.next()
	
	field_names = []

	for f in field_names_unprocessed:
		field_names.append(f[1:len(f)-1])

 	generateTable(file_name,csv_data,field_names)
	
		
		
		
	# Reconstruct a new matrix for use with the recommendation engine.
	# Therefore, we need to remove the manipulate the left most column
	# of the input csv matrix.
	for row in csv_data:
		print row[0]	
	ifile.close();

############################################################
# Creates a new database. If database name already exists, #
# generate a new one                                       #
############################################################
def initDB(db_name):
	try:
		conn = MySQLdb.connect (host = "localhost",
														user = "root",
														passwd = "root")

		cursor = conn.cursor()
		cursor.execute("CREATE DATABASE " + db_name)

	except MySQLdb.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		#sys.exit(1)
	
		# Create our database table
		# TODO: More rubust code to check if database exists

			#row = cursor.fetchone()
			#print row[0]

		cursor.close()
		conn.close()

def executeQuery(query):
	try:
		conn = MySQLdb.connect (host = "localhost",
														user = "root",
														passwd = "root",
														db = "sms_tables")
		# Create our database table
		# TODO: More rubust code to check if database exists
		cursor = conn.cursor()
		cursor.execute(query)
		row = cursor.fetchall()
		
		for r in row:
			r = list(r)	
			print  str(r[1:])[0:160]

	except MySQLdb.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		#sys.exit(1)
	
		
		cursor.close()
		conn.close()



###########################################################
# Generates a table based on CSV values                   #
###########################################################
def generateTable(table_name,csv_data,field_names, pk_idx=0):
	table_name = table_name.replace(".csv","")	
	q = "CREATE TABLE IF NOT EXISTS " + table_name + "(id int(2) PRIMARY KEY AUTO_INCREMENT, "  
	
	for f in field_names:
		q += f + " VARCHAR(200),"

	#q += "PRIMARY KEY(" + field_names[pk_idx] + ")"
	#q += ");"
	q=q[0:len(q)-1] + ");"

	print q
	
	try:
		conn = MySQLdb.connect (host = "localhost",
														user = "root",
														passwd = "root",
														db = "sms_tables")
		cursor = conn.cursor()
		cursor.execute(q)
		
		# Insert values
		idx=1;
		for row in csv_data:
			print "==============================================================="
			q  =  "INSERT INTO " + table_name + " VALUES(" + str(idx) + ","
			q += ",".join(row)
			q += ");"
			idx+=1

			print q
			cursor = conn.cursor()
			cursor.execute(q)

	except MySQLdb.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		#sys.exit(1)
	
		# Create our database table
		# TODO: More rubust code to check if database exists
		cursor.close()
		conn.close()

read_csv("phone.csv")	
read_csv("hospital.csv")	
	

