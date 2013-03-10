import cmd, locale, os, shlex, dropbox, json
from dropbox import client, rest, session
from cStringIO import StringIO
from string import Template
from Schooltraq import Assignment, getAssignments
from Triggers import Trigger_Schooltraq_Essay, Trigger_Schooltraq_Research
from DropboxInterface import StoredSession
import search
import datetime
import credentials_manager


APP_KEY = "."
APP_SECRET = "."
ACCESS_TYPE = "."
STQ_API_KEY = "."
STQ_USERNAME = "."
SECRETS_FILE = "/home/pi/squire/secrets.txt"

#Log the version
print("=====\nversion:2")

#Log the start time
now = datetime.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))

manager = credentials_manager.CredentialsManager()

numUsers = manager.get_num_users(SECRETS_FILE)

print("number_of_users:" + str(numUsers))

for number in range(0, numUsers):
	try:
		sess = manager.load_user(number,SECRETS_FILE)
	except AssertionError:
		print("FAILED:" + str(number) + "-user_load_failed")
		break
	dropboxClient = client.DropboxClient(sess)

	print("user_number:" + str(number))
	print("schooltraq_api_key:" + str(manager.User.stq_api_key))

	assignments = getAssignments.getAssignments(manager.User.stq_api_key)

	#Create the triggers for the assignments
	essayTrigger = Trigger_Schooltraq_Essay.Trigger_Schooltraq_Essay(None, dropboxClient)
	researchTrigger = Trigger_Schooltraq_Research.Trigger_Schooltraq_Research(None, dropboxClient)

	#Log the number of assignments at this time
	print("asn_count:" + str(len(assignments)))

	#Analyse the assignments
	for a in assignments:
		essayTrigger.setAssignment(a)
		researchTrigger.setAssignment(a)
		if essayTrigger.isTriggered():
			essayTrigger.runTrigger()
		elif researchTrigger.isTriggered():
			researchTrigger.runTrigger(manager.User.stq_api_key)

#Log the finish time
now = datetime.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))


