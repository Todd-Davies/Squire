import dropbox, search
from Schooltraq import Assignment, updateAssignment
 #Performs research on a Schooltraq Assignment and adds it to the notes
class Trigger_Schooltraq_Research:
	def __init__(self,assignment, dropboxClient):
		self.assignment = assignment
		self.dropboxClient = dropboxClient

	def setAssignment(self, newAssignment):
		self.assignment = newAssignment

	def isTriggered(self):
		a = self.assignment
		return (a.name[:8].lower()=="research" and a.done=="false" and a.archived=="false" and a.notes.find("**Squire** found these links:")==-1)

	def runTrigger(self, stq_api_key, printPrefix="> "):
		#Do the research
		research = search.googleAssignment(self.assignment.name[9:])
		#Append the links to the notes
		self.assignment.notes += "\n**Squire** found these links:\n" + research
		#Try and update the assignment
		if updateAssignment.updateAssignment(self.assignment, stq_api_key):
			print(printPrefix + "Research done succesfully")
		else:
			print(printPrefix + "Unable to research assignemnt - schooltraq API request failed")
