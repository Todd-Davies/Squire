import requests, json
import Assignment

def getAssignments(api_key):
        payload_asn = {'type': 'get', 'request': 'assignmentlist', 'key' : api_key}
        payload_crs = {'type': 'get', 'request': 'courselist', 'key' : api_key}

        asn_request = requests.post('http://schooltraq.com/api', data=payload_asn)

        crs_request = requests.post('http://schooltraq.com/api', data=payload_crs)

        asn_json_object = asn_request.json();
        crs_json_object = crs_request.json();

	#print(api_key)

        #print(asn_request.text)
        #print(crs_request.text)

        assignments = []

        for text in asn_json_object["assignments"]:
                assignment = asn_json_object["assignments"][text]
                if(assignment["asnstatus"]=="open"):
                        course = crs_json_object["courses"][assignment["asnclass"]]
			done = ("true" if assignment["asnstatus"]=="done" else "false")
			archived = ("true" if assignment["asnstatus"]=="archived" else "false")
			importance = ("false" if assignment["asnpriority"]=="0" else "true") 
                        asn = Assignment.Assignment(assignment["asnid"], assignment["asnname"], course["classid"], course["classname"], course["classcolor"], assignment["asndue"], assignment["asnnotes"], importance, done, archived)
                        assignments.append(asn)

        return assignments
