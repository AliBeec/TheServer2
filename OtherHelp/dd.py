NamesStr ="jobname,nickname,firstname,middlename,grandname,lastname,abuname,phone,mobile,hometel,empEmail,workphone,notes,departementname,detpPhone1,detpPhone2,DeptEmail1,DeptEmail2,DeptWeb,companyname,CompWeb"
StringName = ["Position","Nick Name","First Name","Middle Name","Grandfather Name","Last Name","Abu Name","Phone Number","Mobile Number","Home Telephone","Employee Email Address","Work Phone","Notes","Department Name","Department phone","Other Department phone","Department Email","Other Department Email","Department Website","Company Name","Company Website"]

NamesStr = NamesStr.split(",")

for oneName, longName in zip(NamesStr, StringName):
     oneItem = "<StackLayout Orientation=\"Horizontal\">\n"
     oneItem =  oneItem + "\t<Label Text=\"" + longName + "\" Style=\"{StaticResource TitleLabel}\"/>\n"
     oneItem = oneItem + "\t<Switch HorizontalOptions=\"EndAndExpand\" x:Name=\"chk" + oneName + "\"/>\n"
     oneItem = oneItem + "</StackLayout>\n"
     oneItem = oneItem + "<Entry Placeholder=\"" + longName + "\" x:Name=\"" + oneName + "\"/>\n"
     print(oneItem)
