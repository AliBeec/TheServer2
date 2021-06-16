from Beec import EstablishConnection as SqlConn
from Beec import HardFunction as QRCode
from Beec.UserInfo.UserEmployeeUpdates import updateFullInfo
from Beec.Cards.CardTheams import checkTheamLicence
from Beec.CommanFunctions import ReturnResponse
from flask import session
from Beec.Cards.CardTheams import AddNewTheam

import json

import sys

def NewCard(InJSON:json):

    db = SqlConn.ConnectToDB()

    print("WE ARE HERE")

    # The comming JSON to this funcion should contian three jason inside it [CardInfo, TheamInfo, ThemName, Feilds]
    # Extrat the full card Info
    CardInfoJson = json.dumps(InJSON['CardInfo'])
    CardInfoJson = json.loads(InJSON['CardInfo'])

    # Extract the Theam Info,
    # Should have the shape of [0-0-0:0-0-0:0-0-0] = [R-G-B:R-G-B:R-G-B] = [FontColor:BackgroundColor:FrameColor]

    # Extract the card's Selected feilds of shape [Feild:Feild: ...]
    # FeildsString = InJSON['Feilds']

    # 1. Create and add the company ( From the card info passed )
    #       - Check if company exisit
    #       - Check if the emplyee have a company
    # DONE IN THE PREVIOUS STEP

    # Update the info to the database ( This function should make the the new needed fields also)
    r = updateFullInfo(CardInfoJson)
    if r[0] != "OK":
        # Error is return
        print(str(r))
        return r
    else:
        # Update the JSON Object with the new data from the function as the function might have changed accrodingly
        InJSON = r[1]

    # 2. Create and add the theme if needed
    #       - Check if the comapny has the enough theam licene
    #       - Theam(String that tell what colors seperated with '-', ORDER: Background, FontColor, BoarerColor) d
    #                           (COLORS ARE IN R, G, B for each '-' string)

    TheamID = AddNewTheam(ThemName=InJSON['ThemName'],TheamInfo=InJSON['Theam'],
                ThemStyleID=InJSON['StyleID'], DeptID=CardInfoJson['departementid'])

    if TheamID[0] == 'err':
        return TheamID
    else:
        TheamID = TheamID[1]

    # 3. Create and add the card
    #       - Check if user have the correct licence for the number of cards allowed
    #       - Set the new card as the default card

    cardInsertSQL = "INSERT INTO `cards`(`isprivate`, `visitcounter`, `foremployee`, `applytheamid`, `INFO`) " \
                    "VALUES (0, 0,'" + str(session['EmpID']) + "'," + str(TheamID) \
                    + "'," + str(InJSON["Feilds"]) + "')"

    print("Card Insertion SQL:", str(cardInsertSQL))

    return ["err", "Not Done yet"]

    # 4. Create a QR code

    # Req Paramters: EmployeeID, UserID,

    # ----------------------------------------
    #   Check if EMP have a card
    # ----------------------------------------
    #theSQL = "SELECT * FROM `cards` WHERE `foremployee`" + InJSON['EmpID']

    # Grap the data from the database
    #db = SqlConn.ConnectToDB()
    #r = SqlConn.SendSQL(db, theSQL)

    #if r[0] == "err":
        # No card is found, add the new card
    #    ResultData = SqlConn.InsertSQL(db,
    #               "INSERT INTO `cards`(`foremployee`, `applytheamid`, `INFO`) VALUES(%(EmpID)s , %(TheamID)s , %(JsonData)s )",
    #               POST_REQUEST, True)

    #    if ResultData[0] == "OK":
    #        # Return the card ID
    #        return (ResultData[1])
    #    else:
    #        return ("Fail")

    #else:
        # Card was found, can't add new one
    #    return ("Card Found")