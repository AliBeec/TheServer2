import flask
from flask import request, session, redirect, url_for

import json
import hashlib as Hashing
import flask_mail as eMail

from Beec import Checking, CommanFunctions as beecFunc, app, EstablishConnection as SqlConn, TheSystemMessages as Msgs, mail

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Login")
    if request.method == 'POST':

        # Check if POST request has the Username paramter
        if 'Username' in request.form:
            # OK
            pass
        else:
            # Not passed
            print("Wrong Request")
            return "WORNG REQUEST";

        # Parse the data
        FullInData = json.dumps(request.form)
        FullInData = json.loads(FullInData)

        # Clean the username
        if Checking.CheckEamilFormat(FullInData['Username']):
            username = FullInData['Username']
        else:
            print("Wrong Request2")
            if 'WEB' not in FullInData:
                return beecFunc.ReturnResponse("Fail")

            return flask.render_template("loginpage.html", SystemMessage="Wrong user name or password. Please try again.")

        password = beecFunc.hasPassword(FullInData['password'])

        # Send the sql
        db =  SqlConn.ConnectToDB()

        if type(db).__name__ == "str":
            print("Wrong Request3 db", db)
            return beecFunc.ReturnResponse("error")

        #print(password)
        para = {"username": username, "password": password}
        r = SqlConn.SendSQL(db, "SELECT `ourusers`.`userid`, `ourusers`.`email`, `CanLogin`, `verified`, `points`, `userroleid`, " + \
                            "`employee`.`firstname`, `employee`.`lastname` FROM `ourusers`, `employee` WHERE `employee`." +  \
                            "userid = ourusers.userid AND `ourusers`.`email` = %(username)s AND `password`=%(password)s AND " + \
                            "`CanLogin`=1 AND verified=1 LIMIT 1", para)
        db.close()

        # Check the user
        if r != []:
            # Open the session
            print(r)
            session['Username'] = username
            session['UserID'] = r[0][0]
            session['Email'] = r[0][1]
            session['CanLogin'] = r[0][2]
            session['Verified'] = r[0][3]
            session['Points'] = r[0][4]
            session['UserRoleID'] = r[0][5]
            session['FullName'] = r[0][6] + " " + r[0][7]

            if 'WEB' not in FullInData:
                responseDic = {"Result": "Success!"}

                for l in session:
                    responseDic[l] = session[l]

                response = app.response_class(response=json.dumps(responseDic),
                                              status=200,
                                              mimetype='application/json')

                return response  # ReturnResponse("Success!")
            else:
                return redirect("/home")

            # return open("HTML/homepage.html").read().format(first_header='Welcome', p1=session['FullName'])
        else:
            # Wrong user name or password
            if 'WEB' not in FullInData:
                print("Fails")
                return beecFunc.ReturnResponse("Fail")
            else:
                return flask.render_template("loginpage.html",
                                             SystemMessage="Wrong user name or password. Please try again.")

    print("NOT POST")
    return flask.render_template("loginpage.html")

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'Username' in session:
        # remove the username from the session if it's there
        session.clear()

    print("Logout Successful!")
    return beecFunc.ReturnResponse("Successful")

