import dropbox
from dropbox import client, rest, session

class StoredSession(session.DropboxSession):
	"""a wrapper around DropboxSession that stores a token to a file on disk"""
	#TOKEN_FILE = "/home/pi/squire/token_store.txt"

	def load_creds(self, printOutput, token):
		try:
			stored_creds = input #open(self.TOKEN_FILE).read()
			#self.set_token(*stored_creds.split('|'))
			self.set_token(*token.split('|'))
			if printOutput:
				print("Credentials loaded successfully")
		except IOError:
			pass # don't worry if it's not there

	#def write_creds(self, token):
	#	f = open(self.TOKEN_FILE, 'w')
	#	f.write("|".join([token.key, token.secret]))
	#	f.close()

	def get_creds(self, token):
		return "|".join([token.key, token.secret])

	#def delete_creds(self):
	#	os.unlink(self.TOKEN_FILE)

	def link(self):
		request_token = self.obtain_request_token()
		url = self.build_authorize_url(request_token)
		print "Visit this URL and authorise Squire! When you're done, press enter."
		print "Url:", url
		raw_input()

		self.obtain_access_token(request_token)
		#self.write_creds(self.token)
		return self.get_creds(self.token)

	def unlink(self):
		#self.delete_creds()
		session.DropboxSession.unlink(self)