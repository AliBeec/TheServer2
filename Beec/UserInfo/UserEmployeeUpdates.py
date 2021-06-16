import Beec.EstablishConnection as SqlConn
import json
import sys

from Beec.CommanFunctions import getUserFullData

# --------------------------------------------------------------------------------
# This is the main function which update three tables
def updateFullInfo(inFullData:json):

    # --------------------------------------------------------------------------------
    # Employee Table UPDATE ONLY
    empUpdate = updateSingleTable(tableName='employee', newData=inFullData, condationFeild="empid",
                      exceptionColumn=['licencesid', 'userid'])
    if 'err' in empUpdate:
        print(empUpdate)
        return ["err", "Wrong input for EMPLOYEE"]

    # --------------------------------------------------------------------------------
    # Comapny
    if "companyid" in inFullData:
        compUpdate = updateSingleTable(tableName='company', newData=inFullData, condationFeild="companyid")
        if 'err' in compUpdate:
            return ['err', "Update company", compUpdate]
    else:
        compUpdate = insertNewData(tableName='company', newData=inFullData, idFeildName="companyid")
        if 'err' in compUpdate:
            return ["err", "Insertion to company", compUpdate]
        else:
            inFullData["companyid"] = compUpdate

    # --------------------------------------------------------------------------------
    # Department
    # Check if ID is given for the dept
    if "departementid" in inFullData:
        # Yes, Update hte info
        deptUpdate = updateSingleTable(tableName='departement', newData=inFullData, condationFeild="departementid")
        if 'err' in deptUpdate:
            print(deptUpdate)
            return ["err", "Update department"]
    else:
        # No, Insert a new depratment
        deptUpdate = insertNewData(tableName='departement', newData=inFullData, idFeildName="departementid")

        if 'err' in deptUpdate:
            return ["err", "Insertion to department", deptUpdate]
        else:
            # Add new depratment id to the Data
            inFullData['departementid'] = deptUpdate

            # INSERT into the Dept - Employee connection table
            inData = {"empid":inFullData["empid"], "departid":deptUpdate}
            deptEmplRe = insertNewData(tableName='empbelongstodeprt', newData=inData, idFeildName="", exceptionColumn=['startdate','enddate'])

            if 'err' in deptEmplRe :
                return deptEmplRe

    # Every thing went net, return OK, with the new JSON object
    return ["OK", inFullData]


# --------------------------------------------------------------------------------
# This funcion is used to create the UPDATE sql and send it to database

def updateSingleTable(tableName:str, newData:json, condationFeild:str , exceptionColumn = []):

    # tableName: the target to update table
    # newData: a jason or dict var that will handle the new data that need to be update with the feild names
    # condationFeild: This will be use in the WHERE close of the UDPATE SQL statment to limit the update
    # exceptionColumn: a list of feild names that the funcion should ignore when creating the SQL. Note that, the funcion will
    #       use the newData for feild names and the table's feild that will be extracted form the data base while ignoreing
    #       the ones in exceptionColumn.

    db = SqlConn.ConnectToDB()

    # Get employee tabel feilds name
    EmpTableFeildsName = SqlConn.SendSQL(db, "SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE " \
                + "`TABLE_SCHEMA`='" + SqlConn.getDatabaseName() + "' AND `TABLE_NAME`='" + tableName + "'")

    # Craft the UPDATE SQL
    SqlStatment = "UPDATE `" + tableName + "` SET "
    firstComa = False

    # Loop through the feilds
    for oneFeild in EmpTableFeildsName:

        # Remove any unwanted data
        if oneFeild[0] in exceptionColumn or oneFeild[0] == condationFeild:
            continue

        # Attach the new field
        if oneFeild[0] in newData:
            if str(newData[oneFeild[0]]).upper() == "NONE" or newData[oneFeild[0]] == "":
                continue

            # Handle the first adding comma to the sql
            if firstComa:
                SqlStatment = SqlStatment + "',"
            SqlStatment = SqlStatment + "`" + str(oneFeild[0]) + "`='" + str(newData[oneFeild[0]])

            firstComa = True

    SqlStatment = SqlStatment.strip()
    if SqlStatment[len(SqlStatment)-1] != "'":
        SqlStatment = SqlStatment + "'"

    SqlStatment = SqlStatment + " WHERE `" + condationFeild + "`='" + str(newData[condationFeild]) + "'"

    print(SqlStatment)

    finalUpdateResult = SqlConn.SendSQL (db, SqlStatment, returnDate=False)

    db.close()

    if 'err' in finalUpdateResult:
        return ["err", "Update failed", finalUpdateResult, SqlStatment]
    else:
        if finalUpdateResult[1] == 0:
            # The Update was ok, but it affact no column. Meaning, there is new data need to be inserted
            return ["NO Effect", "No Rows were affected"]
        else:
            return ["OK", ""]

# --------------------------------------------------------------------------------
# Similaer to previous funcion but this one insert the data - BECARFUL
# --------------------------------------------------------------------------------
def insertNewData(tableName:str, newData:json, idFeildName:str, exceptionColumn = []):

    db = SqlConn.ConnectToDB()

    # Get tabel feilds name
    EmpTableFeildsName = SqlConn.SendSQL(db, "SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE " \
                + "`TABLE_SCHEMA`='" + SqlConn.getDatabaseName() + "' AND `TABLE_NAME`='" + tableName + "'")

    ColumnName:str = ""
    ValuesData:str = ""

    # Loop through the feilds
    for oneFeild in EmpTableFeildsName:
        print(oneFeild[0])
        # Remove any unwanted data
        if oneFeild[0] in exceptionColumn or oneFeild[0] in idFeildName:
            continue

        # Attach the new field
        if oneFeild[0] in newData:
            if str(newData[oneFeild[0]]).lower() == "none":
                continue
            ColumnName = ColumnName + "`" + str(oneFeild[0])  + "`,"
            ValuesData = ValuesData + "'" + str(newData[oneFeild[0]]) + "',"

    # Craft the UPDATE SQL
    SqlStatment = "INSERT INTO `" + tableName + "` (" + ColumnName[0:len(ColumnName)-1] + ") VALUES (" \
                  + ValuesData[0:len(ValuesData)-1] + ")"

    print(SqlStatment)
    db.close()

    return SqlConn.InsertSQL(db, SqlStatment)

# --------------------------------------------------------------------------------

# print(updateFullInfo(getUserFullData("5973461")))
# print(insertNewData(tableName="departement", newData=getUserFullData("5973461"), idFeildName="departementid"))