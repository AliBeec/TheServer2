from Beec import EstablishConnection as SqlConn
from Beec import Checking

def getCardFullInfo(cardID:str):

    cardID = Checking.RemoveUnwantedChar(cardID)
    return SqlConn.SendSQL("Select * from Cards WHERE cardid='" + cardID + "'")

def getSelectedFeilds(cardID:str):

    cardID = Checking.RemoveUnwantedChar(cardID)
    return SqlConn.SendSQL("Select INFO from Cards WHERE cardid='" + cardID + "'")
