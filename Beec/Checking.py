import re

EnglishLitters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
ArabicLitters = "اأإبتثجحخدذرزسشصضطظعغفقكلمنهويةلآآلإئءؤ"
ArabicNumbers = "1234567890"
EnglishLitters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def RemoveUnwantedChar(inputText:str):
    result = ""
    for oneChar in inputText:
        if oneChar in EnglishLitters or  oneChar in ArabicLitters or oneChar in ArabicNumbers:
            result = result + oneChar
    return result

def onlyNumber(inputStr:str):
    result = ""
    for oneChar in inputStr:
        if oneChar in ArabicNumbers:
            result = result + oneChar
    return result


def CheckEamilFormat(email:str):
    regex = '^[\w_.-]+@([\w-]+\.)+\w{2,4}$'
    if (re.search(regex, email)):
        return True

    else:
        return False

def passwordComplexity(password):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    # calculating the length
    length_error = len(password) < 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(r"\W", password) is None

    # overall result
    password_ok = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error )

    result = {
        'password_ok' : password_ok,
        'length_error' : length_error,
        'digit_error' : digit_error,
        'uppercase_error' : uppercase_error,
        'lowercase_error' : lowercase_error,
        'symbol_error' : symbol_error  }

    if password_ok == True:
        return "OK"
    else:
        for r in result:
            if r != "password_ok":
                if result[r] == True:
                    return r

if __name__ == "__main__":
    print(passwordComplexity("Hdaddoken#6487"))