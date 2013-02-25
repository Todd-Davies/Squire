import requests, json
import Assignment

def updateAssignment(asn, api_key):
        payload = {'type'         : 'update', 
		   'request'      : 'assignment',
		   'key'          : api_key,
		   'assignmentid' : asn.id,
		   'asndue'       : asn.due,
		   'asnname'      : asn.name,
		   'asnnotes'     : asn.notes,
		   'asnclass'     : asn.classid}

        asn_update_request = requests.post('http://schooltraq.com/api', data=payload)

	return True if asn_update_request.json()["response"]=="success" else False