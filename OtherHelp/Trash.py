Names = ['jobname', 'nickname', 'firstname', 'middlename', 'grandname', 'lastname', 'abuname', 'phone', \
         'mobile', 'hometel', 'empEmail', 'workphone', 'notes', 'departementname', \
         'detpPhone1', 'detpPhone2', 'DeptEmail1', 'DeptEmail2', \
         'DeptWeb', 'companyname', 'CompWeb']

def makeHTML():
    inputtext:str = input("Enter the list of item with ',' as sperator:")
    inputtext = inputtext.split(",")

    #Reenter: UserName: Passowrd: Re-enter: Nickname: First Name: Middle Name: Grand Father Name: Family Name: Abu Name: Mobile Number: Phone Number: Home Phone: Work phone: notes:

    print("HTML")
    for oneInput in inputtext:
        oneInput = oneInput.replace("`", "")
        oneInput = oneInput.replace(" ", "")
        print('<label for="' + oneInput + '">' + oneInput + ':</label><br><input type="text" id="' + oneInput + '" name="' + oneInput + '"><br>' )
    print('<button type="submit" name="newC" id="butNewC">new</button>  |        <button type="submit" name="editC" id="butEditC">update</button><br>')

    print("INSERT")
    for oneInput in inputtext:
        oneInput = oneInput.replace("`", "")
        oneInput = oneInput.replace(" ", "")
        print("%(" + oneInput + ")s", end=",")

    print("UPDATE")
    for oneInput in inputtext:
        oneInput = oneInput.replace("`", "")
        oneInput = oneInput.replace(" ", "")
        print("`" + oneInput + "`=%(" + oneInput + ")s", end=",")

def dd():
    for one in Names:
        # <EntryCell Label="Title/Nickname" Text="" x:Name="txtNickName"  Keyboard="Text"/>
        #nickname.Text = App.UserSavedData.nickname;
        print('<ViewCell><Grid><Grid.ColumnDefinitions><ColumnDefinition Width="25*"/><ColumnDefinition Width="60*"/>'
              '<ColumnDefinition Width="15*"/></Grid.ColumnDefinitions><Grid.RowDefinitions><RowDefinition/></Grid.RowDefinitions>'
              '<Label Text="' + one + '" Grid.Column="0" Grid.Row="0"/><Entry x:Name="'+one+'"Grid.Column="1" Grid.Row="0"/>'
              '<Switch x:Name:chk' + one + 'IsEnabled="True" Grid.Column="2" Grid.Row="0"/></Grid></ViewCell>')

def SwitchEquat(inString:str):

    I = 0
    Pre_I = 0
    result= []

    for litter in inString:
        I = I + 1
        if litter == "=" or litter == ";":
            result.append(inString[Pre_I:I-1])
            Pre_I = I

    prev:bool = False
    prevValue = ""

    print(result)
    newResult = ""

    for one in result:
        if prev:
            newResult = newResult + one + "=" + prevValue + "; \n"
            prev = False
        else:
            prevValue = one
            prev = True

    print(newResult)

def CreateSwitchString():
    FinalResult = ""
    for one in Names:
        FinalResult = FinalResult + "if (chk" + one + ".IsToggled)\nResult = Result + " + "\":" + one + "\";\n"

    print(FinalResult)

def FullInfoUpdate():
    result = ""
    for one in Names:
        result = result + one + '.Text = App.UserSavedData.theJsonObject["' + one + '"].ToString();'

    print(result)
    return result

def ifCheck():
    for oneName in Names:
        print('if (oneField == "'+oneName+'") chk'+oneName+'.IsEnabled = true;')

import json

if __name__ == "__main__":

    rr = {}

    #rr = "bb"

    print(json.dumps(rr))


    theSQL = "SELECT `nickname`, `firstname`, `middlename`, `grandname`, `lastname`, `abuname`, `phone`, " \
             "`mobile`, `hometel`, emp.`email` as empEmail, `workphone`, `notes`, `departementname`, `landphone1` " \
             "as detpPhone1, `landphone2` as detpPhone2, dept.`email` as DeptEmail1, `email2` as DeptEmail2, " \
             "dept.`website` as DeptWeb, `companyname`, `websitelink` as CompWeb " \
             "FROM employee emp,empbelongstodeprt EmpDept, departement dept, company " \
             "WHERE `userid`='----' AND `licencesid`!='' AND emp.`empid`=EmpDept.empid " \
                                           "AND empDept.departid = dept.departementid AND company.companyid = dept.belongtocomapny"

    makeHTML()

    #print(theSQL)
    #dd()#

    #SwitchEquat(FullInfoUpdate())

    #ifCheck()

    #SwitchEquat("nickname.Text = App.UserSavedData.nickname; " + \
    #        "firstname.Text = App.UserSavedData.firstname; " + \
    #        "middlename.Text = App.UserSavedData.middlename; " + \
    #        "grandname.Text = App.UserSavedData.grandname; " + \
    #        "lastname.Text = App.UserSavedData.lastname; " + \
    #        "abuname.Text = App.UserSavedData.abuname; " + \
    #        "phone.Text = App.UserSavedData.phone; " + \
    #        "mobile.Text = App.UserSavedData.mobile; " + \
    #        "hometel.Text = App.UserSavedData.hometel; " + \
    #        "empEmail.Text = App.UserSavedData.empEmail; " + \
    #        "workphone.Text = App.UserSavedData.workphone; " + \
    #        "notes.Text = App.UserSavedData.notes; " + \
    #        "departementname.Text = App.UserSavedData.departementname; " + \
    #        "detpPhone1.Text = App.UserSavedData.detpPhone1; " + \
    #        "detpPhone2.Text = App.UserSavedData.detpPhone2; " + \
    #        "DeptEmail1.Text = App.UserSavedData.DeptEmail1; " + \
    #        "DeptEmail2.Text = App.UserSavedData.DeptEmail2; " + \
    #        "DeptWeb.Text = App.UserSavedData.DeptWeb; " + \
    #        "companyname.Text = App.UserSavedData.companyname; " + \
    #        "CompWeb.Text = App.UserSavedData.CompWeb; " + \
    #        "jobname.Text = App.UserSavedData.jobname;")