import dropbox
from Schooltraq import Assignment
from cStringIO import StringIO
from string import Template

#Create an essay template from a Schooltraq assignment in the Dropbox
class Trigger_Schooltraq_Essay:
	def __init__(self,assignment, dropboxClient):
		self.assignment = assignment
		self.dropboxClient = dropboxClient
		self.dirPath = ""
		self.essayPath = ""

	def findPaths(self):
		#Work out and define the path to the essay directory (Homework/<Classname>/<Essays/<EssayName>)
		self.dirPath = "Homework/" + self.assignment.classname.replace (" ", "_") + "/Essays/" + self.assignment.name[9:].replace (" ", "_")
		#Work out the path to the essay
		self.essayPath = self.dirPath + "/" + self.assignment.name[9:].replace (" ", "_") + ".tex"

	def setAssignment(self, newAssignment):
		self.assignment = newAssignment
		self.findPaths()

	def fillInTemplate(self, templateType, asn):
		f = open('/home/pi/squire/templates/' + templateType)
		s = Template(f.read())
		return (s.safe_substitute(title=asn.name, author=str(self.dropboxClient.account_info()['display_name'])))

	def isEssayPathFree(self):
		a = self.assignment
		try:
			metadata = self.dropboxClient.metadata(self.essayPath);
			if (metadata.get("bytes", 0) == 0): #The file has 0 bytes
				if (metadata.get("is_deleted", False) == True): #The file is deleted
					return True
				else:
					return False
			else:
				return False #File already exists
		except dropbox.rest.ErrorResponse, e:
			if e.status == 404: #Good, the file wasn't there in the first place
				return True
			else:
				return False #Something bad happened (like quota exceeded)
			pass

	def uploadEssay(self, essayFile):
		return self.dropboxClient.put_file(self.essayPath, essayFile)

	def isTriggered(self, printOut=True, printPrefix="> "):
		a = self.assignment
		if a.name[:8].lower()=='essay on' and a.done=="false" and a.archived=="false" and self.isEssayPathFree():
			if printOut:
				print(printPrefix + "Trigger found for asn id: " + a.id)
			return True
		return False

	def runTrigger(self, printPrefix="> "):
		a = self.assignment
		#Generate the template from the assignment
		gen = self.fillInTemplate('essay', a)
		#Create an uploadable file object from the template
		essayFile = StringIO(gen)
		#Check the essay path is free
		if self.isEssayPathFree():
			try:
				response = self.uploadEssay(essayFile)
				print(printPrefix + "Template created successfully: " + response["size"])
			except dropbox.rest.ErrorResponse, e:
				print(printPrefix + "ERROR: couldn't create template: " + str(e.status) + " - " + e.reason)
		else:
			print(printPrefix + "ERROR: path already taken")