from Beec import Checking, CommanFunctions as comFunc, EstablishConnection as SqlConn, app
import flask, json, os, re
from flask import session, redirect, url_for, request

@app.route('/')
def index():
    return flask.render_template("index.html")

@app.route("/beecStyle.css")
def styles():
    return flask.render_template("beecStyle.css")

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
#         ''' WEB FUNCIONS ''' Those function should only be used on website '''
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

@app.route('/home', methods=['GET'])
def openHome():
    if comFunc.checkLogin() == False:
        return redirect(url_for('login'))
    return flask.render_template("homepage.html",  first_header='Welcome', p1=session['FullName'])

@app.route('/company', methods=['GET', 'POST'])
def compnayEdit():
    if comFunc.checkLogin() == False:
        return redirect(url_for('login'))

    if request.method == 'POST':
        return CallFor(callingAddress="compnayEdit", \
                       parametersList="`companyid`, `companyname`, `websitelink`, `representiviteid`", \
                       TableName='company', IdName='companyid', \
                       inCondation="`companyid`=%(companyid)s")

    theList = comFunc.DropListTags(
        "SELECT `companyid`,`companyname` FROM `company` WHERE `representiviteid`=" + str(session['UserID']))
    # return open("HTML/Address.html").read().format(TheList=theList)
    return flask.render_template("editCompany.html")

@app.route('/department', methods=['GET', 'POST'])
def departmentEdit():
    if comFunc.checkLogin() == False:
        return redirect(url_for('login'))

    if request.method == 'POST':
        return CallFor(callingAddress="departmentEdit", \
                       parametersList="`departementid`, `departementname`, `landphone1`, `landphone2`, `email`, `email2`, `website`, `belongtocomapny`, `addressid`", \
                       TableName='departement', IdName='departementid', \
                       inCondation="`departementid`=%(departementid)s")

    return flask.render_template("department.html")

@app.route('/address', methods=['GET', 'POST'])
def AddressEdit():
    if comFunc.checkLogin() == False:
        return redirect(url_for('login'))

    if request.method == 'POST':
        return CallFor(callingAddress="AddressEdit", \
                       parametersList="`addressid`, `firstline`, `streetname`, `unitid`, `postoffice`, `area`, `quarter`, `addressname`, `countryid`, `AddedBy`", \
                       TableName='addresseslists', IdName='addressid', \
                       inCondation="`addressid`=%(addressid)s", ExtraData={"AddedBy": str(session['UserID'])})

    theList = comFunc.DropListTags("SELECT `addressid`,`addressname` FROM addresseslists")
    return open("Beec/HTML/Address.html").read().format(TheList=theList)

    # return flask.render_template("Address.html")

@app.route('/joblist', methods=['GET', 'POST'])
def joblistEdit():
    if comFunc.checkLogin() == False:
        return redirect(url_for('login'))

    if request.method == 'POST':
        return CallFor(callingAddress="joblistEdit", \
                       parametersList="`jobid`, `jobname`, `jobdescription`", \
                       TableName='jobslist', IdName='jobid', \
                       inCondation="`jobid`=%(jobid)s", \
                       idGenSize=3)

    return flask.render_template("joblist.html")

@app.route('/employee', methods=['GET', 'POST'])
def employeeEdit():
    if comFunc.checkLogin() == False:
        return redirect(url_for('login'))
    if request.method == 'POST':
        return CallFor(callingAddress="employeeEdit", \
                       parametersList="`empid`, `nickname`, `firstname`, `middlename`, `grandname`, `lastname`, `abuname`, `phone`, `mobile`, `hometel`, `email`, `workphone`, `notes`, `userid`, `licencesid`", \
                       TableName='employee', IdName='empid', \
                       inCondation="`empid`=%(empid)s", \
                       idGenSize=9, ExtraData={"userid": str(session['UserID'])})

    return flask.render_template("employee.html")

