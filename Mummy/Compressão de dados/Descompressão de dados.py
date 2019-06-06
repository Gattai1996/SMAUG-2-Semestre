import base64

with open('menu_cópia.png', 'rb') as File:

    with open('menu_cópia2.png', 'wb') as imageFile:
        string = base64.b64decode(bytes(File))
        imageFile.write(string)
        imageFile.close()
