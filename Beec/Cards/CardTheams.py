import Beec.EstablishConnection as SqlConn
from flask import session

#   - Theam(String that tell what colors seperated with '-', ORDER: Background, FontColor, BoarerColor) d
#                       (COLORS ARE IN R, G, B for each '-' string)

def checkTheamLicence(licencesType:str):

    # thre return has this shap:
    #   If OK ["Ok", LicenceID, Current ActiveLicence]
    #   IF Ok but the use has no valide licence ["Reject", LicenceID]

    if licencesType == 'T' or licencesType == 'E':
        None
    else:
        return ['err', 'Unknown licences Type']

    db = SqlConn.ConnectToDB()
    dbAnswer = SqlConn.SendSQL(db, "SELECT * FROM licences WHERE type='" + licencesType + "' AND CreatedFor=" + session['UserID'])
    db.close()

    if 'err' in dbAnswer:
        return ['err', 'No Licence']
    else:
        # Check if still has more to use
        # if (ActivatedCount) < ( MaxUsingCount )
        #print(dbAnswer[0][2],dbAnswer[0][3] )
        if int(dbAnswer[0][2]) < int(dbAnswer[0][3]):
            # Return the licence ID, ActivatedCount
            return ['OK', dbAnswer[0][0], dbAnswer[0][2]]
        else:
            return ['Rejected', dbAnswer[0][0]]

def AddNewTheam(ThemName:str, TheamInfo:str, ThemStyleID:int, DeptID:int):

    # NOT TEST AT ALL
    # Theam info is a JSON object that has all needed info for the insertion query
        # - theamname
        # - TheamInfo
        # - forDepartment

    # Retun the new inserted theam number

    LicenceCheck = checkTheamLicence('T')

    if 'OK' not in LicenceCheck:
        return ['err', 'Licence Rejection']

    db = SqlConn.ConnectToDB()

    InserSQL = "INSERT INTO `theam`(`theamname`, `colorcodes`, `StyleID`, `createdby`, `forDepartment`, `licenceid`)" \
                        " VALUES (" + ThemName + "," + TheamInfo + "," + str(ThemStyleID) + "," + session["UserID"] + \
                        "," + str(DeptID) + "," + LicenceCheck[1] + ")"

    TheamID = SqlConn.InsertSQL(Conn=db, SQLStatment=InserSQL)

    db.close()

    # NOTE: Licenect update is done automatically by the databse enginge

    if 'err' in TheamID:
        return TheamID
    else:
        return ['OK', TheamID]