@app.route('/imageupload', methods=['GET', 'POST'])
def imageupload():
    if comFunc.checkLogin() == False:
        return redirect(url_for('login'))
    if request.method == 'POST':

        FileStorage = request.files["image"]

        # Get the image file name
        imageFileName = FileStorage.filename

        # Save the comming picture
        FileStorage.save(os.path.join(app.config["UploadImageFolder"], FileStorage.filename))

        # Parse the data
        FullInData = json.dumps(request.form)
        FullInData = json.loads(FullInData)

        # Clean up the name
        FullInData['ImageName'] = Checking.RemoveUnwantedChar(FullInData['ImageName'])

        # React with DB
        db = SqlConn.ConnectToDB()
        SQLs = "INSERT INTO imgsave (`Path`, `UploadedBy`, `ImageName`, `type`) VALUES " + \
               "('" + FileStorage.filename + "','" + str(session['UserID']) + "','" + FullInData[
                   'ImageName'] + "', 'F')"
        r = SqlConn.InsertSQL(db, SQLs, FullInData, returnID=False)

        if r[0] == "OK":
            return redirect("/home")
        else:
            return '<center>' + r[1] + '<center>"<meta http-equiv="refresh" content="3";url=' + url_for(
                'imageUpload') + '" />"'

    return flask.render_template("imageUpload.html")

@app.route('/theams', methods=['GET', 'POST'])
def theamsEdit():
    if comFunc.checkLogin() == False:
        return redirect(url_for('login'))
    if request.method == 'POST':
        MoreData = {}
        MoreData['createdby'] = str(session['UserID'])
        return CallFor(callingAddress="theamsEdit", \
                       parametersList="`theamid`, `theamname`, `HTMLcode`, `createdby`, `forcompany`, `licenceid`", \
                       TableName='theam', IdName='theamid', \
                       inCondation="`theamid`=%(theamid)s", \
                       ExtraData=MoreData, idGenSize=8)

    return flask.render_template("Theam.html")

@app.route('/editCards', methods=['GET', 'POST'])
def CardsEdit():
    if comFunc.checkLogin() == False:
        return redirect(url_for('login'))

    if request.method == 'POST':
        ReqnData = json.dumps(request.form)
        ReqnData = json.loads(ReqnData)
        FullInData = ReqnData

        # Clean up
        for x in FullInData:
            FullInData[x] = Checking.RemoveUnwantedChar(FullInData[x])

        # React with DB
        db = SqlConn.ConnectToDB()
        if 'newC' in request.form:
            # Generate a new ID

            FullInData['cardid'] = SqlConn.GenerateRadom(5)

            # Fix the checkbox input
            if FullInData['isprivate'] == 'on':
                FullInData['isprivate'] = "1"
            else:
                FullInData['isprivate'] = "0"

            ##############################
            #   Fix the INFO feild to JSON object
            ##############################

            # Get the Theam HTML
            para = {"applytheamid": FullInData['applytheamid']}
            ThemSQL_Result = SqlConn.SendSQL(db, "SELECT `HTMLcode` FROM `theam` WHERE `theamid`=%(applytheamid)s", para)

            # Extart the requried data
            inHTML_ParaList = re.findall(r"\{[a-zA-Z]*\}", ThemSQL_Result[0][0])
            # Remove the {} from the results
            for x in range(0, len(inHTML_ParaList)):
                inHTML_ParaList[x] = inHTML_ParaList[x][1:len(inHTML_ParaList[x]) - 1]

            ##################
            # Get the full data JSON
            FullDataJSON =   GetUserFullData(session['UserID'], app, True)
            FullDataJSON = json.loads(FullDataJSON)

            ResultJSON: dict = {}
            # Match the needed data with the data in FullDataJSON

            for oneEntry in FullDataJSON:
                if oneEntry in inHTML_ParaList:
                    ResultJSON[oneEntry] = FullDataJSON[oneEntry]

            # Fix Full Name `firstname``middlename``grandname``lastname`
            ResultJSON['FullName'] = FullDataJSON['firstname']
            if "middlename" in FullDataJSON:
                ResultJSON['FullName'] = ResultJSON['FullName'] + " " + FullDataJSON['middlename']
            if "grandname" in FullDataJSON:
                ResultJSON['FullName'] = ResultJSON['FullName'] + " " + FullDataJSON['grandname']

            ResultJSON['FullName'] = str(ResultJSON['FullName'] + " " + FullDataJSON['lastname'])

            # Assign the JSON object
            FullInData['INFO'] = json.dumps(ResultJSON, ensure_ascii=False)

            ###############################################

            # Create the Insert SQL
            SQLs = "INSERT INTO cards (`cardid`, `cardname`, `hashlink`, `isprivate`, `visitcounter`, `htmllink`, `foremployee`, `applytheamid`, `INFO`, `QRCodeImg`) VALUES " \
                   + "('" + str(FullInData['cardid']) + "','" + FullInData['cardname'] + "','" + FullInData[
                       'hashlink'] + "','" + \
                   FullInData['isprivate'] + "','0','" + FullInData['htmllink'] + "','" + \
                   str(FullInData['foremployee']) + "','" + str(FullInData['applytheamid']) + "','" + FullInData[
                       'INFO'] + "','" + \
                   str(FullInData['QRCodeImg']) + "')"

            r = SqlConn.InsertSQL(db, SQLs, FullInData, returnID=False)

            return str(r)

        elif 'editC' in request.form:
            # Create the list of paramter accordingly
            print("^^^", FullInData)

        db.close()


    else:
        return flask.render_template("EditCard.html")