@app.route('/Register', methods=['GET', 'POST'])
def RegisterNewUser():
    if request.method == 'POST':
        # Convert the input to JSON object
        FullInData = json.dumps(request.form)
        FullInData = json.loads(FullInData)

        # print("Resived:", FullInData)

        try:
            # return FullInData;

            # Check email format
            if Checking.CheckEamilFormat(FullInData['email']):
                # Check email Match
                if (FullInData['email']) == (FullInData['Reenter'] or 'WEB' not in FullInData):
                    print("email check passed")
                    pass
                else:
                    if 'WEB' not in FullInData:
                        return beecFunc.ReturnResponse("Email Match")
                    else:
                        return Msgs.getErrorMessage(0, "EN")
            else:
                if 'WEB' not in FullInData:
                    return beecFunc.ReturnResponse("Email Format")
                else:
                    return Msgs.getErrorMessage(1, "EN")

            # Check Password Match
            if FullInData['Passowrd'] == FullInData['pReenter'] or 'WEB' not in FullInData:
                # Password Complexity
                d = Checking.passwordComplexity(FullInData['Passowrd'])

                if d == "OK":
                    print("Password Complexity Passed")
                    pass
                else:
                    print("Password Complexity FAILD")
                    if 'WEB' not in FullInData:
                        return beecFunc.ReturnResponse("Pwd Complexity")
                    else:
                        return Msgs.getErrorMessage(2, "EN")
            else:
                if 'WEB' not in FullInData:
                    return beecFunc.ReturnResponse("Pwd Match")
                else:
                    return Msgs.getErrorMessage(3, "EN")

            # Virify the username
            # FullInData['UserName'] = Checking.RemoveUnwantedChar(FullInData['UserName'])

            # Clean all input data
            for x in FullInData:
                if x != "Passowrd" and x != "email":
                    FullInData[x] = Checking.RemoveUnwantedChar(FullInData[x])
        except KeyError:
            if 'WEB' not in FullInData:
                return beecFunc.ReturnResponse("Passed Key error: " + str(KeyError))
            else:
                return "Passed Key error: " + str(KeyError)
        except:
            if 'WEB' not in FullInData:
                return beecFunc.ReturnResponse("Other Error")
            else:
                return "Some error in you request"

        # ----------------------------------------
        #   Everything is ok
        # ----------------------------------------

        print("Everything is OK")

        # Create User ID
        FullInData['userid'] = str(SqlConn.GenerateRadom(8))
        FullInData['password'] = beecFunc.hasPassword(FullInData['Passowrd'])

        # Connect to the SQL serer
        dbConn = SqlConn.ConnectToDB()

        # 1 Insert the user
        ResultData = SqlConn.InsertSQL(dbConn,
                                       "INSERT INTO `ourusers`(`CanLogin`,`points`,`userroleid`,`userid`, `email`,`password`) VALUES (1, 0, 122, %(userid)s, %(email)s, %(password)s )",
                                       FullInData, False)

        # Check if result is ok
        if ResultData == None or ResultData[0] != "OK":
            if 'WEB' not in FullInData:
                return beecFunc.ReturnResponse(ResultData)
            else:
                return str(ResultData)

        # 2 Get the new created Licese ID
        # LicSQL = SqlConn.SendSQL(dbConn, "SELECT `licencesid` FROM `licences` WHERE `type`='E' AND `CreatedFor`=' " + str(UserID) + "'")

        para = {"username": FullInData['userid']}
        LicSQL = SqlConn.SendSQL(dbConn,
                                 "SELECT `licencesid` FROM `licences` WHERE `type`='E' AND `CreatedFor`=%(username)s",
                                 para)
        # print(FullInData['userid'])
        FullInData["LicenceID"] = str(LicSQL[0][0])

        # 3 Create and employee

        # print("FullInData[1LicenceID1]=", FullInData["LicenceID"])
        myInsert = "INSERT INTO `employee`(`empid`, `nickname`, `firstname`, `middlename`, `grandname`, `lastname`, `abuname`, " + \
                   "`phone`, `mobile`, `hometel`, `email`, `workphone`, `notes`, `userid`, `licencesid`) VALUES ('1'," + \
                   " %(Nickname)s , %(FirstName)s, %(MiddleName)s , %(GrandFatherName)s , %(FamilyName)s ,%(AbuName)s , %(PhoneNumber)s" + \
                   ", %(MobileNumber)s , %(HomePhone)s , %(email)s , %(Workphone)s , %(notes)s , %(userid)s , %(LicenceID)s )"

        ResultData = SqlConn.InsertSQL(dbConn, myInsert, FullInData, True)

        # ------------
        # 4 SEND EMAIL

        if ResultData[0] == "OK":
            # Create the Verifcation code
            VirifcationCode = str(SqlConn.GenerateRadom(3))
            VirifcationCode = Hashing.sha3_256(VirifcationCode.encode()).hexdigest()[2:10]
            VirifcationCode = VirifcationCode.upper()

            # Save the code to the database
            para = {"vcode": VirifcationCode, "userID": FullInData['userid']}
            SqlConn.InsertSQL(dbConn, "INSERT INTO `verifications`(`vercode`, `UserID`) VALUES (%(vcode)s,%(userID)s )",
                              para, False)

            # Send the email
            beecFunc.SendEmail(emailSubject="Avtivate you account with eCards", emailTo=FullInData['email'],
                               emailBody="Hi Mr. " + FullInData['FirstName'] + \
                                         ", \n You have register with us and complete your registration please click the line bellow or use this Code:\n" + \
                                         VirifcationCode + " \n Thank you ...")

            # Close DB Connection
            SqlConn.CloseConnection(dbConn)

            # 5 Redirect to verificaiton
            RR = flask.send_from_directory("HTML", "EmailVerifcation.html")
            if 'WEB' not in FullInData:
                return beecFunc.ReturnResponse({"Result":"OK", "UserID":ResultData[1] }, True)
            else:
                return str(RR)

        # Close DB Connection
        SqlConn.CloseConnection(dbConn)

        if 'WEB' not in FullInData:
            return beecFunc.ReturnResponse(ResultData)
        else:
            return str(ResultData)

        # return Msgs.getErrorMessage(4, "EN") + FullInData['UserName']

    elif request.method == 'GET':
        # If it get, simply return the registration form
        return flask.send_from_directory("HTML", "Register.html")

