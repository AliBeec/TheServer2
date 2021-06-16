import os
from flask import send_file, session

import hashlib as Hashing
import json
from Beec import app, EstablishConnection as SqlConn, mail

import flask_mail as eMail

# @app.route('/SavedImage/<ImageName>', methods=['GET','POST'])
def displayImage(ImageName, app, IsAppServer=True):

    try:
        # Create the absulte path
        imageFileName = os.path.join(app.config["UploadImageFolder"], ImageName)

        # Check if the image is there
        if os.path.isfile(imageFileName):
            return send_file(imageFileName, mimetype='image/gif')
        else:
            if IsAppServer:
                return ReturnResponse("NOT FOUND")
            else:
                return "NOT FOUND"
    except:
        if IsAppServer:
            return ReturnResponse("NOT FOUND")
        else:
            return "NOT FOUND"


# -----------------------------------------------

def checkLogin():
    try:
        if 'Username' in session:
            return True
        return False
    except KeyError as e:
        return False


#   -----------------------------------------------------------------------------------------------
#   -----------------------------------------------------------------------------------------------
#           '''     HELP FUNCATION CALLED USING THE MAIN FUNCIONS UP ONLY    '''
#   -----------------------------------------------------------------------------------------------
#   -----------------------------------------------------------------------------------------------

def hasPassword(inPassword: str) -> str:
    return Hashing.sha3_256(inPassword.encode()).hexdigest()[1:40];

def DropListTags(theSQL: str):
    db = SqlConn.ConnectToDB()
    r = SqlConn.SendSQL(db, theSQL)
    theList = ""
    for oneItem in r:
        print(oneItem)
        theList = theList + '<option value="' + str(oneItem[0]) + '">' + str(oneItem[1]) + '</option>\n'

    db.close()

    return theList

def ReturnResponse(inData, JsonMessagePassed=False):
    #data = {"Result": "Fail"}  # Your data in JSON-serializable type

    if JsonMessagePassed == False:
        # inData is plain Text, so we encapsolated in a new JSON object
        jsonR={}
        jsonR["Result"]= inData
        response = app.response_class(response=json.dumps(jsonR),
                                      status=200,
                                      mimetype='application/json')
    else:
        # inData is a Json Object, Simply send it as it is
        response = app.response_class(response=json.dumps(inData),
                                      status=200,
                                      mimetype='application/json')
    return response

def SendEmail(emailSubject:str, emailTo:str, emailBody:str):
    with app.app_context():

        msg = eMail.Message(sender=app.config.get("MAIL_USERNAME"),
                            subject=emailSubject, recipients=[emailTo], body=emailBody)
        mail.send(msg)

def getUserFullData(UserID:str):
    theSQL = "SELECT * FROM `employee`, `jobslist`, `empjob`, `departement`, `empbelongstodeprt`, `company`" + \
            " WHERE `userid`=" + UserID + \
            " AND `jobslist`.`jobid` = `empjob`.`jobid` AND `empjob`.`empid` = `employee`.`empid`" + \
            " AND `departement`.`departementid` = `empbelongstodeprt`.`departid` " + \
            " AND `empbelongstodeprt`.`empid` = `employee`.`empid` AND `company`.`companyid` = `departement`.`belongtocomapny`"

    db = SqlConn.ConnectToDB()
    if type(db) is str:
        print("DB")
        return db

    r = SqlConn.SendSQL(db, theSQL, returnColumns=True)

    if "No Data" in r:
        ColsNameList = []
        ColsNameList.append(extractColumnNames(db, "Show COLUMNS FROM `employee`"))
        ColsNameList.append(extractColumnNames(db, "Show COLUMNS FROM `jobslist`"))
        ColsNameList.append(extractColumnNames(db, "Show COLUMNS FROM `empjob`"))
        ColsNameList.append(extractColumnNames(db, "Show COLUMNS FROM `departement`"))
        ColsNameList.append(extractColumnNames(db, "Show COLUMNS FROM `empbelongstodeprt`"))
        ColsNameList.append(extractColumnNames(db, "Show COLUMNS FROM `company`"))

        JsonArray = {}

        for oneItem in ColsNameList:
            for oneColm in oneItem:
                JsonArray[oneColm] = ""

        return json.dumps(JsonArray)

    return json.dumps(r, ensure_ascii=False, default=DataTimeHandler).encode('utf8')

def DataTimeHandler(obj):
    return str(obj)

def extractColumnNames(db, SqlIn:str):
    ColsNameList = SqlConn.SendSQL(db, SqlIn)
    tempList = []
    for oneCol in ColsNameList:
        tempList.append(oneCol[0])

    return tempList

def addImageToDB(FileName:str, ImageName:str):

    db = SqlConn.ConnectToDB()

    SQLs = "INSERT INTO imgsave (`Path`, `UploadedBy`, `ImageName`, `type`) VALUES " + \
           "('" + FileName + "','" + str(session['UserID']) + "','" + ImageName + "', 'F')"
    return SqlConn.InsertSQL(db, SQLs)

# print("ME:", getUserFullData("0"))