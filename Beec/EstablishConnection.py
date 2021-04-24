import mysql.connector as mysql
from Beec import TheSystemMessages as myMsgs

import random

def ConnectToDB():
    try:
        mydb = mysql.connect(
        host="localhost",
        user="root",
        password="alibhp110",
        database="ecardbd2"
        )
        return  mydb
    except:
        return "Connection to database error"

def SendSQL(myDBin, SQLStatment:str, parameters={}, returnDate=True, returnColumns=False):
    try:
        mycursor = myDBin.cursor()

        # Exucte the SQL
        mycursor.execute(SQLStatment, parameters)

        if (returnDate):
            if returnColumns:
                dd =mycursor.fetchone()
                if dd != None:
                    row = dict(zip(mycursor.column_names, dd))
                    return row
                else:
                    return ["err", "No Data"]
            return mycursor.fetchall()
        else:
            myDBin.commit()
            return ["OK", ""]
    except (mysql.Error, mysql.Warning) as e:
        return ["err", str(e)]
    #except:
    #    return ["err", "Unkonw DB ERR"]

    # for x in myresult:
    #    print(x[1])

def InsertSQL(Conn, SQLStatment:str, parameters={}, returnID=True):
    try:
        mycursor = Conn.cursor()
        mycursor.execute(SQLStatment, parameters)
        Conn.commit()

        if returnID:
            lastEnteredID = mycursor.lastrowid
            return ["OK", str(lastEnteredID)]
        return ["OK", ""]
    except (mysql.Error, mysql.Warning) as e:
        if e.errno == 1062:
            return ["err", myMsgs.getErrorMessage(msgID=5, Languge="EN")]
        else:
            return ["err", str(e)]
    except:
        return ["err", "Unkonw DB ERR"]


def CloseConnection(connection):
    if (connection.is_connected()):
        connection.close()
    return True

def GenerateRadom(DigitsNeeded:int):
    return (int(random.random() * int("1" + ("0" * DigitsNeeded))))
    return random()

# SET NEW.`password` = substr(SHA2(NEW.`password`, 256),1,40)

def makeHTML(WhatYouWant:str, ParaList:str):
    inputtext:str = ParaList
    inputtext = inputtext.split(",")

    r = ""
    if WhatYouWant == "HTML":
        for oneInput in inputtext:
            oneInput = oneInput.replace("`", "")
            oneInput = oneInput.replace(" ", "")
            r = r + '<label for="' + oneInput + '">' + oneInput + ':</label><br><input type="text" id="' + oneInput + '" name="' + oneInput + '"><br>'
    elif WhatYouWant == "INSERT":
        for oneInput in inputtext:
            oneInput = oneInput.replace("`", "")
            oneInput = oneInput.replace(" ", "")
            r = r + "%(" + oneInput + ")s" + ","
        r = r[0:len(r)-1]

    elif WhatYouWant == "UPDATE":
        for oneInput in inputtext:
            oneInput = oneInput.replace("`", "")
            oneInput = oneInput.replace(" ", "")
            r = r + "`" + oneInput + "`=%(" + oneInput + ")s" + ","
        r = r[0:len(r)-1]

    return r