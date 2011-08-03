#!/usr/bin/python
############################################################
# --=[[SMSGenie.py]]=--                
# 
# Hacked together by Benjamin Tan (26022010) for the GWF 
# GEM project. 
# 
# Gammu is used to provide SMS send/receive functionality.
# A Sony Ericsson K810i was used in this implementation.
#
# SMSGenie:
#   * provides a backend for recieving SMS
#   * queries the database based on SMS text message 
#   * returns a formatted response from database 
#     back to the user.
#
# Notes:
#   * Make sure that Gammu is installed. However, there is
#     no need to manually launch Gammu.
#   * Ubuntu Karmic 9.10 with Gammu 1.26. Note that the 
#     default repos are 1.24. Therefore you would need to 
#     update the software sources to get the latest release.
###########################################################

# TODO: 
# - Generate random code, then using that code generate database 

import gammu, pdb,time, MySQLdb

def init():
	
	# Sets up the phone using GAMMU
	sm = gammu.StateMachine()
	sm.ReadConfig()
	sm.Init()

	unread_sms_list = []

	while 1:	
		status = sm.GetSMSStatus()
		remain = status['SIMUsed'] + status['PhoneUsed'] + status['TemplatesUsed']
		start = True

		print "Checking for new SMSes"

		while remain > 0:
			if start:
				sms = sm.GetNextSMS(Start = True, Folder = 0)
				start = False
			else:
				sms = sm.GetNextSMS(Location = sms[0]['Location'], Folder = 0)
			
			remain = remain - len(sms)

			for m in sms:
				if m['State'] == "UnRead":				
					unread_sms_list.append(m)
					msg = parseMessage(m)
				
					message = {'Text': msg, 'SMSC': {'Location':1}, 'Number': str(m['Number'])}
					print message
					sm.SendSMS(message)
					print "Done sending message"

		if len(unread_sms_list) != 0:
			print "New SMS Found! Adding to queue"
			print "Sleeping for 10 seconds" 
			# Reset list
			unread_sms_list = []
		else:
			print "No new SMS"
		
		time.sleep(10)

# Retrieves short code and query from SMS
def parseMessage(m):
	num      = m['Number']
	datetime = m['DateTime']
	text     = m['Text']

	print "========================================="
	print "New SMS Found! Adding to queue"
	print "========================================="
	print '%-15s: %s' % ('Number', m['Number'])
	print '%-15s: %s' %  ('Date', str(m['DateTime']))
	print '%-15s: %s' %  ('Text', str(m['Text']))
	print "========================================="
	short_code, query = text.split(" ")[0], text.split(" ")[1:]
	print '%-15s: %s' %  ('Short Code', short_code)
	print '%-15s: %s' %  ('Query', ' '.join(query))
	print "========================================="
	
	msg = ""

	try:
		conn = MySQLdb.connect (host = "localhost",
					                 	user = "root",
					                  passwd = "root",
														db = "sms_tables")
		 
		cursor = conn.cursor()
		q = "SHOW COLUMNS FROM sms_tables." + short_code.lower()
		cursor.execute(q)

		# Uses only the first column (not the _id) to perform query 
		q_col = list(cursor.fetchall())[1][0]
		q = "SELECT * FROM "+short_code.lower()+" WHERE "+q_col+ " LIKE '"+str(query[0])+"%'"
		print q
		
		cursor = conn.cursor()
		cursor.execute(q)
		row = list(cursor.fetchone())
	
		msg = " ".join(row[2:])[0:160].replace('\xa0', ' ')


	except MySQLdb.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
						     

	cursor.close()
	conn.close()

	print msg
	return msg


m = {}
m['Number'] = "4086663855"
m['Text']   = "aids_drug2 NOR"
m['DateTime']   = "Today"

parseMessage(m)

###########################
# Starts up everything up #
###########################
if __name__ == '__main__':
	init()
	print "Closed."