@app.route('/emailVerfication', methods=['POST', 'GET'])
def emailVerfication():

    if request.method == 'POST':
        FullInData = json.dumps(request.form)
        FullInData = json.loads(FullInData)
        inVerCode = Checking.RemoveUnwantedChar(FullInData['VerCode'])

        if len(inVerCode) == 8:
            myDB = SqlConn.ConnectToDB()

            para = {"VarCard": inVerCode}
            SQLResult = SqlConn.SendSQL(myDB, "SELECT `userid` FROM `verifications` WHERE `vercode` = %(VarCard)s AND `enddate` > NOW()" \
                                        , parameters=para)

            if SQLResult != None:
                SqlConn.SendSQL(myDB, "UPDATE `ourusers` SET `verified`=TRUE WHERE `userid`='" + str(SQLResult[0][0]) + "'", \
                                returnDate=False)
                myDB.close()
                if 'WEB' not in FullInData:
                    return beecFunc.ReturnResponse("OK")
                else:
                    return flask.send_from_directory("HTML", "loginpage.html")

        if 'WEB' not in FullInData:
            return beecFunc.ReturnResponse("Wrong code!")
        else:
            return flask.send_from_directory("HTML", "EmailVerifcation.html")
    else:
        if 'WEB' not in request.form:
            return beecFunc.ReturnResponse("Wrong code!")
        else:
            return flask.send_from_directory("HTML", "EmailVerifcation.html")

@app.route('/resendVerfication/<UserID>', methods=['POST', 'GET'])
def resendVerifcaiton(UserID):

    #Clean the Passed UserID
    UserID =  Checking.RemoveUnwantedChar(UserID)

    # Connect to the SQL serer
    dbConn = SqlConn.ConnectToDB()

    # Check if the user exisits and get its data
    para = {"userID": UserID}
    ur = SqlConn.SendSQL(dbConn, "SELECT ourusers.`email` as email, `firstname`, `lastname` FROM ourusers, `employee` " + \
                      "WHERE ourusers.`userid`=%(userID)s AND verified = 0 AND ourusers.userid = employee.userid", para)

    if ur == None:
        return beecFunc.ReturnResponse("Fail")

    # Create new Verifcation code
    VirifcationCode = str(SqlConn.GenerateRadom(3))
    VirifcationCode = Hashing.sha3_256(VirifcationCode.encode()).hexdigest()[2:10]
    VirifcationCode = VirifcationCode.upper()

    # Update the code to the database
    para = {"vcode": VirifcationCode, "userID": UserID}
    SqlConn.InsertSQL(dbConn, "UPDATE `verifications` SET `vercode`= %(vcode)s WHERE `UserID`=%(userID)s", para, False)

    # Close DB Connection
    SqlConn.CloseConnection(dbConn)

    # Send the email
    beecFunc.SendEmail(emailSubject="Avtivate you account with eCards", emailTo=ur[0][0],
                       emailBody="Hi Mr. " + ur[0][1] + " " + ur[0][2] + \
                                 ", \n You have register with us and complete your registration please click the line bellow or use this Code:\n" + \
                                 VirifcationCode + " \n Thank you ...")

    return beecFunc.ReturnResponse("OK")

