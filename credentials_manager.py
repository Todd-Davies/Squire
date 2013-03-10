from DropboxInterface import StoredSession

class CredentialsManager:

	class User:
		name = ""
		stq_api_key = ""
		dropbox_token = ""
		app_key = ""
		app_secret = ""
		access_type = ""

	def load_user(self, number, file, dropbox_session=None):
		try:
			stored_creds = open(file,'r').readlines()
			lineToRead = "."
			count = 0
			for line in stored_creds:
				lineToRead = line
				if count==number:
					break
				count += 1

			count = 0

			for secret in lineToRead.split('|'):
				if count==0:
					self.User.app_key= secret.rstrip()
				elif count==1:
					self.User.app_secret = secret.rstrip()
				elif count==2:
					self.User.access_type = secret.rstrip()
				elif count==3:
					self.User.stq_api_key = secret.rstrip()
				elif count==4:
					self.User.name = secret.rstrip()
				else:
					self.User.dropbox_token += secret.rstrip() + "|"
				count += 1

			self.User.dropbox_token = self.User.dropbox_token[:self.User.dropbox_token.__len__()-1]

			dropbox_session = StoredSession.StoredSession(self.User.app_key,self.User.app_secret,self.User.access_type)

			dropbox_session.load_creds(False, self.User.dropbox_token)
			if not dropbox_session.is_linked():
				dropbox_session.link()
			return dropbox_session
		except IOError:
			return None
			pass # don't worry if it's not there


	def add_user(self, fname, user):
		to_write = user.app_key + "|"
		to_write += user.app_secret + '|'
		to_write += user.access_type + '|'
		to_write += user.stq_api_key + '|'
		to_write += user.dropbox_token
		with open(fname, "a") as secrets_file:
			secrets_file.write(to_write)

	def get_num_users(self, fname):
		with open(fname) as f:
			for i, l in enumerate(f):
				pass
		return i + 1
