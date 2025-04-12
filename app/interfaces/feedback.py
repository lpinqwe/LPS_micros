import json


class Feedback:


    @classmethod
    def from_map(self,json_map):
        return json.dumps(json_map)
    def __init__(self, purpose="info", ID_of_text="sysMsg", payload="testMsg", consum=''):

        self.purpose = purpose
        self.username = ID_of_text
        if(consum==''):
            consum=[ID_of_text]
        self.consum=consum
        if(payload == None):
            payload=""
        self.payload = payload

    def get_data(self):
        return {
            "purpose": self.purpose,
            "id": self.username,
            "payload": self.payload,
            "consumers":self.consum
        }

    def __str__(self):
        return json.dumps(self.get_data(),ensure_ascii=False)
