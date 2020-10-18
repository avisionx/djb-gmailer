import re


class ComplaintParser:

    def __init__(self):
        self.keyList = {
            'NAME:': 'name',
            'ADDRESS:': 'address',
            'CONTACT NO.:': 'contact',
            'KNO:': 'kno',
            'ISSUE:': 'issue',
        }
        self.whitespacelist = ["", " ", "\n", " \n", "\n ", "\t", " \t", "\t "]

    def parse(self, body):
        issue_params = {
            'name': None,
            'address': None,
            'contact': None,
            'kno': None,
            "issue": None
        }
        for key in self.keyList.keys():
            body = body.replace(key, "||"+key)
            
        keysToFind = list(self.keyList.keys())
        issueDump = ""
        for data in body.split("||"):
            cleanData = " ".join(data.split())
            if cleanData in self.whitespacelist:
                continue
            foundPlace = False
            for key in keysToFind:
                pattern = re.compile(key)
                match = pattern.match(cleanData)
                if match:
                    foundPlace = True
                    keysToFind.remove(key)
                    tag = self.keyList[key]
                    issue_params[tag] = cleanData.replace(key, "")
                    continue
            if not foundPlace:
                issueDump += cleanData + " "
        try:
            issue_params['issue'] += issueDump
        except:
            pass

        for key in issue_params.keys():
            if(issue_params[key] == None):
                return (issue_params, True)

        return (issue_params, False)


if __name__ == "__main__":
    complaintParser = ComplaintParser()
    print(complaintParser.parse('''NAME: Ram gopal shashtri
    ADDRESS: Plot no. 9(GF) Roshan garden, Najafagarh park 110043CONTACT NO.:9319525030
    KNO:6536662086 ISSUE: I have facing problem regardin g new Meter connection and it's been more than 2 Month's kindly resolve my issue asap'''))
