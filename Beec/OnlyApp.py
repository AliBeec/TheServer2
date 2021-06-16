import Beec.Cards.CardInfo as CardInfo
from Beec.Cards.NewCard import NewCard as AddNewCard
from Beec import EstablishConnection as SqlConn, CommanFunctions as beecFunc, app, Checking
from flask import request, session
import json, os, random

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

    UserID = Checking.onlyNumber(UserID)

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


# --------------------------------------------------------------------------------------------

@app.route('/NewCard', methods=['POST'])
def CreateNewCard():

    if beecFunc.checkLogin() == False:
        return beecFunc.ReturnResponse("LGOIN")

    # Request :
    #   - CardInfo(JSON OBJECT tell all the data),
    #   - Theam(String that tell what colors seperated with '-', ORDER: Background, FontColor, BoarerColor) d
    #                       (COLORS ARE IN R, G, B for each '-' string)
    #   - Feilds(String List of wanted feild seperated with ":"

    if request.method == 'POST':
        # Convert the input to JSON object
        FullInData = json.dumps(request.form)
        FullInData = json.loads(FullInData)

        print(FullInData)
        # Call the create Card Module

        # Call the a function in the folder Cards/NewCard.py [It was imported in this name]
        NewCardResult = AddNewCard(FullInData)

        if NewCardResult[0] == "OK":
            return beecFunc.ReturnResponse("OK")
        else:
            return beecFunc.ReturnResponse("err")

        #return beecFunc.ReturnResponse(NewCard.NewCard(POST_REQUEST=))

# --------------------------------------------------------------------------------------------

@app.route('/WantedFeilds', methods=['GET', 'POST'])
def WantedFeilds():
    if checkLogin() == False:
        return

    UserID = str(session['UserID'])
    return beecFunc.ReturnResponse(CardInfo.getSelectedFeilds(UserID))

# --------------------------------------------------------------------------------------------

@app.route('/UploadImage', methods=['POST'])
def uploadingImageToServer():

    if checkLogin() == False:
        return beecFunc.ReturnResponse("LOGIN")

    FileStorage = request.files["image"]

    # Make the new image file name
    randNum =  str(random.random()*1000)[:3]
    imageFileName = FileStorage.filename + "_" + str(session["UserID"]) + "_" + str(randNum) + ".png"

    print(request.files)

    # Save the comming picture
    FileStorage.save(os.path.join(app.config["UploadImageFolder"], imageFileName))

    # React with DB
    r = beecFunc.addImageToDB(FileName=FileStorage.filename, ImageName=imageFileName)

    if 'err' in r:
        return beecFunc.ReturnResponse("err")
    else:
        return beecFunc.ReturnResponse("OK")

# --------------------------------------------------------------------------------------------
#    Undecordated methods
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

def checkLogin():
    if beecFunc.checkLogin() == False:
        return beecFunc.ReturnResponse("LOGIN")
    else:
        return True

