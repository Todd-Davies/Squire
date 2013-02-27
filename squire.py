import cmd, locale, os, shlex, dropbox, json
from dropbox import client, rest, session
from cStringIO import StringIO
from string import Template
from Schooltraq import Assignment, getAssignments
from Triggers import Trigger_Schooltraq_Essay, Trigger_Schooltraq_Research
from DropboxInterface import StoredSession
import search
import datetime

APP_KEY = "."
APP_SECRET = "."
ACCESS_TYPE = "."
STQ_API_KEY = "."
SECRETS_FILE = "/home/pi/squire/secrets.txt"

def loadSecrets():
		try:
			secrets = open(SECRETS_FILE).read()
			count = 0
			for secret in secrets.split('|'):
				if count==0:
					global APP_KEY
					APP_KEY = secret.rstrip()
				elif count==1:
					global APP_SECRET
					APP_SECRET = secret.rstrip()
				elif count==2:
					global ACCESS_TYPE
					ACCESS_TYPE = secret.rstrip()
				elif count==3:
					global STQ_API_KEY
					STQ_API_KEY = secret.rstrip()
				else:
					print("Warning - malformed secrets file")
				count += 1
			#print("Credentials loaded successfully")
		except IOError:
			print("Error - no secrets.txt file found")
			exit()

#Log the start time
now = datetime.datetime.now()
print("Started on " + now.strftime("%Y-%m-%d %H:%M:%S"))

#Load the API credentials etc
loadSecrets()
sess = StoredSession.StoredSession(APP_KEY,APP_SECRET,ACCESS_TYPE)
dropboxClient = client.DropboxClient(sess)
sess.load_creds(False)
if not sess.is_linked():
	sess.link()

#Download the assignments from Schooltraq
assignments = getAssignments.getAssignments(STQ_API_KEY)

#Create the triggers for the assignments
essayTrigger = Trigger_Schooltraq_Essay.Trigger_Schooltraq_Essay(None, dropboxClient)
researchTrigger = Trigger_Schooltraq_Research.Trigger_Schooltraq_Research(None, dropboxClient)

#Log the number of assignments at this time
print("> " + str(len(assignments)) + " assignments found")

#Analyse the assignments
for a in assignments:
	essayTrigger.setAssignment(a)
	researchTrigger.setAssignment(a)
	if essayTrigger.isTriggered():
		essayTrigger.runTrigger()
	elif researchTrigger.isTriggered():
		researchTrigger.runTrigger(STQ_API_KEY)

#Log the finish time
now = datetime.datetime.now()
print("Finished on " + now.strftime("%Y-%m-%d %H:%M:%S"))
