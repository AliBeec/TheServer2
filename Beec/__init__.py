from flask import Flask
import flask_mail as eMail
'''
    Add the Job and depratment connection to the Empoyee
    Make the edit option available using the select list

'''

app = Flask(__name__)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "beec.app.sa@gmail.com",
    "MAIL_PASSWORD": "Alibhp#2110"
}

app.config.update(mail_settings)
mail = eMail.Mail(app)

app.config["UploadImageFolder"] = "Beec\\UploadedImgs"

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

import Beec.OnlyWebsite
import Beec.OnlyApp
import Beec.LoginRouts