@app.route('/ViewCard/', methods=['GET'])
def ViewCard():
    # Get the theam from the Database
    return flask.render_template("DisplayCard.html")

@app.route('/DisplayCard/<cardID>', methods=['GET', 'POST'])
def DisplayCard(cardID):
    if request.method == 'POST':
        cardID = request.form["cardid"]

    # Clear the input
    cardID = Checking.RemoveUnwantedChar(cardID)

    # Get the card information form DB
    TheSql = "SELECT `isprivate`,`applytheamid`,`INFO` FROM cards WHERE cardid=%(cardID)s"
    db = SqlConn.ConnectToDB()
    para = {"cardID": cardID}
    CardDB_Data = SqlConn.SendSQL(db, TheSql, para)

    if CardDB_Data == []:
        return "Card not found!"

    # Get the Theam Data
    TheSql = "SELECT HTMLcode FROM theam WHERE theamid='" + str(CardDB_Data[0][1]) + "'"
    CardTheam = SqlConn.SendSQL(db, TheSql)

    if CardTheam == []:
        return "Theam not found!"

    db.close()

    ########################3

    TheFinalHTML = CardTheam[0][0]
    CardInfo = json.loads(CardDB_Data[0][2])

    # Extart the between {} Strings
    inHTML_ParaList = re.findall(r"\{[a-zA-Z]*\}", TheFinalHTML)

    # Replace the {} with the data form the database
    for oneWord in inHTML_ParaList:
        DataPeice = oneWord[1:len(oneWord) - 1]
        TheFinalHTML = TheFinalHTML.replace(oneWord.strip(), CardInfo[DataPeice])

    return TheFinalHTML

@app.route('/SavedImage/<ImageName>', methods=['GET', 'POST'])
def displayImage(ImageName):
    return comFunc.displayImage(ImageName, app=app, IsAppServer=False)

#   -----------------------------------------------------------------------------------------------
#   -----------------------------------------------------------------------------------------------3
#           (((((((((((((  EXTRA FUNCTION FOR THIS MODUL )))))))))))))
#   -----------------------------------------------------------------------------------------------
#   -----------------------------------------------------------------------------------------------

def CallFor(callingAddress: str, parametersList: str, TableName: str, ExtraData: dict = {}, IdName: str = "",
            inCondation="", idGenSize=7):
    if comFunc.checkLogin() == False:
        return redirect(url_for('login'))

    # Parse the data
    ReqnData = json.dumps(request.form)
    if ExtraData != "":
        ExtraData = json.dumps(ExtraData)
        ReqnData = ReqnData[0:len(ReqnData) - 1] + ", " + ExtraData[1:]

    ReqnData = json.loads(ReqnData)
    FullInData = ReqnData

    # Clean up
    for x in FullInData:
        FullInData[x] = Checking.RemoveUnwantedChar(FullInData[x])

    # React with DB
    db = SqlConn.ConnectToDB()
    if 'newC' in request.form:
        # Generate a new ID

        FullInData[IdName] = SqlConn.GenerateRadom(idGenSize)

        # Create the list of paramter accordingly
        InsertList = SqlConn.makeHTML(WhatYouWant="INSERT", ParaList=parametersList)
        SQLs = "INSERT INTO " + TableName + " (" + parametersList + ") VALUES " + "(" + InsertList + ")"
        r = SqlConn.InsertSQL(db, SQLs, FullInData, returnID=False)

    elif 'editC' in request.form:
        # Create the list of paramter accordingly
        #print("^^^", FullInData)
        UpdateList = SqlConn.makeHTML(WhatYouWant="UPDATE", ParaList=parametersList)
        SQLs = "UPDATE " + TableName + " SET " + UpdateList + " WHERE " + inCondation
        r = SqlConn.SendSQL(db, SQLs, FullInData, returnDate=False)

    db.close()

    # Check Result
    if r[0] == "OK":
        return redirect("/home")
    else:
        return '<center>' + r[1] + '<center>"<meta http-equiv="refresh" content="3";url=' + url_for(
            callingAddress) + '" />"'
