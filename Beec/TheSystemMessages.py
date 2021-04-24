ErrorMessagesENG = ["Entered Emails and the conformation is not matached!",
"Entered Emails format is not accaptable!",
"The Entered Password is not complex enough! please chose a differnt password",
"Entered password and the conformation is not matached!" ,
"OK",
"The Entered email address exisits in our database. Please login or use different email address."]
ErrorMessagesARB = [

]
SpicalText = ["User Registration was completed successfully. A verifcation email was send to your register email to complete the registration"]


def getErrorMessage(msgID:int, Languge:str):
    if Languge == "EN":
        return ErrorMessagesENG[msgID]
    elif Languge == "AR":
        return ErrorMessagesARB[msgID]

def getSpicalText (msgID:int, Language:str):
    if Language == "EN":
        return SpicalText[msgID]
    elif Language == "AR":
        return SpicalText[msgID]
