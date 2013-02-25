import dropbox
from Schooltraq import Assignment
from cStringIO import StringIO
from string import Template

#Create an essay template from a Schooltraq assignment in the Dropbox
class Trigger_Schooltraq_Essay:
	def __init__(self,assignment, dropboxClient):
		self.assignment = assignment
		self.dropboxClient = dropboxClient

	def setAssignment(self, newAssignment):
		self.assignment = newAssignment

	def fillInTemplate(self, templateType, asn):
		f = open('./templates/' + templateType)
		s = Template(f.read())
		return (s.safe_substitute(title=asn.name, author=str(self.dropboxClient.account_info()['display_name'])))

	def isEssayPathFree(self, essayPath):
		a = self.assignment
		try:
			metadata = self.dropboxClient.metadata(essayPath);
			if (metadata.get("bytes", 0) == 0): #The file has 0 bytes
				if (metadata.get("is_deleted", False) == True): #The file is deleted
					return False
				else:
					return True
			else:
				return False #File already exists
		except dropbox.rest.ErrorResponse, e:
			if e.status == 404: #Good, the file wasn't there in the first place
				return True
			else:
				return False #Something bad happened (like quota exceeded)
			pass

	def uploadEssay(self, essayPath, essayFile):
		return self.dropboxClient.put_file(self.essayPath, self.essayFile)

	def isTriggered(self):
		a = self.assignment
		return (a.name[:8].lower()=='essay on' and a.done=="false" and a.archived=="false")

	def runTrigger(self, printPrefix="> "):
		a = self.assignment
		#Work out and define the path to the essay directory (Homework/<Classname>/<Essays/<EssayName>)
		dirPath = "Homework/" + a.classname.replace (" ", "_") + "/Essays/" + a.name[9:].replace (" ", "_")
		#Work out the path to the essay
		essayPath = dirPath + "/" + a.name[9:].replace (" ", "_") + ".tex"
		#Generate the template from the assignment
		gen = self.fillInTemplate('essay', a)
		#Create an uploadable file object from the template
		essayFile = StringIO(gen)
		#Check the essay path is free
		if self.isEssayPathFree(essayPath):
			try:
				response = self.uploadEssay(essayPath, essayFile)
				print(printPrefix + "template created succesfully: " + response["size"])
			except dropbox.rest.ErrorResponse, e:
				print(printPrefix + "ERROR: couldn't create template: " + e.status)
		else:
			print(printPrefix + "ERROR: path " + essayPath + " already taken")