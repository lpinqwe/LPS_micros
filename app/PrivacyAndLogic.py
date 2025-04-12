


class PrivacyAndLogic:

    def process(self,d):
        d=self.replace_null_with_empty(d)
        return d

    def replace_null_with_empty(self,d):
        if not isinstance(d, dict):
            return d
        for key, value in d.items():
            if(value=="null" or value==None):
                d[key]=""
        return d