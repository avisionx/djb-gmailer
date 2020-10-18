
class ComplaintParser:

    def __init__(self):
        pass

    def parse(self, body):
        print(body)
        issue_params = {
            'name': "Avi",
            'address': "b15",
            'contact': "con",
            'kno': "kno",
            "issue": "issue"
}
        return (issue_params, True)


if __name__ == "__main__":
    complaintParser = ComplaintParser()
    complaintParser.parse(''' 
NAME: Ram gopal shashtri 
ADDRESS: Plot no. 9(GF) Roshan garden, Najafagarh park 110043
CONTACT NO.:9319525030
KNO:6536662086
ISSUE: I have facing problem regarding new Meter connection and it's been more than 2 Month's kindly resolve my issue asap''')