@app.route('/forget', methods=['GET', 'POST'])
def forgetPassword():
    if request.method == "GET":
        return flask.send_from_directory("HTML", "ForgetRequest.html")
    else:
        inEmail = request.form['email']

        if Checking.CheckEamilFormat(inEmail) == False:
            return "Wrong email address format"

        db = SqlConn.ConnectToDB()

        para = {"inEmail":inEmail}
        # Check if email is there
        r = SqlConn.SendSQL(db, "SELECT concat(`firstname`,' ',`lastname`) as FullName, `ourusers`.`userid` \
            FROM `employee`, `ourusers` WHERE `ourusers`.`userid` = `employee`.`userid` \
            AND `ourusers`.`email`=%(inEmail)s LIMIT 1", para)

        if 'err' in r:
            db.close()
            return "email not found"

        # Generate the Verfication code

        # Create the Verifcation code
        VirifcationCode = str(SqlConn.GenerateRadom(5)) + inEmail
        VirifcationCode = Hashing.sha3_256(VirifcationCode.encode()).hexdigest()[3:13]
        VirifcationCode = VirifcationCode.upper()

        # Save the code to the database
        para = {"vcode": VirifcationCode, "userID": r[0][1]}
        SqlConn.SendSQL(db, "UPDATE `verifications` SET `vercode`=%(vcode)s, `enddate`=DATE_ADD(NOW(), INTERVAL 4 HOUR_MINUTE) WHERE UserID = %(userID)s limit 1"
                        , para, False)

        db.close()

        # Send the email
        with app.app_context():
            msg = eMail.Message(subject="Forget account password with eCards",
                                sender=app.config.get("ali.bhp@gmail.com"),
                                recipients=[inEmail],
                                body="Hi Mr. " + str(r[0][0]) +
                                     ", \n You have register with us and complete your registration please click the line bellow or use this Code:\n" + \
                                     str(VirifcationCode) + " \n Thank you ...")
            mail.send(msg)

        return flask.send_from_directory("HTML", "ForgetVerifcation.html")

@app.route('/forgetVeri', methods=['POST'])
def forgetPwdVeri():

    if 'VerifcationCode' in request.form:
        incode = request.form['VerifcationCode']

        db = SqlConn.ConnectToDB()

        para = {'incode':incode}
        r = SqlConn.SendSQL(db, "SELECT `UserID` FROM `verifications` WHERE `vercode`=%(incode)s AND `enddate`> NOW() LIMIT 1", para)

        if 'err' in r:
            db.close()
            return str(r)
        else:
            if 'passwordCheck' in request.form and 'NewPassword' in request.form:
                if request.form['passwordCheck'] == request.form['NewPassword']:
                    para = {"NewPassword":beecFunc.hasPassword(request.form['NewPassword']), "UserID":r[0][0]}
                    SqlConn.SendSQL(db, "UPDATE `ourusers` SET `password`= %(NewPassword)s WHERE `userid`=%(UserID)s",
                                        para, returnDate=False)
                    db.close()
                    return redirect("/login")

    else:
        return flask.send_from_directory("HTML", "ForgetVerifcation.html")

