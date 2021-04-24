from Beec import EstablishConnection as SqlConn, CommanFunctions as beecFunc, app, Cards
from flask import request
import json

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
#           ''' APP FUNCION ''' Those function should only be used on APP '''
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

@app.route('/FullData/<UserID>', methods=['GET', 'POST'])
def GetUserFullData(UserID):
    # Make sure the user is loged in
    loginResult = checkLogin()
    if loginResult != True:
        print("Fulldata request rejected, login is required")
        return loginResult;

    r = json.loads(beecFunc.getUserFullData(UserID))

    if "err" in r:
        print("Error in r db 1")
        return beecFunc.ReturnResponse("NONE")

    if (len(r) == 0):
        return beecFunc.ReturnResponse("NONE")

    print("Fulldata request was sent successfully")
    # return the response object
    return app.response_class(response=json.dumps(r, ensure_ascii=False),
                                      status=200,
                                      mimetype='application/json')

def GetUserFullData_OLD(UserID):
    # Make sure the user is loged in

    loginResult = checkLogin()
    if loginResult != True:
        print("Fulldata request rejected, login is required")
        return loginResult;

    r = beecFunc.getUserFullData(UserID)

    # Create the SQL
    theSQL = "SELECT `nickname`, `firstname`, `middlename`, `grandname`, `lastname`, `abuname`, `phone`, " \
             "`mobile`, emp.`empid`, `hometel`, emp.`email` as empEmail, `workphone`, `notes`, `departementname`, `landphone1` " \
             "as detpPhone1, `landphone2` as detpPhone2, dept.`email` as DeptEmail1, `email2` as DeptEmail2, " \
             "dept.`website` as DeptWeb, `companyname`, `websitelink` as CompWeb, jobslist.jobname " \
             "FROM employee emp,empbelongstodeprt EmpDept, departement dept, company, jobslist, empjob " \
             "WHERE `userid`='" + UserID + "' AND `licencesid`!='' AND emp.`empid`=EmpDept.empid " \
                                           "AND empDept.departid = dept.departementid AND company.companyid = dept.belongtocomapny " \
                                           "AND emp.empid = empjob.empid AND empjob.jobid = jobslist.jobid"

    # Grap the data from the database
    db = SqlConn.ConnectToDB()
    r = SqlConn.SendSQL(db, theSQL)

    if "err" in r:
        print("Error in r db 1")
        return beecFunc.ReturnResponse("NONE")

    if (len(r) == 0):
        return beecFunc.ReturnResponse("NONE")

    # Clean the result
    ValueStr = str(r)
    ValueStr = ValueStr.replace("\"", "")
    ValueStr = ValueStr.replace("(", "")
    ValueStr = ValueStr.replace(")", "")
    ValueStr = ValueStr.replace("]", "")
    ValueStr = ValueStr.replace("[", "")
    ValueStr = ValueStr.replace(" ", "")
    ValueStr = ValueStr.replace("'", "")
    ValueStr = ValueStr.split(",")

    # Preper the JSON headers namse
    Names = ['nickname', 'firstname', 'middlename', 'grandname', 'lastname', 'abuname', 'phone', \
             'mobile', 'empid', 'hometel', 'empEmail', 'workphone', 'notes', 'departementname', \
             'detpPhone1', 'detpPhone2', 'DeptEmail1', 'DeptEmail2', \
             'DeptWeb', 'companyname', 'CompWeb', 'jobname']

    # Generat the final JSON result
    res = {}
    i: int = 0;
    for key in Names:
        res[key] = ValueStr[i]
        i = i + 1

    # Create the JSON Ojbect
    dd = json.dumps(res, ensure_ascii=False).encode('utf8')

    # Create the respnd ojbect
    response = app.response_class(response=dd, status=200, mimetype='application/json')

    print("Fulldata request was sent successfully")
    # return the response object
    return response


@app.route('/NewCard', methods=['POST'])
def CreateNewCard():

    if beecFunc.checkLogin() == False:
        return

    # Request :
    #   - CardInfo(JSON OBJECT tell all the data),
    #   - Theam(String that tell what colors seperated with '-', ORDER: Background, FontColor, BoarerColor) d
    #                       (COLORS ARE IN R, G, B for each '-' string)
    #   - Feilds(String List of wanted feild seperated with ":"

    if request.method == 'POST':
        # Convert the input to JSON object
        FullInData = json.dumps(request.form)
        FullInData = json.loads(FullInData)

        # Call the create Card Module
        return beecFunc.ReturnResponse("DONE")
        #return beecFunc.ReturnResponse(Cards.NewCard.NewCard(POST_REQUEST=FullInData))

def checkLogin():
    if beecFunc.checkLogin() == False:
        return beecFunc.ReturnResponse("LOGIN")
    else:
        return True