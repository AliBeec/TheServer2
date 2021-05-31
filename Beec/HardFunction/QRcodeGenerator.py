import qrcode

# Return is an image content, when get it back, use the command
#   [RETURN REUSLT FORM THIS].save([FILE NAME])
def GetQRCodeImage(QRValue):
    qr = qrcode.QRCode(
        box_size=10,
        border=10,
    )
    qr.add_data(QRValue)
    qr.make(fit=True)

    return qr.make_image(fill_color="black", back_color="white").convert('RGB')
