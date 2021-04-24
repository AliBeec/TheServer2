from Beec import EstablishConnection as SqlConn


def NewCard(POST_REQUEST):

    print("WE ARE HERE")
    print(POST_REQUEST)

    return "DONE"

    # Clean the input data

    # 1. Create and add the company ( From the card info passed )
    #       - Check if company exisit
    #       - Check if the emplyee have a company
    companyCheck = SqlConn.SendSQL("SELECT * FROM `company` WHERE `companyname`=" + CardJSON['companyname'])
    if "err" in companyCheck:
        # Insert the new comapny
        print("err")
        # Check if this is allow
    else:
        CardInsertSQL = "INSERT INTO `cards`(`foremployee`, `applytheamid`, `INFO`) " \
                    "VALUES ([value-1],[value-2],[value-3])"

    # 2. Create and add the theme
    #       - Check if the comapny has the enough licene
    # 3. Create and add the card

    # Req Paramters: EmployeeID, UserID,

    # ----------------------------------------
    #   Check if EMP have a card
    # ----------------------------------------
    theSQL = "SELECT * FROM `cards` WHERE `foremployee`" + POST_REQUEST['EmpID']
    # Grap the data from the database
    db = SqlConn.ConnectToDB()
    r = SqlConn.SendSQL(db, theSQL)

    if r[0] == "err":
        # No card is found, add the new card
        ResultData = SqlConn.InsertSQL(db,
                                       "INSERT INTO `cards`(`foremployee`, `applytheamid`, `INFO`) VALUES(%(EmpID)s , %(TheamID)s , %(JsonData)s )",
                                       POST_REQUEST, True)

        if ResultData[0] == "OK":
            # Return the card ID
            return (ResultData[1])
        else:
            return ("Fail")

    else:
        # Card was found, can't add new one
        return ("Card Found")