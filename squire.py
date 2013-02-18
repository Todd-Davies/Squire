import cmd, locale, os, shlex, Assignment, getAssignments, dropbox, json
from cStringIO import StringIO
from string import Template
from dropbox import client, rest, session

APP_KEY = "."
APP_SECRET = "."
ACCESS_TYPE = "."
STQ_API_KEY = "."
SECRETS_FILE = "secrets.txt"

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
    TOKEN_FILE = "token_store.txt"

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
for a in assignments:
	if a.name[:8].lower()=='essay on' and a.done=="false" and a.archived=="false":
		print("Trigger found - " + "Creating essay template for assignment id " + a.id)
		path = "Homework/" + a.classname.replace (" ", "_") + "/Essays/" + a.name[9:].replace (" ", "_")
		gen = fillInTemplate('essay', a)
		try:
			dropboxClient.file_create_folder(path)
		except dropbox.rest.ErrorResponse, e:
			pass
		output = StringIO(gen)
		#Get the metadata for the file to see if it's there
		try:
			metadata = dropboxClient.metadata(path + "/" + a.name[9:].replace (" ", "_") + ".tex");
			if (metadata.get("bytes", 0) == 0): #The file has 0 bytes
				if (metadata.get("is_deleted", False) == True): #The file is deleted
					response = dropboxClient.put_file(path + "/" + a.name[9:].replace (" ", "_") + ".tex", output)
					print("> Template created successfully")
				else:
					print("> Error - a file with that name already exists") #File already exists (just with 0 bytes)
			else:
				print("> Nope I've already created that template") #File already exists
		except dropbox.rest.ErrorResponse, e:
			if e.status == 404: #Good, the file wasn't there in the first place
				response = dropboxClient.put_file(path + "/" + a.name[9:].replace (" ", "_") + ".tex", output)
				print("> Template created successfully")
			else:
				print("> Error - " + e) #Something went wrong
			pass
print("---Squire has finished---")
