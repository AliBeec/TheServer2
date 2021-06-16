import Beec.EstablishConnection as SqlConn
from flask import session
from Beec.CommanFunctions import checkLogin

def companyAndDepartmentInfo():

    if checkLogin() == False:
        return ['err', "Login"]

    db = SqlConn.ConnectToDB()

    SqlStatment = "SELECT `departement`.* FROM `departement` WHERE `departement`.`belongtocomapny` = " + \
                    "( SELECT companyid FROM `company` WHERE `company`.`representiviteid` = " + session['EmpID']

    Result = SqlConn.SendSQL(db, SQLStatment=SqlStatment)

    db.close()

    return Result