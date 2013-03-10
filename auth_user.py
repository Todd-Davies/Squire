from DropboxInterface import StoredSession
from credentials_manager import CredentialsManager

class AuthUser:

	def auth(self):
		user = CredentialsManager.User()
		user.app_key = "ykbwjy6ttncuosa"
		user.app_secret = "7r6r036gr06v094"
		user.access_type = "app_folder"
		user.user = raw_input("Enter Schooltraq username: ")
		user.stq_api_key = raw_input("Enter Schooltraq API key: ")

		dropbox_session = StoredSession.StoredSession(user.app_key,user.app_secret,user.access_type)
		user.dropbox_token = dropbox_session.link()
		manager = CredentialsManager()
		manager.add_user("/home/pi/squire/secrets.txt", user)