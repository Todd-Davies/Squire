import cmd, locale, os, shlex, dropbox, json, Trigger_Schooltraq_Essay, Trigger_Schooltraq_Research
from cStringIO import StringIO
from string import Template
from dropbox import client, rest, session
from Schooltraq import Assignment, getAssignments
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
		print("Credentials loaded successfully")
	except IOError:
		print("Error - no secrets.txt file found")
		exit()

class StoredSession(session.DropboxSession):
    """a wrapper around DropboxSession that stores a token to a file on disk"""
    TOKEN_FILE = "/home/pi/squire/token_store.txt"

    def load_creds(self):
        try:
            stored_creds = open(self.TOKEN_FILE).read()
            self.set_token(*stored_creds.split('|'))
            print("Credentials loaded successfully")
        except IOError:
            pass # don't worry if it's not there

    def write_creds(self, token):
        f = open(self.TOKEN_FILE, 'w')
        f.write("|".join([token.key, token.secret]))
        f.close()

    def delete_creds(self):
        os.unlink(self.TOKEN_FILE)

    def link(self):
        request_token = self.obtain_request_token()
        url = self.build_authorize_url(request_token)
        print "Copy and paste the following URL into your browser, and authorise Squire. When you're done, press enter."
        print "Url:", url
        raw_input()

        self.obtain_access_token(request_token)
        self.write_creds(self.token)

    def unlink(self):
        self.delete_creds()
        session.DropboxSession.unlink(self)

def fillInTemplate(templateType, asn):
	f = open('./templates/' + templateType)
	s = Template(f.read())
	return (s.safe_substitute(title=asn.name, author=str(dropboxClient.account_info()['display_name'])))
	
print("---Squire---")
now = datetime.datetime.now()
print("Started on " + now.strftime("%Y-%m-%d %H:%M:%S"))
print("Loading application secrets")
loadSecrets()
print("Loading dropbox credentials")
sess = StoredSession(APP_KEY,APP_SECRET,ACCESS_TYPE)
dropboxClient = client.DropboxClient(sess)

sess.load_creds()

if not sess.is_linked():
	sess.link()

print("Downloading Schooltraq assignments")
assignments = getAssignments.getAssignments(STQ_API_KEY);
print(str(len(assignments)) + " assignments found")
print("Analysing assignments for triggers")
essayTrigger = Trigger_Schooltraq_Essay.Trigger_Schooltraq_Essay(None, dropboxClient)
researchTrigger = Trigger_Schooltraq_Research.Trigger_Schooltraq_Research(None, dropboxClient)
for a in assignments:
	essayTrigger.setAssignment(a)
	researchTrigger.setAssignment(a)
	if essayTrigger.isTriggered():
		print("Trigger found for asn id: " + a.id)
		essayTrigger.runTrigger()
	elif researchTrigger.isTriggered():
		print("Trigger found - " + "doing research on for assignment id " + a.id)
		researchTrigger.runTrigger(STQ_API_KEY)
now = datetime.datetime.now()
print("Finished on " + now.strftime("%Y-%m-%d %H:%M:%S"))
